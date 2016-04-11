# encoding: utf-8

import os
import sys

class GRASS():
    def __init__(self, gisbase, dbase, location, mapset='PERMANENT'):

        self.gisbase = os.environ['GISBASE'] = gisbase
        self.dbase = dbase

        self.location = location
        self.mapset = mapset

        # Пока не обновлены пути, импортировать GRASS не удастся
        sys.path.append(os.path.join(os.environ['GISBASE'], "etc", "python"))
        
        import grass.script as grass
        import grass.script.setup as gsetup

        self.grass = grass
        self.gsetup = gsetup

        # Активируем GRASS
        self.gsetup.init(self.gisbase,
            self.dbase, self.location, self.mapset)

    def get_region_info(self):
        gregion = self.grass.region()
        return gregion


if __name__ == "__main__":
    grs = GRASS(gisbase='/usr/lib/grass70', dbase='/home/dima/GRASSDATA', location='AML')
    grs.grass.run_command('g.region', flags='p')
