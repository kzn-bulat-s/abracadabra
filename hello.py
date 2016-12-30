def parse_params(params):
    for param in params.split('&'):
        yield '%s\n' % (param,)

def app(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return parse_params(environ['QUERY_STRING'])

