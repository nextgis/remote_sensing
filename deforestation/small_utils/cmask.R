library(mgcv) 
library('rgrass7') 
 
args <- commandArgs(trailingOnly = TRUE) 
 
raster = args[1] 
cloud.model.file = args[2] 
snow.model.file = args[3] 
 
cat(raster) 
cat('\n') 
 
load(cloud.model.file) 
load(snow.model.file) 
 
bands = paste(rep('toar_', 11), rep(raster, 11), rep('_B', 11), 1:11, sep='') 
 
execGRASS("g.region", raster=bands[1], flags = "p") 
 
b1 = readRAST(bands[1]) 
b2 = readRAST(bands[2]) 
b3 = readRAST(bands[3]) 
b4 = readRAST(bands[4]) 
b5 = readRAST(bands[5]) 
b6 = readRAST(bands[6]) 
b7 = readRAST(bands[7]) 
 
points = data.frame(b1=as.vector(as.matrix(b1)), b2=as.vector(as.matrix(b2)), b3=as.vector(as.matrix(b3)), b4=as.vector(as.matrix(b
4)), b5=as.vector(as.matrix(b5)), b6=as.vector(as.matrix(b6)), b7=as.vector(as.matrix(b7))) 
 
rm(b1, b2, b3, b4, b5, b6) 
gc() 
 
points$b1[points$b1 > 1] = 1.0 
points$b2[points$b2 > 1] = 1.0 
points$b3[points$b3 > 1] = 1.0 
points$b4[points$b4 > 1] = 1.0 
points$b5[points$b5 > 1] = 1.0 
points$b6[points$b6 > 1] = 1.0 
points$b7[points$b7 > 1] = 1.0 
 
 
points$b1[points$b1 < 0] = 0.0 
points$b2[points$b2 < 0] = 0.0 
points$b3[points$b3 < 0] = 0.0 
points$b4[points$b4 < 0] = 0.0 
points$b5[points$b5 < 0] = 0.0 
points$b6[points$b6 < 0] = 0.0 
points$b7[points$b7 < 0] = 0.0 
 
size = dim(points)[1] 
 
pdata = data.frame(answ1=NA, answ2=NA, answ3=NA, 
 b1=points$b1, b2=points$b2, b3=points$b3, b4=points$b4, b5=points$b5, b6=points$b6, 
 b7=points$b7, b9=NA, b10=NA, b11=NA, scene=NA 
 ) 
 
rm(points) 
gc() 


cat('Predict clouds\n') 
clouds = predict(cloud.model, pdata) 
b7$clouds = as.numeric(clouds) 
writeRAST(b7, paste('clouds', raster, sep='_'), zcol="clouds", overwrite=T) 
rm(clouds) 
gc() 
 
cat('Predict snow\n') 
snow = predict(snow.model, pdata) 
b7$snow = as.numeric(snow) 
writeRAST(b7, paste('snow', raster, sep='_'), zcol="snow", overwrite=T)     