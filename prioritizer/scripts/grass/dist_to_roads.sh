
set -e

COST_MAP=tmp_cost_map
COST_VALUE=$(g.region -g | grep nsres | cut -d= -f2)

r.mapcalc expression="$COST_MAP = $COST_VALUE"

for IN_MAP in asfalt good_grunt grunt land other trop
do
    OUT_MAP=dist_$IN_MAP
    r.cost input=$COST_MAP output=$OUT_MAP start_raster=roads_$IN_MAP --o
done

g.remove type=rast name=$COST_MAP -f
