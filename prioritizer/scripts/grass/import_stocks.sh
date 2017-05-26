
unzip -d "TMP" data/wood_stocks.zip
v.import input=TMP/wood_stocks.shp output=wood_stocks --o
rm -r TMP
