__config__ = 'config.yml'

import sys
import re
import yaml

import tornado.httpserver
import tornado.ioloop
import tornado.web

from tornado.options import define, options
from handlers.urls import url_patterns

define('settings', default=None, help='load settings(default: common)')


class App(tornado.web.Application):
    def __init__(self, settings):
        tornado.web.Application.__init__(self, url_patterns, **settings)


def get_config():
    try:
        if options.settings:
            path = re.sub(r'\.', '\/', options.settings)
        else:
            path = __config__
        f = file(path, 'r')
        config = yaml.load(f)
        f.close()
    except IOError:
        print 'Invalid or missing config file %s' % __config__
        sys.exit(1)

    return config

def main():
    tornado.options.parse_command_line()
    config = get_config()

    if not config or 'settings' not in config:
        print 'No default configuration found - settings'
        sys.exit(1)

    settings = config['settings']
    for k,v in settings.items():
        if k.endswith('_path'):
            settings[k] = settings[k].replace(
                '__path__',
                os.path.dirname(__file__),
            )

    http_server = tornado.httpserver.HTTPServer(App(settings))
    http_server.listen(settings['port'])

    if 'debug' in settings and settings['debug'] is True:
        tornado.autoreload.start()
        print 'Tornado Debug HttpServer Start.'
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
