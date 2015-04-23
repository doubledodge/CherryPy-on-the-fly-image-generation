# -*- coding: utf-8 -*-
"""
Created  Apr 09 14:02:22 2015
Scope image server adapted from Cherry Py Tutorial 4
http://docs.cherrypy.org/en/latest/tutorials.html#tutorials
Go to http://localhost:8080/ in your browser to view the web page
This version tests serving a python generated image, the
image is generated by visiting http://localhost:8080/trace
@author: doubledodge
#    Copyright (C) 2015  Bob Anderson
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""


import os, os.path
import cherrypy
import StringIO
from PIL import Image

class BobTrial(object):
    @cherrypy.expose
    def index(self):
        return """<html>
          <head>CherryPy on the fly image server</head>
          <body>
          <div style="background-color:#efffcc">
          <img  src="checks" >
          <p>The image above was generated in response to the browser get request</p>
          </div>
          </body>
        </html>"""
    @cherrypy.expose
    def checks(self):
        sqSize=50 # checkerboard square size in pixels
        nSquares=8 # number of EVEN rows and columns of the checkerboard
        # create a black backround image
        img=Image.new('1',(nSquares*sqSize,nSquares*sqSize))
        # add white squares in checkerboard fashion
        for i in range (nSquares/2): # row pair offset
            for j in range (2): # row 2-step
                for k in range (nSquares/2): # column step
                    x1=(2*k+j)*sqSize
                    y1=(j+i*2)*sqSize
                    img.paste(1,((2*k+j)*sqSize,(j+i*2)*sqSize,x1+sqSize,y1+sqSize))
        cherrypy.response.headers['Content-Type'] = "image/png"
        # use StringIO to stream the image out to the browser direct from RAM
        output = StringIO.StringIO()
        format = 'PNG' # JPEG and other formats are available
        img.save(output, format)
        contents = output.getvalue()
        output.close()
        return contents
if __name__ == '__main__':
     conf = {
         '/': {
             'tools.sessions.on': True,
             'tools.staticdir.root': os.path.abspath(os.getcwd())
         },
         '/static': {
             'tools.staticdir.on': True,
             'tools.staticdir.dir': './public'
         }
     }
     cherrypy.quickstart(BobTrial(),'/', conf)
    
