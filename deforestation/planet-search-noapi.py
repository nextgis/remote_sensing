from planet import api
from osgeo import ogr
from osgeo import osr

client = api.Client('ADD-API-KEY-HERE')

input_shape = '/media/sim/Windows7_OS/work/ALARM/trainings2016/training2015-2016_winter.shp'

#get features
driver = ogr.GetDriverByName("ESRI Shapefile")
dataSource = driver.Open(input_shape, 0)
layer = dataSource.GetLayer()
source_srs = layer.GetSpatialRef()
callback = api.write_to_file('/media/sim/Windows7_OS/work/ALARM/trainings2016/downloads')

target_srs = osr.SpatialReference()
target_srs.ImportFromEPSG(4326)
transform = osr.CoordinateTransformation(source_srs, target_srs)

ids = []
for f in layer:
    #get feature's WKT geometry
    geom = f.GetGeometryRef()
    geom.Transform(transform)
    f_wkt = geom.ExportToWkt()

    scenes = client.get_scenes_list(scene_type='ortho', intersects=f_wkt)
    for scene in scenes.get()['features']:
        if scene['id'] not in ids:
            bodies = client.fetch_scene_geotiffs([scene['id']], callback=callback)
            for b in bodies:
                b.await()
                ids.append(scene['id'])
                print('Downloaded ' + scene['id'] + '\n')