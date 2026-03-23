"""Passenger WSGI entry point for cPanel Python hosting."""

import sys
import os

# Add the app directory to path
sys.path.insert(0, os.path.dirname(__file__))

from stripe_inspector.web.app import create_app

# Passenger expects an 'application' callable
# Set token via environment variable if needed: TOKEN=mysecret
token = os.environ.get("TOKEN", None)
app = create_app(token=token)

# Passenger needs a WSGI app, but FastAPI is ASGI
# Use a2wsgi to bridge ASGI -> WSGI
try:
    from a2wsgi import ASGIMiddleware
    application = ASGIMiddleware(app)
except ImportError:
    # Fallback: try uvicorn if a2wsgi not available
    print("ERROR: a2wsgi not installed. Run: pip install a2wsgi", file=sys.stderr)
    def application(environ, start_response):
        start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
        return [b'a2wsgi not installed. Run: pip install a2wsgi']
