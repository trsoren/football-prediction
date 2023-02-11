
library(readxl)

final_madden = data.frame()
final_madden = data.frame(matrix(ncol=9, nrow=0))
colnames(final_madden) = c("year", "team", "qb_rating", "rb_rating", "wr_rating", "ol_rating", "db_rating", "lb_rating", "dl_rating")
setwd("/Users/grantsasina/desktop/eecs_448/football-prediction/data/madden")


all_data = read.csv("all_player_data.csv")

all_data$team[which(all_data$team =="washington_redskins")] = "washington_football_team"
all_data$team[which(all_data$team =="oakland_raiders")] = "las_vegas_raiders"
all_data$team[which(all_data$team =="san_diego_chargers")] = "los_angeles_chargers"
all_data$team[which(all_data$team =="st._louis_rams")] = "los_angeles_rams"
all_data$team[which(all_data$team =="jacksonville_jagaurs")] = "jacksonville_jaguars" 

df = data.frame(all_data)
years = c("2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021")
for (year in years) {
  for (team in unique(all_data$team)) {
      new_df = df[which(df$team==team & df$year==year), ]
      
      qbs = new_df[which(new_df$position=="QB"), ]
      rbs = new_df[which(new_df$position=="HB"), ]
      wrs = new_df[which(new_df$position=="WR"| new_df$position == "TE"), ]
      oline = new_df[which(new_df$position == "C" | new_df$position == "RT" | new_df$position == "LT" | new_df$position == "RG" | new_df$position == "LG" | new_df$position == "OL"), ]
      dbs = new_df[which(new_df$position=="CB"| new_df$position == "FS" | new_df$position == "SS" | new_df$position == "S"), ]
      lbs = new_df[which(new_df$position=="LOLB"| new_df$position == "MLB" | new_df$position == "LB" | new_df$position == "ROLB"), ]
      dline = new_df[which(new_df$position=="DT"| new_df$position == "LE" | new_df$position == "RE" | new_df$position == "DL"), ]
      
      qbs = sort(qbs$overall, decreasing=TRUE)
      rbs = sort(rbs$overall, decreasing=TRUE)
      wrs = sort(wrs$overall, decreasing=TRUE)
      oline = sort(oline$overall, decreasing=TRUE)
      dbs = sort(dbs$overall, decreasing=TRUE)
      lbs = sort(lbs$overall, decreasing=TRUE)
      dline = sort(dline$overall, decreasing=TRUE)
      
      qb_score = qbs[1]
      rb_score = 0.75*rbs[1] + 0.25*rbs[2]
      wr_score = 0.40*wrs[1] + 0.25*wrs[2] + 0.20*wrs[3] + 0.15*wrs[4]
      oline_score = 0.20*oline[1] + 0.15*oline[2] + 0.15*oline[3] + 0.15*oline[4] + 0.15*oline[5] + 0.15*oline[6]
      db_score = 0.40*dbs[1] + 0.25*dbs[2] + 0.20*dbs[3] + 0.10*dbs[4] + 0.05*dbs[5]
      lb_score = 0.40*lbs[1] + 0.25*lbs[2] + 0.20*lbs[3] + 0.10*lbs[4] + 0.05*lbs[5]
      dline_score = 0.40*dline[1] + 0.25*dline[2] + 0.20*dline[3] + 0.10*dline[4] + 0.05*dline[5]
      vec = data.frame(year=year, team=team, qb_rating=qb_score, rb_rating=rb_score, wr_rating=wr_score, ol_rating=oline_score, db_rating=db_score, lb_rating=lb_score, dl_rating=dline_score)
      final_madden = rbind(final_madden, vec)
    }
  
  }
  
  write.csv(final_madden, "final_madden.csv", row.names=FALSE)
