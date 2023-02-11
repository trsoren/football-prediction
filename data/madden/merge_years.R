setwd('~/Desktop/eecs_448/football-prediction/data/madden')

all_data = data.frame(data.frame(matrix(ncol=4, nrow=0)))
colnames(all_data) = c("year", "team", "position", "overall")

for (year in list.files("raw_data")){
  df = read.csv(paste("raw_data/", year, '/data', year, '.csv', sep=''))
  all_data = rbind(all_data, df)
}

write.csv(all_data, 'all_player_data.csv' , row.names=FALSE)