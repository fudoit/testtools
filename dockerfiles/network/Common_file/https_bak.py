#!/usr/bin/env python

# python3
import http.server
import socketserver

# python2
#import SimpleHTTPServer
#import BaseHTTPServer
#import SocketServer

import io
import ssl
#from http import HTTPStatus
import socket
import sys
import json
import requests

proto = []


def get_content(self):
    status = 200

    s = "Host: %s\n" % socket.gethostname()
    s += "Proto: %s\n" % proto
    s += "C->S: %s -> %s\n" % (self.connection.getpeername(), self.connection.getsockname())
    s += "Path: %s\n" % self.path

    s += "  Head:\n"
    for k, v in self.headers.items():
        s += "    %s: %s\n" % (k, v)
        if k.lower() == "httpstatus":
            status = int(v) if v.isdigit() else 400

    l = self.headers.get("L", "")
    if l.isdigit():
        s += "=" * int(l)
        s += "\n"
    
    dict1 = {}
    dict1['host'] = socket.gethostname()
    dict1['proto'] = proto
    dict1['cs'] = (self.connection.getpeername(), self.connection.getsockname())
    dict1['headers']=self.headers.items()
    #agent = self.headers.get("User-Agent", "")
    s = "<html><body><pre>\n%s\n</pre></body></html>\n" % s
    #import pdb;pdb.set_trace()

    return status, s.encode("utf-8"), dict1


def do_GET2(self):
    status, msg, dict1 = get_content(self)
    print(self.headers)
    if 'url_name' in self.headers:
        test_url= self.headers['url_name']
        try:
            r0 = requests.get(test_url)
            access_test = r0.status_code 
            
        except Exception:
            access_test = 'error'
        
        dict1["pc"] = access_test
   
    msg = json.dumps(dict1) 
    self.send_response(status)
    #self.send_header("Content-type", "text/html")
    self.end_headers()
    self.wfile.write(msg.encode('utf-8'))

def run_https(port, handler):
    proto.append("https")
    httpd = http.server.HTTPServer(("", port), handler)
    httpd.socket = ssl.wrap_socket(httpd.socket,
            keyfile="./cert/ssl.key",
            certfile='./cert/ssl.crt',
            ca_certs="./cert/ca.crt",
            ssl_version=ssl.PROTOCOL_SSLv23,
            cert_reqs=ssl.CERT_OPTIONAL,
            #cert_reqs=ssl.CERT_REQUIRED,
            server_side=True)
    print("serving at port", port)
    httpd.serve_forever()

def run_http(port, handler):
    proto.append("http")
    httpd = socketserver.TCPServer(("", port), handler)
    print("serving at port", port)
    httpd.serve_forever()

def main():
    port = 80
    if len(sys.argv) >= 2:
        port = int(sys.argv[1])

    Handler = http.server.SimpleHTTPRequestHandler
    Handler.do_GET = do_GET2

    if "https" in sys.argv[0]:
        run_https(port, Handler)
    else:
        run_http(port, Handler)
main()
