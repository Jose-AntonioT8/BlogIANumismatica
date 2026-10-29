"""Redacta una pieza de El Gabinete con Ollama y la publica mediante el MCP.

Solo crea artículos de numismática. No edita ni borra piezas ya guardadas.
"""
import asyncio
import json
import os
import re
import sys
from datetime import date
from typing import Literal

from mcp import Client
from ollama import AsyncClient
from pydantic import BaseModel, Field

MODELO = os.getenv("OLLAMA_MODEL", "qwen3:4b")
URL_MCP = "http://127.0.0.1:8080/mcp"
# La única escritura permitida. listar_articulos solo se lee para no repetir títulos.
HERRAMIENTA_CREAR = "crear_articulo"

# Programación y ejercicios de código no son una pieza del gabinete.
_CODIGO = re.compile(
    r"(?i)(\bpython\b|\bjavascript\b|\bjava\b|\bc\+\+\b|"
    r"\bprogramaci[oó]n\b|\bdef\s+\w+\s*\(|\bprint\s*\(|"
    r"\bimport\s+\w+|```|asteriscos?|pir[aá]mide)"
)
# El tipo "Moneda" no basta: el texto tiene que hablar de una pieza o de su historia.
_ANCLA = re.compile(
    r"(?i)\b("
    r"monedas?|billetes?|medallas?|numism[aá]tic[ao]s?|cecas?|"
    r"acuñ\w*|cuños?|cospeles?|cospel|anverso|reverso|"
    r"ensay\w*|vell[oó]n|platas?|oros?|cobres?|n[ií]queles?|"
    r"reales?|pesetas?|denarios?|sestercios?|onzas?|"
    r"maraved[ií](?:es|s)?|escudos?|columnarios?|macuquinas?|"
    r"filigranas?|troquel\w*|exergo|efigies?|leyendas?|"
    r"conmemorativ\w*|papel moneda|casa de moneda"
    r")\b"
)


class Articulo(BaseModel):
    titulo: str = Field(min_length=1, max_length=120)
    cuerpo: str = Field(min_length=1, max_length=20000)
    fecha: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    tipo: Literal["Moneda", "Billete", "Medalla"]


class Veredicto(BaseModel):
    numismatica: bool
    motivo: str = ""


class EncargoCorregido(BaseModel):
    texto: str = Field(min_length=1, max_length=4000)


class FichaCorregida(BaseModel):
    titulo: str = Field(min_length=1, max_length=120)
    cuerpo: str = Field(min_length=1, max_length=20000)


async def usar_mcp(nombre, argumentos):
    # Una conexion nueva para cada llamada: no permanece abierta mientras Ollama trabaja.
    async with Client(URL_MCP) as cliente:
        respuesta = await cliente.call_tool(nombre, argumentos)
    if respuesta.is_error:
        texto = " ".join(b.text for b in respuesta.content if b.type == "text")
        raise RuntimeError(f"{nombre}: {texto or 'error de la herramienta'}")
    datos = respuesta.structured_content
    if datos is None:
        texto = "\n".join(b.text for b in respuesta.content if b.type == "text")
        datos = json.loads(texto)
    if isinstance(datos, dict) and set(datos) == {"result"}:
        datos = datos["result"]
    if isinstance(datos, dict) and datos.get("ok") is False:
        campos = datos.get("campos") or {}
        detalle_campos = ", ".join(f"{campo}: {mensaje}" for campo, mensaje in campos.items())
        mensaje = datos.get("error") or "Django no ha publicado la pieza"
        if detalle_campos:
            mensaje = f"{mensaje} ({detalle_campos})"
        raise RuntimeError(f"{nombre}: {mensaje}")
    if isinstance(datos, dict) and datos.get("error"):
        raise RuntimeError(f"{nombre}: {datos['error']}")
    return datos


def rechazar(motivo):
    print(f"NO PUBLICADO: {motivo}", flush=True)
    return False


def parece_codigo(texto):
    return _CODIGO.search(texto or "") is not None


def tiene_ancla(texto):
    return _ANCLA.search(texto or "") is not None


async def consultar(mensajes, esquema, aviso, limite):
    print(f"Ollama ({MODELO}): {aviso}", flush=True)
    tarea = asyncio.create_task(AsyncClient(timeout=150).chat(
        model=MODELO, messages=mensajes, think=False,
        format=esquema,
        options={"temperature": 0, "num_predict": limite},
    ))
    try:
        for segundos in range(20, 121, 20):
            terminado, _ = await asyncio.wait({tarea}, timeout=20)
            if terminado:
                respuesta = await tarea
                return respuesta.message.content
            print(f"Ollama sigue en ello ({segundos} s)...", flush=True)
        raise TimeoutError("Ollama no ha respondido en 120 segundos")
    finally:
        if not tarea.done():
            tarea.cancel()
            await asyncio.gather(tarea, return_exceptions=True)


_ORTOGRAFIA = (
    "Corriges solo la ortografía y la acentuación del español. "
    "No cambies el significado, los datos, los nombres propios, los años, "
    "las cecas ni el tipo de pieza. No añadas ni quites hechos. "
    "Si no hay errores, devuelve el mismo texto."
)


async def corregir_encargo(encargo):
    crudo = await consultar(
        [
            {"role": "system", "content": _ORTOGRAFIA + " Devuelve solo el campo texto."},
            {"role": "user", "content": encargo},
        ],
        EncargoCorregido.model_json_schema(),
        "corrigiendo la ortografía del encargo...",
        500,
    )
    texto = EncargoCorregido.model_validate_json(crudo).texto.strip()
    if texto and texto != encargo:
        print("Ollama: ortografía del encargo corregida.", flush=True)
        return texto
    return encargo


