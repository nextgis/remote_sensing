
unzip -d "TMP" data/roads_prim_02_05.zip
v.import input=TMP/roads_prim_02_05/roads_prim_02_05.shp output=roads_all --o
rm -r TMP
