# encoding: utf-8

import os
import sys

import uuid

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response

from grasslib import GRASS

from utilites import (
    get_grassdata_path,
    get_location_name,
    get_location_path,
)

grs = GRASS(gisbase='/usr/lib/grass70', 
    dbase=get_grassdata_path(), 
    location=get_location_name()
)

def _grass_wms(layers=[], bbox=[], width=256, height=256):
    # Получаем список известных растровых и векторных слоев
    vector_layers = grs.grass.list_strings(type="vect")
    raster_layers = grs.grass.list_strings(type="rast")
   
    print 'sdfgdfg'
    grs.grass.run_command("g.region", w=bbox[0], s=bbox[1], e=bbox[2], n=bbox[3])
    print '1sdfgdfg'

    # Настраиваем параметры вывода
    filename = uuid.uuid4().hex + '.png'
    os.environ["GRASS_CAIROFILE"] = filename
    os.environ["GRASS_WIDTH"] = width
    os.environ["GRASS_HEIGHT"] = height
    print '2sdfgdfg'

    # Отрисовка
    grs.grass.run_command("d.mon", output=filename, start="cairo")

    for layer in layers:
        if layer in raster_layers:
            grs.grass.run_command("d.rast", map=layer, quiet=1)
        elif layer in vector_layers:
            grs.grass.run_command("d.vect", map=layer, quiet=1, fcolor="0:0:255", color=None)

    grs.grass.run_command("d.mon", stop="cairo")


    return filename

@view_config(route_name="wms")
def wms_view(request):

    layers = request.params.get("LAYERS", "").split(",")
    bbox = request.params.get("BBOX", "").split(",")
    width = request.params.get("WIDTH")
    height = request.params.get("HEIGHT")

    try:
        filename = _grass_wms(layers=layers,
                             bbox=bbox,
                             width=width,
                             height=height)
        f = open(filename, "r+")
        body = f.read()
        f.close()
    except:
        raise
    finally:
        os.unlink(filename)

    return Response(body=body, content_type="image/png")

@view_config(route_name="index")
def index_view(request):
    body = """
    <html xml:lang="en"
    xmlns:tal="http://xml.zope.org/namespaces/tal"
    xmlns="http://www.w3.org/1999/xhtml">
    <head>
     <title>GRASS GIS Web Map Service</title>
     <script src="http://openlayers.org/api/OpenLayers.js" type="text/javascript"></script>
     <script type="text/javascript">
       var map, wms_layer;
       function init(){
           var map = new OpenLayers.Map("map-div",{
               projection: "EPSG:32653",
               maxExtent: new OpenLayers.Bounds(419602, 4999818, 743949, 5320904),
               numZoomLevels: 18,
           });
           var wms_layer = new OpenLayers.Layer.WMS("GRASS WMS", '/wms', {
               layers: "toar_LC81120272015365LGN00_B2@PERMANENT"
           },{
               singleTile: true,
           });
           map.addLayer(wms_layer);
           map.zoomToMaxExtent();
       }
     </script>
    </head>
    <body onload="init()">
       <div id="map-div" style="height: 600px; width: 800px;"></div>
    </body>
    </html>"""
    return Response(body=body, content_type="text/html", status=200)

def main():
    """ Данная функция возвращает WSGI-приложение Pyramid.
    """
    config = Configurator()
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route("index", '/')
    config.add_route("wms", '/wms')
    config.scan()
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()


main()
