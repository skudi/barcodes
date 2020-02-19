import sys
import os.path
import shutil
import cherrypy
#import barcode
from barcode import generate
from barcode.writer import ImageWriter

config = "../config/app.conf"

class Barcodes(object):
    
    @cherrypy.expose
    def index(self):
        return """<html>
          <head></head>
          <body>
            <form method="get" action="generate">
              <input type="text" value="8" name="length" />
              <button type="submit">Give it now!</button>
            </form>
          </body>
        </html>"""

    @cherrypy.expose
    def generate_ean13(self, code=13):
        cachedir = "%s/%s" % (
                cherrypy.request.app.config['/']['tools.staticdir.root']
                , cherrypy.request.app.config['/cache']['tools.staticdir.dir']
                )
        cachedext = ".svg"
        cachedpath = "%s/%s%s" % (cachedir, code, cachedext) 
        cherrypy.log("generate_ean13(%s) to %s" % (code, cachedpath))
        if ( not os.path.isfile(cachedpath)):
            cachedfullname = generate('EAN13', code, output=cachedpath)
        return 'cache/%s%s' % (code, cachedext)

if __name__ == '__main__':
    cherrypy.quickstart(Barcodes(), '/barcodes', config)

