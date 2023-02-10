library(readxl)

setwd('/Users/trsorensen/Code/EECS448/football/data/madden/raw_data/2009/raw')

master_ratings = data.frame(matrix(ncol=4, nrow=0))
colnames(master_ratings) = c("year", "team", "position", "overall")
for (fn in list.files()) {
  
  team = read_excel(fn)
  name = strsplit(fn, "_madden") [[1]][1]
  
  
  team$Position
  df = data.frame(year=2009, team=name, position = team$Position, overall= team$OVERALL)
  master_ratings=rbind(master_ratings, df)
}
  
write.csv(master_ratings, "data2009.csv", row.names=FALSE)