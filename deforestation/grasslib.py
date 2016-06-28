# encoding: utf-8

import os
import sys

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
        import grass.pygrass.raster as grs_raster

        self.grass = grass
        self.r = grs_raster

    def get_region_info(self):
        gregion = self.grass.region()
        return gregion


if __name__ == "__main__":
    grs = GRASS(gisbase='/usr/lib/grass70', dbase='/home/cruncher/GRASSDATA', location='FOREST')
    grs.grass.run_command('g.region', flags='p')
