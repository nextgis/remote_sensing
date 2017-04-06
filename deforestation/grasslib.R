#!/usr/bin/Rscript

get_gisbase_path = function(){
    return ('/usr/lib/grass72')
}

get_grassdata_path = function(){
    HOME_DIR = Sys.getenv("HOME")
    return (file.path("", HOME_DIR, "GRASSDATA"))
}


get_location_name = function(){
    return ('FOREST')
}

get_ll_location_name = function(){
    return ('LatLon')
}

get_location_path = function(){
    grass_data = get_grassdata_path()
    locname = get_location_name()
    return (file.path(grass_data, locname))
}



# library(rgrass7)

# # initialisation and the use of North Carolina sample dataset
# initGRASS(gisBase = get_gisbase_path(), home = tempdir(), 
          # gisDbase = get_grassdata_path(),
          # location = get_location_name(), mapset = "PERMANENT")

# system("g.region -p")

