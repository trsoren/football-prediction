df = read.csv("final_madden.csv")

png('plot.png', width=600, height=6400)
par(mfrow=c(32, 1))

for (team in unique(df$team)) {
  team_df = df[which(df$team == team), ]
  plot(
    x=team_df$year,
    y=team_df$qb_rating,
    main=team,
    type='l',
    ylim=c(60,100)
  )
}

dev.off()