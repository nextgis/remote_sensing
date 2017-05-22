
# Импорт выделов
unzip -d "TMP" data/vud.zip

export SHAPE_ENCODING=CP1251
v.import input=TMP/vud_all.shp output=vud_all --o
unset SHAPE_ENCODING

rm -r TMP
