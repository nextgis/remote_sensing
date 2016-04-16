# encoding: utf-8

import os
import sys

import uuid

from lxml import etree
from lxml.builder import ElementMaker

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPBadRequest

from grasslib import GRASS

from utilites import (
    get_grassdata_path,
    get_location_name,
    get_location_path,
)


NS_XLINK = 'http://www.w3.org/1999/xlink'


# Общий GRASS на все запросы. Возможны проблемы при 
# одновременном использовании с разными MAPSET'ами
grs = GRASS(gisbase='/usr/lib/grass70', 
    dbase=get_grassdata_path(), 
    location=get_location_name()
)


def _grass_wms(layers=[], bbox=[], width=256, height=256):   
    minx, miny, maxx, maxy = bbox[0], bbox[1], bbox[2], bbox[3]
    grs.grass.run_command("g.region", w=minx, s=miny, e=maxx, n=maxy)

    # Настраиваем параметры вывода
    filename = uuid.uuid4().hex + '.png'
    os.environ["GRASS_CAIROFILE"] = filename
    os.environ["GRASS_WIDTH"] = width
    os.environ["GRASS_HEIGHT"] = height
    os.environ["GRASS_RENDER_TRANSPARENT"] = "TRUE"

    # Отрисовка
    grs.grass.run_command("d.mon", 
                          output=filename, 
                          width=width,
                          height=height,
                          start="png")

    for layer in layers:
        grs.grass.run_command("d.rast", map=layer, quiet=1, flags='n')

    grs.grass.run_command("d.mon", stop="png")

    return filename


@view_config(route_name="wms")
def wms_view(request):
    
    mapset = request.matchdict['mapset']
    mapsets = grs.grass.read_command('g.mapset', flags='l').split()
    
    if mapset not in mapsets:
        raise HTTPBadRequest("Invalid MAPSET name.")
    
    params = dict((k.upper(), v) for k, v in request.params.iteritems())
    
    
    req = params.get('REQUEST')
    service = params.get('SERVICE')
    
    if req == 'GetCapabilities':
        if service != 'WMS':
            raise HTTPBadRequest("Invalid SERVICE parameter value.")
        return _get_capabilities(request)
    elif req == 'GetMap':
        return _get_map(params)
    else:
        raise HTTPBadRequest("Invalid REQUEST parameter value.")

        
def _get_map(params):
    layers = params.get("LAYERS", "").split(",")
    bbox = params.get("BBOX", "").split(",")
    width = params.get("WIDTH")
    height = params.get("HEIGHT")
    
    filename = None

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
        if filename is not None:
            os.unlink(filename)

    return Response(body=body, content_type="image/png")

        
def _get_capabilities(request):
    E = ElementMaker(nsmap=dict(xlink=NS_XLINK))
    
    OnlineResource = lambda: E.OnlineResource({
        '{%s}type' % NS_XLINK: 'simple',
        '{%s}href' % NS_XLINK: request.path_url})
    
    DCPType = lambda: E.DCPType(E.HTTP(E.Get(OnlineResource())))
    
    service = E.Service(
        E.Name(None or 'WMS'),
        E.Title('SDFSDF'),
        E.Abstract('sdf' or ''),
        OnlineResource()
    )
    
    capability = E.Capability(
        E.Request(
            E.GetCapabilities(
                E.Format('text/xml'),
                DCPType()),
            E.GetMap(
                E.Format('image/png'),
                E.Format('image/jpeg'),
                DCPType()),
        ),
        E.Exception(E.Format('text/xml'))
    )
    
    layer = E.Layer(
        E.Title('sdgdfsgsfg'),
        E.LatLonBoundingBox(dict(
            minx="90.0", miny="20.0",
            maxx="180.0", maxy="85.0"))
    )
    
    mapset = request.matchdict['mapset']
    raster_layers = grs.grass.list_strings(type="rast")
    if mapset != 'PERMANENT':
        raster_layers += grs.grass.list_strings(type="rast", mapset=mapset)
    for l in raster_layers:
        lnode = E.Layer(
            dict(queryable='0'),
            E.Name(l),
            E.Title(l))

        lnode.append(E.SRS('EPSG:32653'))

        layer.append(lnode)

    capability.append(layer)
    
    xml = E.WMT_MS_Capabilities(
        dict(version='1.1.1'),
        service, capability)

    return Response(
        etree.tostring(xml, encoding='utf-8'),
        content_type=b'text/xml')

        
@view_config(route_name="index")
def index_view(request):
    body = _default_wms_body()
    return Response(body=body, content_type="text/html", status=200)


def _default_wms_body(layers=None):
    if layers is None:
        layers = 'toar_LC81120272015365LGN00_B2@PERMANENT'
    
    body = body = """
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
           var wms_layer = new OpenLayers.Layer.WMS("GRASS WMS", '/cruncher_wms/wms', {
               layers: "%s"
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
    </html>""" % (layers, )
    
    return body

def main():
    """ Данная функция возвращает WSGI-приложение Pyramid.
    """
    config = Configurator()
    config.add_static_view('static', 'static', cache_max_age=3600)
    
    config.add_route("index", '/')
    config.add_route("wms", '/wms/{mapset}/')
    
    config.scan()
    
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()


if __name__ == "__main__":
    main()
