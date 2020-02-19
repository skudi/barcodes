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
    def index(self, codes="", noform="off"):
        doc=""
        form=""
        if (codes):
            for namecode in codes.split():
                name, code = namecode.split(",")
                doc += """<tr><td class="name">%s</td><td class="barcode"><img src="%s" /></td></tr>""" % (name, self.prepare_image(code))
            doc = """<table>%s</table>""" % (doc)
        if (noform == "off"):
            form= """
                <form method="get" action="">
                  <textarea name="codes" rows="20" cols="50"/>%s</textarea>
                  <br />
                  <input type="checkbox" name="noform" />Do wydruku
                  <br />
                  <button type="submit">Generator</button>
                </form>
            """ % (codes)
        return """<html>
          <head>
          <style>
            td.barcode {text-align: right;}
            td.name {text-align: left;}
          </style>
          </head>
          <body>%s%s
          </body>
        </html>""" % (form, doc)

    def prepare_image(self, code):
        cherrypy.log("prepare_image(%s[%d])" % (code, len(code)))
        if (len(code) > 12):
            return self.generate_barcode(code, "EAN13")
        else:
            return self.generate_barcode(code, "CODE128")
        return ""

    def generate_barcode(self, code, codeformat):
        cachedir = "%s/%s" % (
                cherrypy.request.app.config['/']['tools.staticdir.root']
                , cherrypy.request.app.config['/cache']['tools.staticdir.dir']
                )
        cachedext = ".svg"
        cachedpath = "%s/%s" % (cachedir, code) 
        cachedpathwithext = "%s%s" % (cachedpath, cachedext) 
        cherrypy.log("generate_barcode(%s) to %s" % (code, cachedpath))
        if ( not os.path.isfile(cachedpathwithext)):
            cachedfullname = generate(codeformat, code, output=cachedpath)
        return 'cache/%s%s' % (code, cachedext)

if __name__ == '__main__':
    cherrypy.quickstart(Barcodes(), '/barcodes', config)

