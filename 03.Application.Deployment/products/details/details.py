#!/usr/bin/python

from __future__ import print_function
from flask_bootstrap import Bootstrap
from flask import Flask, request, session, render_template, redirect, url_for
from flask import _request_ctx_stack as stack
from jaeger_client import Tracer, ConstSampler
from jaeger_client.reporter import NullReporter
from jaeger_client.codecs import B3Codec
from opentracing.ext import tags
from opentracing.propagation import Format
from opentracing_instrumentation.request_context import get_current_span, span_in_context
import simplejson as json
import requests
import sys
from json2html import *
import logging
import os
import asyncio

# These two lines enable debugging at httplib level (requests->urllib3->http.client)
# You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# The only thing missing will be the response.body which is not logged.
try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client
http_client.HTTPConnection.debuglevel = 1

app = Flask(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.DEBUG)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

Bootstrap(app)

servicesDomain = "" if (os.environ.get("SERVICES_DOMAIN") is None) else "." + os.environ.get("SERVICES_DOMAIN")
detailsHostname = "details" if (os.environ.get("DETAILS_HOSTNAME") is None) else os.environ.get("DETAILS_HOSTNAME")
ratingsHostname = "ratings" if (os.environ.get("RATINGS_HOSTNAME") is None) else os.environ.get("RATINGS_HOSTNAME")
reviewsHostname = "reviews" if (os.environ.get("REVIEWS_HOSTNAME") is None) else os.environ.get("REVIEWS_HOSTNAME")

flood_factor = 0 if (os.environ.get("FLOOD_FACTOR") is None) else int(os.environ.get("FLOOD_FACTOR"))

details = {
    "name": "http://{0}{1}:9080".format(detailsHostname, servicesDomain),
    "endpoint": "details",
    "children": []
}

ratings = {
    "name": "http://{0}{1}:9080".format(ratingsHostname, servicesDomain),
    "endpoint": "ratings",
    "children": []
}

reviews = {
    "name": "http://{0}{1}:9080".format(reviewsHostname, servicesDomain),
    "endpoint": "reviews",
    "children": [ratings]
}

productpage = {
    "name": "http://{0}{1}:9080".format(detailsHostname, servicesDomain),
    "endpoint": "details",
    "children": [details, reviews]
}

service_dict = {
    "productpage": productpage,
    "details": details,
    "reviews": reviews,
}

# OpenTracing tracer (with null reporter)
tracer = Tracer(
    one_span_per_rpc=True,
    service_name='details',
    reporter=NullReporter(),
    sampler=ConstSampler(decision=True),
    extra_codecs={Format.HTTP_HEADERS: B3Codec()}
)


def trace():
    '''
    Function decorator that creates opentracing span from incoming b3 headers
    '''
    def decorator(f):
        def wrapper(*args, **kwargs):
            request = stack.top.request
            try:
                span_ctx = tracer.extract(
                    Format.HTTP_HEADERS,
                    dict(request.headers)
                )
                rpc_tag = {tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER}
                span = tracer.start_span(
                    operation_name='op', child_of=span_ctx, tags=rpc_tag
                )
            except Exception as e:
                span = tracer.start_span('op')
            with span_in_context(span):
                r = f(*args, **kwargs)
                return r
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator


def getForwardHeaders(request):
    headers = {}

    # x-b3-*** headers can be populated using the opentracing span
    span = get_current_span()
    carrier = {}
    tracer.inject(
        span_context=span.context,
        format=Format.HTTP_HEADERS,
        carrier=carrier)

    headers.update(carrier)

    # We handle other (non x-b3-***) headers manually
    if 'user' in session:
        headers['end-user'] = session['user']

    # Keep this in sync with the headers in details and reviews.
    incoming_headers = [
        'x-request-id',
        'x-ot-span-context',
        'x-datadog-trace-id',
        'x-datadog-parent-id',
        'x-datadog-sampling-priority',
        'traceparent',
        'tracestate',
        'x-cloud-trace-context',
        'grpc-trace-bin',
        'user-agent',
        'cookie',
        'authorization',
        'jwt',
    ]

    for ihdr in incoming_headers:
        val = request.headers.get(ihdr)
        if val is not None:
            headers[ihdr] = val

    return headers


# The UI:
# @app.route('/')
# @app.route('/index.html')
# def index():
#    """ Display productpage with normal user and test user buttons"""
#    global productpage
#
#    table = json2html.convert(json=json.dumps(productpage),
#                              table_attributes="class=\"table table-condensed table-bordered table-hover\"")
#
#    return render_template('index.html', serviceTable=table)


@app.route('/')
def front():
    return [
        {
            'type': 'paperback',
            'pages': '200',
            'publisher': 'PublisherA',
            'language': 'English',
            'ISBN-10': '1234567890',
            'ISBN-13': '123-4567890'
        }
    ]


@app.route('/health')
def health():
    return 'Product page is healthy'


class Writer(object):
    def __init__(self, filename):
        self.file = open(filename, 'w')

    def write(self, data):
        self.file.write(data)

    def flush(self):
        self.file.flush()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        logging.error("usage: %s port" % (sys.argv[0]))
        sys.exit(-1)

    p = int(sys.argv[1])
    logging.info("start at port %s" % (p))
    # Make it compatible with IPv6 if Linux
    if sys.platform == "linux":
        app.run(host='::', port=p, debug=True, threaded=True)
    else:
        app.run(host='0.0.0.0', port=p, debug=True, threaded=True)
