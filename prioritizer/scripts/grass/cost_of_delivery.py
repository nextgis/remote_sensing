#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import csv

from collections import namedtuple

from uuid import uuid4

import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Create raster for cost of delivery.')

    parser.add_argument(
        '--result',
        dest='result',
        action='store',
        default='-',
        help='Name of result raster to store cost.'
    )
    parser.add_argument(
        '--cost_data',
        dest='costs_data',
        action='store',
        required=True,
        help='Name of costs data file.'
    )
    parser.add_argument(
        '--stocks',
        dest='stocks',
        action='store',
        required=True,
        help='Raster with stock areas.'
    )
    parser.add_argument(
        '--overwrite',
        dest='overwrite',
        action='store_const',
        const=True,
        default=False,
        help='Overwrite existing result file (True or False).'
    )
    parser.add_argument(
        '--separator',
        dest='separator',
        action='store',
        default=':',
        help='Separator between raster names and their costs.'
    )
    args = parser.parse_args()

    return args


def setup_grass():
    # define GRASS-Python environment
    gisbase = os.environ['GISBASE']
    grassdata = os.environ['GRASSDATA']
    location = os.environ['LOCATION']
    mapset = os.environ['MAPSET']
    
    gpydir = os.path.join(gisbase, "etc", "python")
    sys.path.append(gpydir)
    
    import grass.script as gscript
    import grass.script.setup as gsetup
    gsetup.init(gisbase, grassdata, location, mapset)
    
    return gscript


def main():
    args = parse_args()
    args = vars(args)

    overwrite = args['overwrite']
    stocks = args['stocks']
    result = args['result']
    separator = args['separator']

    costs_data = args['costs_data']
    if costs_data == '-':
        costs_data = sys.stdin
    else:
        costs_data = open(costs_data, 'r')

    reader = csv.reader(costs_data, delimiter=separator)
    
    Raster_cost = namedtuple('RasterCost', ['raster', 'cost'])
    
    costs = []
    for row in reader:
        try:
            new_cost = Raster_cost._make(row)
        except TypeError:
            raise TypeError('Input data must be in foramat "raster_name:cost_value"')
        
        try:
            float(new_cost.cost)
        except:
            raise ValueError('Cost must be a number, but recieved %s' % (new_cost, ))
        costs.append(new_cost)

    gscript = setup_grass()
    
    prefix = 'tmp' + uuid4().hex
    names = []
    for c in costs:
        name = prefix + c.raster
        value = c.cost
        names.append(name)
        
        expression = "%s = %s * %s" % (name, value, c.raster)
        gscript.run_command('r.mapcalc', expression=expression)
    
    walking_cost = prefix + '_walking'
    gscript.run_command('r.patch', input=','.join(names), output=walking_cost)
    gscript.run_command('r.cost', input=walking_cost, output=result, start_raster=stocks, overwrite=overwrite)
    
    gscript.run_command('g.remove', type='rast', pattern=prefix+'*', flags='f')
    
    


if __name__ == '__main__':
    main()

