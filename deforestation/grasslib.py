# encoding: utf-8

import os
import sys
import numpy as np

class GRASS():
    def __init__(self, gisbase, dbase, location, mapset='PERMANENT'):

        self.gisbase = os.environ['GISBASE'] = gisbase 
        os.environ['LD_LIBRARY_PATH'] = os.path.join(self.gisbase, 'lib')
        self.dbase = dbase

        self.location = location
        self.mapset = mapset

        # Пока не обновлены пути, импортировать GRASS не удастся
        sys.path.append(os.path.join(os.environ['GISBASE'], "etc", "python"))
        
        import grass.script.setup as gsetup
        self.gsetup = gsetup

        # Активируем GRASS
        self.gsetup.init(self.gisbase,
            self.dbase, self.location, self.mapset)        
        
        # Импортируем полезные модули
        import grass.script as grass
        import grass.script.array as garray
        import grass.pygrass.raster as grs_raster

        self.grass = grass
        self.garray = garray
        self.rast = grs_raster

    def get_region_info(self):
        gregion = self.grass.region()
        return gregion
    
    # def rast_to_array(self, map_name):
    #     """Считывает растр в текущем регионе и возвращает его в виде одной строки numpy.array
    #     """
    #     with self.rast.RasterRow(map_name) as rast:
    #         cols, rows = rast.info.cols, rast.info.rows
    #         dtype = rast[0].dtype
    #         arr = np.empty((rows, cols), dtype)
    #         for i in range(rows):
    #             arr[i] = rast[i]
            
        return np.reshape(arr, rows*cols)
    
    def rast_to_array(self, map_name):
        """Считывает растр в текущем регионе и возвращает его в виде одной строки numpy.array
        """
        arr = self.garray.array()
        arr.read(map_name)
        row, col = arr.shape
        return arr.reshape(row*col)
    
    def array_to_rast(self, arr, map_name, overwrite=None):
        """Сохраняет numpy.array в виде растра на диске
        """
        rast = self.garray.array()
        rast[...] = arr.reshape(rast.shape)
        rast.write(map_name, overwrite=overwrite)
                           

if __name__ == "__main__":
    grs = GRASS(gisbase='/usr/lib/grass70', dbase='/home/cruncher/GRASSDATA', location='FOREST')
    grs.grass.run_command('g.region', flags='p')
