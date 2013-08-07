#!/usr/bin/env python

"""
Bootstrap and serve your application. This file also serves to not make your
application completely reliant upon DotCloud's hosting service.

If you're in a development environment, envoke the script with:
    $ python bootstrap.py

In a production environment, your application can be run with the `gevent`
Python library:
    $ python bootstrap.py --gevent

"""

import argparse
from app import create_app


def parse_arguments():
    """Parse any additional arguments that may be passed to `bootstrap.py`."""
    parser = argparse.ArgumentParser()
    parser.add_argument('port', nargs='?', type=int, default=5050,
                        help="Port to run the server on.")
    parser.add_argument('--gevent', action='store_true',
                        help="Run gevent's production server.")
    args = parser.parse_args()
    return args


def serve_app(env):
    """
    Serve your application. If `dev_environment` is true, then the
    application will be served using gevent's WSGIServer.
    """
    app = create_app()
    if env.gevent:
        from gevent.wsgi import WSGIServer
        http_server = WSGIServer(('', env.port), app)
        http_server.serve_forever()
    else:
        app.run(debug=True, port=env.port)


if __name__ == '__main__':
    env = parse_arguments()
    serve_app(env)
