
unzip -d "TMP" data/roads_prim_02_05.zip
v.import input=TMP/roads_prim_02_05/roads_prim_02_05.shp output=roads_all_prim --o

unzip -d "TMP" data/roads_chab_13_05.zip
ls TMP/*
v.import input=TMP/roads_chab_13_05/roads_chab.shp output=roads_all_chab --o

v.patch -e input=roads_all_prim,roads_all_chab out=roads_all --o

g.remove vect name=roads_all_chab -f
g.remove vect name=roads_all_prim -f


rm -r TMP
