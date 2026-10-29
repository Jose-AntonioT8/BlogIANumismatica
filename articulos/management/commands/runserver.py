from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Arranca el blog y el MCP en http://127.0.0.1:8080/mcp.'

    def add_arguments(self, parser):
        parser.add_argument('addrport', nargs='?', default='127.0.0.1:8080')

    def handle(self, *args, **options):
        import uvicorn

        self.check(display_num_errors=True)
        host, port = _host_port(options['addrport'])
        uvicorn.run('gabinete.asgi:application', host=host, port=port)


def _host_port(addrport):
    if ':' in addrport:
        host, port_text = addrport.rsplit(':', 1)
        return host or '127.0.0.1', int(port_text)
    return '127.0.0.1', int(addrport)
