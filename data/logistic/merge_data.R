get_off_code<-function(team) {
  switch(team, "arizona_cardinals" = "ARI_OFF",
         "atlanta_falcons" = "ATL_OFF",
         "baltimore_ravens" = "BAL_OFF",
         "buffalo_bills" = "BUF_OFF",
         "carolina_panthers" = "CAR_OFF",
         "chicago_bears" = "CHI_OFF",
         "cincinnati_bengals" = "CIN_OFF",
         "cleveland_browns" = "CLE_OFF",
         "dallas_cowboys" = "DAL_OFF",
         "denver_broncos" = "DEN_OFF",
         "detroit_lions" = "DET_OFF",
         "green_bay_packers" = "GB_OFF",
         "houston_texans" = "HOU_OFF",
         "indianapolis_colts" = "IND_OFF",
         "jacksonville_jaguars" = "JAX_OFF",
         "kansas_city_chiefs" = "KC_OFF",
         "miami_dolphins" = "MIA_OFF",
         "minnesota_vikings" = "MIN_OFF",
         "new_england_patriots" = "NE_OFF",
         "new_orleans_saints" = "NO_OFF",
         "new_york_giants" = "NYG_OFF",
         "new_york_jets" = "NYJ_OFF",
         "las_vegas_raiders" = "LV_OFF",
         "philadelphia_eagles" = "PHI_OFF",
         "pittsburgh_steelers" = "PIT_OFF",
         "los_angeles_chargers" = "LAC_OFF",
         "san_francisco_49ers" = "SF_OFF",
         "seattle_seahawks" = "SEA_OFF",
         "los_angeles_rams" = "LA_OFF",
         "tampa_bay_buccaneers" = "TB_OFF",
         "tennessee_titans" = "TEN_OFF",
         "washington_football_team" = "WAS_OFF")
}

get_def_code<-function(team) {
  switch(team, "arizona_cardinals" = "ARI_DEF",
         "atlanta_falcons" = "ATL_DEF",
         "baltimore_ravens" = "BAL_DEF",
         "buffalo_bills" = "BUF_DEF",
         "carolina_panthers" = "CAR_DEF",
         "chicago_bears" = "CHI_DEF",
         "cincinnati_bengals" = "CIN_DEF",
         "cleveland_browns" = "CLE_DEF",
         "dallas_cowboys" = "DAL_DEF",
         "denver_broncos" = "DEN_DEF",
         "detroit_lions" = "DET_DEF",
         "green_bay_packers" = "GB_DEF",
         "houston_texans" = "HOU_DEF",
         "indianapolis_colts" = "IND_DEF",
         "jacksonville_jaguars" = "JAX_DEF",
         "kansas_city_chiefs" = "KC_DEF",
         "miami_dolphins" = "MIA_DEF",
         "minnesota_vikings" = "MIN_DEF",
         "new_england_patriots" = "NE_DEF",
         "new_orleans_saints" = "NO_DEF",
         "new_york_giants" = "NYG_DEF",
         "new_york_jets" = "NYJ_DEF",
         "las_vegas_raiders" = "LV_DEF",
         "philadelphia_eagles" = "PHI_DEF",
         "pittsburgh_steelers" = "PIT_DEF",
         "los_angeles_chargers" = "LAC_DEF",
         "san_francisco_49ers" = "SF_DEF",
         "seattle_seahawks" = "SEA_DEF",
         "los_angeles_rams" = "LA_DEF",
         "tampa_bay_buccaneers" = "TB_DEF",
         "tennessee_titans" = "TEN_DEF",
         "washington_football_team" = "WAS_DEF")
}



# read in data 
df_plays = read.csv("/Users/trsorensen/Code/EECS448/football/data/plays/play_features.csv")
df_madden = read.csv("/Users/trsorensen/Code/EECS448/football/data/madden/final_madden.csv")

# add cols to plays df
#df_plays[c("qb_rating", "rb_rating", "wr_rating", "ol_rating", 
#           "db_rating", "lb_rating", "dl_rating")] = NA

# make madden offense stats df
df_off = data.frame(season=df_madden$year - 2009, team=df_madden$team, 
                     qb_rating=df_madden$qb_rating, rb_rating=df_madden$rb_rating,
                     wr_rating=df_madden$wr_rating, ol_rating=df_madden$ol_rating)
off_codes = names(df_plays)[which(grepl("_OFF", names(df_plays), fixed=TRUE))]
df_off[off_codes] = 0

# make madden defense stats df
df_def = data.frame(season=df_madden$year - 2009, team=df_madden$team, 
                     db_rating=df_madden$db_rating, lb_rating=df_madden$lb_rating,
                     dl_rating=df_madden$dl_rating)
def_codes = names(df_plays)[which(grepl("_DEF", names(df_plays), fixed=TRUE))]
df_def[def_codes] = 0

# fill corresponding featues of offense and defense stats dfs
for (team in unique(df_madden$team)) {
  #message(paste('"', team, '"', sep=''))
  df_off[which(df_off$team == team), get_off_code(team)] = 1
  df_def[which(df_def$team == team), get_def_code(team)] = 1
}
# remove full team names from offense and defense stats dfs
df_off = df_off[ ,-which(names(df_off)=='team')]
df_def = df_def[ ,-which(names(df_def)=='team')]


# merge plays with madden offense and defense team stats
df = merge(df_plays, df_off, all = TRUE)
df = merge(df, df_def, all = TRUE)

write.csv(df, "/Users/trsorensen/Code/EECS448/football/data/all_features.csv", row.names=F)
