import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gabinete.settings')

from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler
from django.core.asgi import get_asgi_application

django_application = ASGIStaticFilesHandler(get_asgi_application())

from servidor_mcp import mcp

_mcp = mcp.streamable_http_app(streamable_http_path='/mcp', host='127.0.0.1')


async def application(scope, receive, send):
    path = scope.get('path', '')
    if scope['type'] == 'lifespan' or path == '/mcp' or path.startswith('/mcp/'):
        await _mcp(scope, receive, send)
        return
    await django_application(scope, receive, send)
