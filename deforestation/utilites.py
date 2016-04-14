# encoding: utf-8

import os
import tarfile


def get_grassdata_path():
    HOME_DIR = os.getenv("HOME")
    return os.path.join(HOME_DIR, 'GRASSDATA')


def get_location_name():
    return 'LANDSAT'

def get_location_path():
    grass_data = get_grassdata_path()
    locname = get_location_name()
    return os.path.join(grass_data, locname)    


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