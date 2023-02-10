library(readxl)

setwd('/Users/trsorensen/Code/EECS448/football/data/madden/raw_data/2016/')

master_ratings = data.frame(matrix(ncol=4, nrow=0))
colnames(master_ratings) = c("year", "team", "position", "overall")
for (fn in list.files('raw')) {
  
  team = read_excel(paste('raw/', fn, sep=''))
  
  name = strsplit(fn, "_\\(madden") [[1]][1]
  
  df = data.frame(year=2016, team=name, position=team$Position, overall=team$OVR)
  master_ratings=rbind(master_ratings, df)
}

write.csv(master_ratings, "data2016.csv", row.names=FALSE)