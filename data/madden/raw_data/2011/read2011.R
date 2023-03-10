library(readxl)


master_ratings = data.frame(matrix(ncol=4, nrow=0))
colnames(master_ratings) = c("year", "team", "position", "overall")
for (fn in list.files()) {
  
  team = read_excel(fn)
  name = strsplit(fn, "_madden") [[1]][1]
  
  if (name == "chicago_bears" || name == "tennessee_titans") {
    df = data.frame(year=2011, team=name, position = team$POSITION, overall=team$"OVERALL\nRATING")
  }
  else {
    df = data.frame(year=2011, team=name, position = team$POSITION, overall=team$"OVERALL RATING")
  }
  
  master_ratings=rbind(master_ratings, df)
}

write.csv(master_ratings, "data2011.csv", row.names=FALSE)


# team <- # code to load in csv as df


#   team[]