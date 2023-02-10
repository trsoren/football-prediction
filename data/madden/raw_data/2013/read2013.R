library(readxl)


master_ratings = data.frame(matrix(ncol=4, nrow=0))
colnames(master_ratings) = c("year", "team", "position", "overall")
for (fn in list.files()) {
  
  team = read_excel(fn)
  name = strsplit(fn, "_madden") [[1]][1]
  
  df = data.frame(year=2013, team=name, position = team$Position, overall=team$Overall)
  
  master_ratings=rbind(master_ratings, df)
}

write.csv(master_ratings, "data2013.csv", row.names=FALSE)
