#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import csv

from collections import namedtuple

from uuid import uuid4

import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Create raster for cost of woods.')

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


def create_factor(gscript, wood_types, costs, function, result):
    prefix = 'tmp' + uuid4().hex
    try:
        res = []
        for w_t in wood_types:
            name = prefix + w_t + 't'
            value = costs[w_t]
            res.append(name)
            
            expression = "%s = float(%s) %s float(%s)" % (name, value, function, w_t)
            gscript.run_command('r.mapcalc', expression=expression)

        gscript.run_command('r.patch', input=','.join(res), output=result)
    finally:
        gscript.run_command('g.remove', type='rast', pattern=prefix+'*', flags='f')


def main():
    args = parse_args()
    args = vars(args)

    overwrite = args['overwrite']
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
    
    costs = dict(costs)

    try:
        wood_types = ['forest_spec_dub', 'forest_spec_jasen', 'forest_spec_kedr', 'forest_spec_lipa', 'forest_background']
        wood_type_cost = prefix + '_wtc'
        create_factor(gscript, wood_types, costs, '*', wood_type_cost)
            
        wood_bon = ['forest_dub_bon', 'forest_jasen_bon', 'forest_kedr_bon', 'forest_lipa_bon', 'forest_background']
        wood_bon_cost = prefix + '_wbc'
        create_factor(gscript, wood_bon, costs, '/', wood_bon_cost)
        
        wood_d = ['forest_dub_d1', 'forest_jasen_d1', 'forest_kedr_d1', 'forest_lipa_d1', 'forest_background']
        wood_d_cost = prefix + '_wdc'
        create_factor(gscript, wood_d, costs, '*', wood_d_cost)

        wood_h = ['forest_dub_h1', 'forest_jasen_h1', 'forest_kedr_h1', 'forest_lipa_h1', 'forest_background']
        wood_h_cost = prefix + '_whc'
        create_factor(gscript, wood_h, costs, '*', wood_h_cost)
        
        wood_a = ['forest_dub_amz1', 'forest_jasen_amz1', 'forest_kedr_amz1', 'forest_lipa_amz1', 'forest_background']
        wood_a_cost = prefix + '_wac'
        create_factor(gscript, wood_a, costs, '*', wood_a_cost)

        # *(1 + psp_cost): +1 т.к. psp_cost может быть равна нулю, не хочу обнулять слагаемые во втором множителе
        expression = "{res} = ({type_cost} + {bon_cost} + {h_cost} + {d_cost} + {a_cost})*(1 + {psp_cost}*if(isnull(forest_psp1), 0, forest_psp1))".format(
            res=result,
            type_cost=wood_type_cost, bon_cost=wood_bon_cost, 
            h_cost=wood_h_cost, d_cost=wood_d_cost, a_cost=wood_a_cost, 
            psp_cost=costs['forest_psp1']
        )
        gscript.run_command('r.mapcalc', expression=expression, overwrite=True)

    finally:
        gscript.run_command('g.remove', type='rast', pattern=prefix+'*', flags='f')
    
    


if __name__ == '__main__':
    main()

