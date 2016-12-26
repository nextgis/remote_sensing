# encoding: utf-8

import os
import datetime
import tarfile


def get_grassdata_path():
    HOME_DIR = os.getenv("HOME")
    return os.path.join(HOME_DIR, 'GRASSDATA')


def get_location_name():
    return 'FOREST'

def get_ll_location_name():
    return 'LatLon'

def get_location_path():
    grass_data = get_grassdata_path()
    locname = get_location_name()
    return os.path.join(grass_data, locname)


def rm_grass_lock(mapset):
    """Удалить lock-файл для заданного mapset (очистка мусора после некорректного завершения).
    (использовать с осторожностью, только если есть уверенность, что данный мапсет не используется!)
    """
    filename = os.path.join(get_location_path(), mapset, '.gislock')
    if os.path.isfile(filename):
        os.remove(filename)

def unpack(data_file, extract_dir):
    try:
        a = tarfile.open(data_file)
        a.extractall(path=extract_dir)
        a.close()
    except IOError:
        return False

    return True


def filename_to_bandname(geofilename):
    """
    Extract from Landsat geotif file the number of the band
    """
    geofilename = os.path.basename(geofilename)
    j = geofilename.rindex('.')
        
    return geofilename[:j]


def find_meta(dirname):
    """
    Find metadata file for the scene
    :param dirname:     directory name of unpacked Landsat scene
    :return:    path to the metadata file
    """
    file_list = [f for f in os.listdir(dirname)
                 if os.path.isfile(os.path.join(dirname, f))]
    file_list = [os.path.join(dirname, f) for f in file_list if f.endswith('_MTL.txt')]
    if len(file_list) != 1:
        raise ValueError('Unknown format of Landsat archive')

    return file_list[0]


def get_raster_list(dirname):
    file_list = [f for f in os.listdir(dirname)
                 if os.path.isfile(os.path.join(dirname, f))]
    file_list = [os.path.join(dirname, f) for f in file_list if f.endswith('.TIF')]

    return file_list

def format_timestamp(year, day):
    """Return timestump in GRASS GIS format
    """
    date = datetime.datetime(year, 1, 1) + datetime.timedelta(day)
    stamp = date.strftime('%-d %b %Y').lower()
    return stamp

def get_wms_link(map, x1,y1,x2,y2, server_address="http://176.9.38.120/cruncher_wms/wms/", w=300, h=300):
    """Вспомогательная функция, возвращает ссылку на кусок растра 
    (с названием map), в BBOX (x1,y1,x2,y2) для получения по wms
    
    Например:
        передав параметры ("toar_LC81120282015237LGN00_B5@landsat", 516684, 5098286, 543339, 5113090), получим:
        http://176.9.38.120/cruncher_wms/wms/landsat/?SERVICE=WMS&REQUEST=GetMap&BBOX=516684,5098286,543339,5113090&WIDTH=300&HEIGHT=300&LAYERS=toar_LC81120282015237LGN00_B5@landsat
        
    """
    mapset = map.split('@')[1]
    address = server_address + mapset + '/?SERVICE=WMS&REQUEST=GetMap'
    
    bbox = 'BBOX=' + ','.join([str(x1), str(y1), str(x2), str(y2)])
    w = "WIDTH=" + str(w)
    h = "HEIGHT=" + str(h)
    layers = "LAYERS=" + map
    
    address = '&'.join([address, bbox, w, h, layers])
    
    return address