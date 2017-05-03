#!/usr/bin/env python

import hvac
import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            f = open('/run/secrets/vault-token','r')
            try:
                token = f.read().strip()
                print token
                client = hvac.Client(url='http://hashicorp-vault:8200', token=token)
                secret = client.read('secret/strangelove')
                self.write("<launch code>%s</launch_code><br />https://www.youtube.com/watch?v=QSbPqin3L6E" % secret['data']['value'])
            except:
                self.write("Sorry, failed retrieving launch code.")
                print "Unexpected error:", sys.exc_info()[0]
                raise
            finally:
                f.close()
        except:
            self.write("Sorry, missing vault token.")


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
