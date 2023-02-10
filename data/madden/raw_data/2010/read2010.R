library(readxl)

setwd('/Users/trsorensen/Code/EECS448/football/data/madden/raw_data/')

master_ratings = data.frame(matrix(ncol=4, nrow=0))
colnames(master_ratings) = c("year", "team", "position", "overall")
for (fn in list.files('d2010')) {
  
  team = read_excel(paste('d2010/', fn, sep=''))
  name = strsplit(fn, "__madden") [[1]][1]
  
  team$Position
  df = data.frame(year=2010, team=name, position=team$POS, overall=team$OVR)
  master_ratings=rbind(master_ratings, df)
}
  
write.csv(master_ratings, "data2010.csv", row.names=FALSE)