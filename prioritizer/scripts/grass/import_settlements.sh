
unzip -d "TMP" data/settlements.zip
v.import input=TMP/settlements.shp output=settlements --o
rm -r TMP
