# encoding: utf-8

import os
import sys
import uuid
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
    
    def raster_to_array(self, map_name):
        """Считывает растр в текущем регионе и возвращает его в виде одной строки numpy.array
        """              
        arr = self.garray.array(map_name, null=np.nan, dtype=np.double)
            
        return np.reshape(arr, -1)
    
    def rasters_to_array(self, maps):
        """Считывает список растров и возвращает их в виде двумерного numpy.array
        (каждый растр в отдельном столбце)
        """
        rows = self.get_region_info()['cells']
        cols = len(maps)
        
        # Наверное, есть способ узнать тип карты проще, чем этот
        rast = self.raster_to_array(maps[0])
        dtype = rast.dtype
        
        arr = np.empty((rows, cols), dtype)
    
        arr[:, 0] = rast
        for i in range(1, cols):
            rast = self.raster_to_array(maps[i])
            arr[:, i] = rast
            
        return arr
    
    def array_to_rast(self, arr, map_name, overwrite=None):
        """Сохраняет numpy.array в виде растра на диске
        """
        rast = self.garray.array()
        rast[...] = arr.reshape(rast.shape)
        rast.write(map_name, overwrite=overwrite)
        
    def copy_metadata_from_rast(self, copy_from, copy_to):
        """Копирует метаданные (r.support) из растра copy_from
        в растр copy_to.
        """
        # Временный файл: 
        tempfile = uuid.uuid4().hex

        try:
            self.grass.run_command('r.support', map=copy_from, savehistory=tempfile)
            self.grass.run_command('r.support', map=copy_to, loadhistory=tempfile)
        finally:
            os.unlink(tempfile)
                           

if __name__ == "__main__":
    grs = GRASS(gisbase='/usr/lib/grass72', dbase='/home/cruncher/GRASSDATA', location='FOREST')
    grs.grass.run_command('g.region', flags='p')
