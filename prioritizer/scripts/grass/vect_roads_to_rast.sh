
set -e


# asfalt - шоссе и усовершенств. шоссе
# good grunt - улучш. грунтовые
# grunt - грунтовые
# land  - полевые и лесные
# other - зимники и навесные дороги
# trop - тропы (?)


for TYPE in asfalt "good grunt" grunt land other trop
do
    MAP_NAME=$(echo $TYPE | tr " " "_")
    MAP_NAME=roads_$MAP_NAME
    v.to.rast type=line input=roads_all output=$MAP_NAME where="typ_all=\"${TYPE}\"" use=val --o
done
