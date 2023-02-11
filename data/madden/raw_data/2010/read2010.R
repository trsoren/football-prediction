library(readxl)

setwd('~/Desktop/eecs_448/football-prediction/data/madden/raw_data/2010/raw')

master_ratings = data.frame(matrix(ncol=4, nrow=0))
colnames(master_ratings) = c("year", "team", "position", "overall")
for (fn in list.files()) {
  
  team = read_excel(fn)
  name = strsplit(fn, "__madden") [[1]][1]
  
  
  team$Position
  df = data.frame(year=2010, team=name, position = team$POS, overall= team$OVR)
  master_ratings=rbind(master_ratings, df)
}

write.csv(master_ratings, "data2010.csv", row.names=FALSE)