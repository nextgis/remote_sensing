

RASTER=$1
RESULT_NAME=$2

GROUP_NAME=temp_group_$$
TEMP_RAST0=temp_rast0_$$
TEMP_RAST1=temp_rast1_$$
TEMP_RAST2=temp_rast2_$$

TEMP_REGION_FILE=tmp_region_$$

g.region save=$TEMP_REGION_FILE

g.region rast=$RASTER

# Создадим нелинейные отображения для того, чтобы получить не серый RGB-композит из одноканального растра
r.mapcalc "${TEMP_RAST0} = $RASTER" 
r.mapcalc "${TEMP_RAST1} = sqrt($RASTER)" 
r.mapcalc "${TEMP_RAST2} = $RASTER * log($RASTER + 1)" 

# r.mapcalc "${TEMP_RAST1} = int($RASTER - log($RASTER + 1))" 
# r.mapcalc "${TEMP_RAST2} = int(500/($RASTER + 100))" 

# Приведем все к байтовому диапазону
for MAP in ${TEMP_RAST0} ${TEMP_RAST1} ${TEMP_RAST2}
do
  RANGE=$(r.info -r $MAP)
  eval $RANGE
  r.mapcalc expression="$MAP = int(254 * ($MAP - $min)/($max-$min))" --o
done

i.group group=$GROUP_NAME subgroup=all input=${TEMP_RAST0},${TEMP_RAST1},${TEMP_RAST2}
r.out.gdal ${GROUP_NAME} out=${RESULT_NAME} createopt="COMPRESS=DEFLATE"  type=Byte -f --o

g.region region=$TEMP_REGION_FILE


g.remove type=rast name=${TEMP_RAST0} -f
g.remove type=rast name=${TEMP_RAST1} -f
g.remove type=rast name=${TEMP_RAST2} -f
g.remove type=group name=${GROUP_NAME} -f

g.remove type=region name="$TEMP_REGION_FILE" -f

