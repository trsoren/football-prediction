library(readxl)


master_ratings = data.frame(matrix(ncol=4, nrow=0))
colnames(master_ratings) = c("year", "team", "position", "overall")
setwd("/Users/grantsasina/desktop/eecs_448/football-prediction/data/madden/raw_data/2017/raw")
for (fn in list.files()) {
  
  team = read_excel(fn)
  name = strsplit(fn, "__madden") [[1]][1]
  
  df = data.frame(year=2017, team=name, position = team$Position, overall=team$Overall)
  
  master_ratings=rbind(master_ratings, df)
}

write.csv(master_ratings, "data2017.csv", row.names=FALSE)
