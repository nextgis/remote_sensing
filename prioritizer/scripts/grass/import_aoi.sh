unzip -d "TMP" data/aoi.zip
v.import input=TMP/AOI.shp output=AOI --o
rm -r TMP
