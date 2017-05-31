from prioretizer.grasslib.grasslib import GRASS
from prioretizer.grasslib.configurator import Params


def get_grass(config):
    config_params = Params(config)

    grass_lib = config_params.grass_lib
    grass_exec = config_params.grass_exec

    location = config_params.location
    dbase = config_params.grassdata

    grass = GRASS(
        gisexec=grass_exec,
        gisbase=grass_lib,
        grassdata=dbase,
        location=location,
        init_loc=True
    )
    return grass
