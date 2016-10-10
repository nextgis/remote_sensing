#!/usr/bin/env python
# -*- coding: utf-8  -*-

#%Module
#% description: Create circle sectors by coordinates of the circle center and two angles which are the borders of the sector.
#%End
#%option
#% key: input_file
#% type: string
#% description: prefix of the input raster maps (e.g. clean.LC81120272015333LGN00)
#% required : yes
#% multiple: yes
#%end
#%option
#% key: band_prefix
#% type: string
#% description: band name (e.g. _B3) 
#% required : yes
#% multiple: yes
#%end
#%option
#% key: rast_prefix
#% type: string
#% description: prefix for cleaned raster maps
#% required : yes
#% multiple: yes
#%end
#%option
#% key: output
#% type: string
#% description: prefix of the output vector map name
#% required : yes
#% multiple: no
#%end
#%option
#% key: method
#% type: string
#% description: aggregation method 
#% required : yes
#% multiple: no
#%end


import os, sys

if "GISBASE" not in os.environ:
    print "You must be in GRASS GIS to run this program."
    sys.exit(1)

import grass.script as grass


def main(options, flags):
    in_file = options['input_file']
    band = options['band_prefix']
    rast_prefix = options['rast_prefix']
    out_map = options['output']
    method = options['method']

    with open(in_file) as f:
        in_maps = f.read()

    in_maps = [rast_prefix + name + band for name in in_maps.split()]
    grass.run_command('g.region', raster=in_maps[0])

    in_maps = ','.join(in_maps)

    grass.run_command('r.series', input=in_maps, method=method, output=out_map, overwrite=grass.overwrite())



if __name__ == "__main__":
    options, flags = grass.parser()
    main(options, flags)
    sys.exit(0)
                                                                                                                                
