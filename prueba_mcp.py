import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


async def main():
    async with streamable_http_client('http://127.0.0.1:8080/mcp') as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            print('TOOLS', [tool.name for tool in tools.tools])
            listed = await session.call_tool('listar_articulos', {'tipo': 'Billete'})
            print('LIST', listed)
            missing = await session.call_tool('obtener_articulo', {'identificador': 'no-existe'})
            print('MISSING', missing)


asyncio.run(main())
