## Django WSGI application path in pattern MODULE_NAME:VARIABLE_NAME
wsgi_app = "src.core.wsgi:application"

## The granularity of Error log outputs
loglevel = "debug"

## The number of worker processes for handling requests
workers = 2

## The socket to bind
bind = "0.0.0.0:8000"