async def corregir_ficha(articulo):
    crudo = await consultar(
        [
            {"role": "system", "content": (
                _ORTOGRAFIA + " Devuelve solo titulo y cuerpo."
            )},
            {"role": "user", "content": f"Título: {articulo.titulo}\n\nCuerpo:\n{articulo.cuerpo}"},
        ],
        FichaCorregida.model_json_schema(),
        "corrigiendo la ortografía de la ficha...",
        700,
    )
    ficha = FichaCorregida.model_validate_json(crudo)
    titulo = ficha.titulo.strip()
    cuerpo = ficha.cuerpo.strip()
    if titulo != articulo.titulo or cuerpo != articulo.cuerpo:
        print("Ollama: ortografía de la ficha corregida.", flush=True)
    return articulo.model_copy(update={"titulo": titulo, "cuerpo": cuerpo})


async def admite(texto):
    if parece_codigo(texto):
        return rechazar(
            "el encargo pide programación o código. "
            "Este blog solo cataloga monedas, billetes y medallas."
        )
    crudo = await consultar(
        [
            {"role": "system", "content": (
                "Juzgas encargos para El Gabinete, un blog de numismática. "
                "numismatica es true solo si el tema principal es una moneda, "
                "un billete, una medalla, una ceca, la acuñación o la historia "
                "de esas piezas. Es false para código, programación, tutoriales, "
                "figuras de asteriscos, recetas, deportes, software y cualquier "
                "asunto que no sea una pieza monetaria. Pedir publicarlo en el "
                "blog no lo convierte en numismática. Devuelve numismatica y un motivo breve."
            )},
            {"role": "user", "content": texto},
        ],
        Veredicto.model_json_schema(),
        "comprobando que el encargo sea de numismática...",
        200,
    )
    veredicto = Veredicto.model_validate_json(crudo)
    if veredicto.numismatica:
        return True
    return rechazar(veredicto.motivo or "el encargo no trata de numismática.")


async def redactar(encargo, publicados):
    hoy = date.today().isoformat()
    crudo = await consultar(
        [
            {"role": "system", "content": (
                "Redactas fichas de El Gabinete, un blog local de numismática, "
                "de unas 150 palabras en texto plano. El tema es solo una moneda, "
                "un billete o una medalla. No escribas código, programas ni "
                "tutoriales de software. Separa los párrafos con una línea en "
                "blanco. Usa solo los datos del usuario: no inventes cecas, "
                "reinos, pesos, leyes, números de catálogo ni fuentes. "
                "El tipo es exactamente uno de: Moneda, Billete o Medalla. "
                "La fecha es el día de publicación en formato AAAA-MM-DD; "
                f"si el usuario no indica otro día, usa {hoy}. "
                "Escribe con ortografía y tildes correctas. "
                "Evita títulos ya publicados. Devuelve solo titulo, cuerpo, fecha y tipo."
            )},
            {"role": "user", "content": f"Piezas publicadas: {publicados}\n\n{encargo}"},
        ],
        Articulo.model_json_schema(),
        "redactando la pieza...",
        700,
    )
    return Articulo.model_validate_json(crudo)


async def ejecutar(encargo):
    if not await admite(encargo):
        return
    encargo = await corregir_encargo(encargo)
    publicados = await usar_mcp("listar_articulos", {"tipo": ""})
    if not isinstance(publicados, list):
        raise RuntimeError("listar_articulos no devolvio una lista")
    resumen = [
        f"{a['titulo']} ({a.get('tipo') or 'Sin clasificar'})"
        for a in publicados
        if isinstance(a, dict) and isinstance(a.get("titulo"), str)
    ]
    print(f"MCP: consultadas {len(publicados)} piezas publicadas.", flush=True)
    articulo = await redactar(encargo, resumen)
    print(f"Ollama: pieza redactada ({articulo.titulo}, {articulo.tipo}).", flush=True)
    articulo = await corregir_ficha(articulo)
    texto = f"{articulo.titulo}\n{articulo.cuerpo}"
    if parece_codigo(texto) or not tiene_ancla(texto):
        rechazar(
            "el texto redactado no es una ficha de moneda, billete o medalla. "
            "No se ha creado nada."
        )
        return
    print("MCP: publicando la pieza en Django...", flush=True)
    creado = await usar_mcp(HERRAMIENTA_CREAR, articulo.model_dump())
    pieza = creado.get("articulo") if isinstance(creado, dict) else None
    if not isinstance(creado, dict) or creado.get("ok") is not True or not isinstance(pieza, dict):
        raise RuntimeError(f"Django no ha confirmado la publicacion: {creado!r}")
    if not pieza.get("identificador"):
        raise RuntimeError(f"Django no ha confirmado la publicacion: {creado!r}")
    print(
        f"PIEZA PUBLICADA: {pieza['titulo']} "
        f"({pieza.get('tipo', articulo.tipo)}, {pieza.get('fecha', articulo.fecha)}) "
        f"/articulo/{pieza['identificador']}/",
        flush=True,
    )


def detalle(error):
    if isinstance(error, BaseExceptionGroup):
        return " | ".join(detalle(e) for e in error.exceptions)
    return f"{type(error).__name__}: {error}"


if __name__ == "__main__":
    encargo = input("Describe la pieza que quieres catalogar: ").strip()
    if not encargo:
        sys.exit("ERROR: el encargo está vacío")
    try:
        asyncio.run(ejecutar(encargo))
    except Exception as error:
        print("ERROR:", detalle(error), file=sys.stderr, flush=True)
        sys.exit(1)