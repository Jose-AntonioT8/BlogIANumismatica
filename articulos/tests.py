from datetime import date, datetime, timezone

from django.test import TestCase

from .models import Article
from .servicio import crear, listar, obtener
from .text import excerpt


class GabineteTests(TestCase):
    def test_portada_ordenada(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        html = response.content.decode()
        titles = [
            'La onza sevillana y el oro del Guadalquivir',
            'Cuando la peseta se hizo papel',
            'Cómo leer la ceca de una moneda',
            'El real de a ocho, la moneda que dio la vuelta al mundo',
        ]
        positions = [html.index(title) for title in titles]
        self.assertEqual(positions, sorted(positions))
        self.assertContains(response, '29 de octubre de 2026')
        self.assertContains(response, '2 de junio de 2026')
        self.assertIn('…', excerpt(Article.objects.get(slug='peseta-en-papel').body))

    def test_empate_por_created_at_y_posicion(self):
        shared = date(2026, 11, 1)
        Article.objects.create(
            slug='alfa',
            title='A' * 120,
            body='Texto de la ficha alfa.\n\nSegundo párrafo.',
            published_on=shared,
            piece_type='Moneda',
            created_at=datetime(2026, 11, 1, 8, 0, tzinfo=timezone.utc),
        )
        Article.objects.create(
            slug='beta',
            title='Ficha beta de verificación',
            body='Texto de la ficha beta.',
            published_on=shared,
            piece_type='Medalla',
            created_at=datetime(2026, 11, 1, 9, 0, tzinfo=timezone.utc),
        )
        html = self.client.get('/').content.decode()
        self.assertLess(html.index('Ficha beta de verificación'), html.index('A' * 120))

    def test_detalle_parrafos_y_tipo(self):
        response = self.client.get('/articulo/real-de-a-ocho/')
        self.assertContains(response, 'Moneda')
        self.assertContains(response, '12 de marzo de 2026')
        self.assertContains(response, 'viajó en galeones')
        self.assertContains(response, 'De esa familiaridad salió el dólar')
        prose = response.content.decode().split('<div class="prose">', 1)[1].split('</div>', 1)[0]
        self.assertEqual(prose.count('<p>'), 3)

    def test_html_del_cuerpo_se_muestra_como_texto(self):
        Article.objects.create(
            slug='con-marca',
            title='Ficha con marca literal',
            body='Si alguien anota <em>ensaye</em>, se lee tal cual.',
            published_on=date(2026, 1, 2),
            piece_type='Moneda',
        )
        response = self.client.get('/articulo/con-marca/')
        self.assertContains(response, '&lt;em&gt;ensaye&lt;/em&gt;')
        self.assertNotContains(response, '<em>ensaye</em>')

    def test_no_encontrado(self):
        response = self.client.get('/articulo/no-existe/')
        self.assertContains(response, 'Pieza no encontrada', status_code=404)
        self.assertContains(response, 'Ese artículo no está en el gabinete.', status_code=404)
        self.assertContains(response, 'Volver al listado', status_code=404)

    def test_alta_invalida_no_guarda(self):
        before = Article.objects.count()
        empty = self.client.post('/nueva/', {
            'title': '   ',
            'body': '',
            'published_on': '',
            'piece_type': '',
        })
        self.assertContains(empty, 'El título es obligatorio')
        self.assertContains(empty, 'El cuerpo es obligatorio')
        self.assertContains(empty, 'La fecha es obligatoria')
        self.assertContains(empty, 'El tipo es obligatorio')

        bad_date = self.client.post('/nueva/', {
            'title': 'Fecha imposible',
            'body': 'No debe guardarse.',
            'published_on': '2026-02-29',
            'piece_type': 'Moneda',
        })
        self.assertContains(bad_date, 'La fecha debe ser un día real con el formato AAAA-MM-DD')

        bad_type = self.client.post('/nueva/', {
            'title': 'Tipo inválido',
            'body': 'No debe guardarse.',
            'published_on': '2026-01-15',
            'piece_type': 'Ficha',
        })
        self.assertContains(bad_type, 'El tipo debe ser Moneda, Billete o Medalla')

        long_title = self.client.post('/nueva/', {
            'title': 'A' * 121,
            'body': 'Título demasiado largo.',
            'published_on': '2026-01-15',
            'piece_type': 'Moneda',
        })
        self.assertContains(long_title, 'El título admite como máximo 120 caracteres')
        self.assertEqual(Article.objects.count(), before)
        self.assertFalse(Article.objects.filter(title='Fecha imposible').exists())

    def test_alta_valida_guarda_tipo_y_abre_detalle(self):
        response = self.client.post('/nueva/', {
            'title': 'Medalla de proclamación',
            'body': 'Una medalla recuerda el juramento, no compra el pan.\n\nPor eso no es una moneda.',
            'published_on': '2026-10-20',
            'piece_type': 'Medalla',
        })
        article = Article.objects.get(title='Medalla de proclamación')
        self.assertEqual(article.piece_type, 'Medalla')
        self.assertRedirects(response, f'/articulo/{article.slug}/')
        home = self.client.get('/')
        html = home.content.decode()
        self.assertLess(
            html.index('La onza sevillana y el oro del Guadalquivir'),
            html.index('Medalla de proclamación'),
        )
        self.assertLess(
            html.index('Medalla de proclamación'),
            html.index('Cuando la peseta se hizo papel'),
        )

    def test_persiste_en_la_base(self):
        self.client.post('/nueva/', {
            'title': 'Ficha que permanece',
            'body': 'Sigue aquí después de consultar de nuevo.',
            'published_on': '2026-04-04',
            'piece_type': 'Billete',
        })
        article = Article.objects.get(slug='ficha-que-permanece')
        self.assertEqual(article.piece_type, 'Billete')
        again = Article.objects.get(pk=article.pk)
        self.assertEqual(again.title, 'Ficha que permanece')

    def test_estado_vacio(self):
        Article.objects.all().delete()
        response = self.client.get('/')
        self.assertContains(response, 'El gabinete está vacío')
        self.assertContains(response, 'Todavía no hay piezas catalogadas.')
        self.assertContains(response, 'Catalogar la primera pieza')
        self.assertNotContains(response, 'No hay piezas de este tipo.')
        self.assertNotContains(response, 'aria-label="Tipo de pieza"')

    def test_filtro_y_sin_clasificar(self):
        billete = self.client.get('/?tipo=Billete')
        self.assertContains(billete, 'Cuando la peseta se hizo papel')
        self.assertNotContains(billete, 'El real de a ocho')
        medalla = self.client.get('/?tipo=Medalla')
        self.assertContains(medalla, 'No hay piezas de este tipo.')
        self.assertContains(medalla, 'Todas')

        Article.objects.create(
            slug='pieza-sin-tipo',
            title='Pieza sin clasificar',
            body='Artículo anterior a la clasificación.',
            published_on=date(2020, 5, 5),
            piece_type='',
            created_at=datetime(2020, 5, 5, tzinfo=timezone.utc),
        )
        home = self.client.get('/')
        self.assertContains(home, 'Sin clasificar')
        moneda = self.client.get('/?tipo=Moneda')
        self.assertNotContains(moneda, 'Pieza sin clasificar')
        detail = self.client.get('/articulo/pieza-sin-tipo/')
        self.assertContains(detail, 'Sin clasificar')


class ServicioMcpTests(TestCase):
    def test_listar_y_filtrar(self):
        pieces = listar()
        self.assertEqual(pieces[0]['titulo'], 'La onza sevillana y el oro del Guadalquivir')
        billetes = listar('Billete')
        self.assertEqual([piece['titulo'] for piece in billetes], ['Cuando la peseta se hizo papel'])
        with self.assertRaisesMessage(ValueError, 'El tipo debe ser Moneda, Billete o Medalla'):
            listar('Ficha')

    def test_obtener_desconocido(self):
        with self.assertRaisesMessage(ValueError, 'Artículo no encontrado'):
            obtener('no-existe')

    def test_crear_reutiliza_la_validacion_del_formulario(self):
        before = Article.objects.count()
        rejected = crear('   ', '', '2026-02-29', 'Ficha')
        self.assertFalse(rejected['ok'])
        self.assertEqual(rejected['campos']['titulo'], 'El título es obligatorio')
        self.assertEqual(rejected['campos']['cuerpo'], 'El cuerpo es obligatorio')
        self.assertEqual(
            rejected['campos']['fecha'],
            'La fecha debe ser un día real con el formato AAAA-MM-DD',
        )
        self.assertEqual(rejected['campos']['tipo'], 'El tipo debe ser Moneda, Billete o Medalla')
        self.assertEqual(Article.objects.count(), before)

        created = crear(
            'Duro columnario',
            'Las columnas y la banda dieron pie al símbolo del dólar.',
            '2026-07-01',
            'Moneda',
        )
        self.assertTrue(created['ok'])
        self.assertEqual(created['articulo']['tipo'], 'Moneda')
        self.assertEqual(created['articulo']['ruta'], '/articulo/duro-columnario/')
        opened = obtener('duro-columnario')
        self.assertEqual(opened['titulo'], 'Duro columnario')

    def test_el_servidor_mcp_registra_las_tres_herramientas(self):
        import servidor_mcp

        names = sorted(tool.name for tool in servidor_mcp.mcp._tool_manager.list_tools())
        self.assertEqual(names, ['crear_articulo', 'listar_articulos', 'obtener_articulo'])
        listed = servidor_mcp.listar_articulos(tipo='Medalla')
        self.assertEqual(listed, [])
        from mcp.server.mcpserver.exceptions import ToolError
        with self.assertRaisesMessage(ToolError, 'Artículo no encontrado'):
            servidor_mcp.obtener_articulo('no-existe')
