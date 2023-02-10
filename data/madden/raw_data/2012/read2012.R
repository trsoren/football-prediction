library(readxl)

setwd('/Users/trsorensen/Code/EECS448/football/data/madden/raw_data/2012/')

master_ratings = data.frame(matrix(ncol=4, nrow=0))
colnames(master_ratings) = c("year", "team", "position", "overall")
for (fn in list.files('raw')) {
  
  team = read_excel(paste('raw/', fn, sep=''))
  
  team = team[-which(is.na(team$Name)), ]
  team = team[-which(team$Name=='Name'), ]
  
  name = strsplit(fn, "__madden") [[1]][1]
  
  df = data.frame(year=2012, team=name, position=team$Position, overall=team$Overall)
  master_ratings=rbind(master_ratings, df)
}

write.csv(master_ratings, "data2012.csv", row.names=FALSE)