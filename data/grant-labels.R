
setwd("/Users/grantsasina/desktop/eecs_448/football-prediction/data/data-bowl")
data <- read.csv("plays.csv")


df = data.frame(data)

df2 <- df[, c("gameId", "playId", "playDescription")]

# SHORT LEFT INCOMPLETE
shortLeftInc <- grepl("short", df$playDescription) & grepl("left", df$playDescription) & 
  grepl("incomplete", df$playDescription)

dfsli <- df2[shortLeftInc, ]
dfsli$playDescription = "short left incomplete"

# SHORT RIGHT INCOMPLETE
shortRightInc <- grepl("short", df$playDescription) & grepl("right", df$playDescription) & 
  grepl("incomplete", df$playDescription)

dfsri <- df2[shortRightInc, ]
dfsri$playDescription = "short right incomplete"

# SHORT LEFT COMPLETE
shortLeftCom <- grepl("short", df$playDescription) & grepl("left", df$playDescription) & 
  !grepl("incomplete", df$playDescription)

dfslc <- df2[shortLeftCom, ]
dfslc$playDescription = "short left complete"

# SHORT RIGHT COMPLETE
shortRightCom <- grepl("short", df$playDescription) & grepl("right", df$playDescription) & 
  !grepl("incomplete", df$playDescription)

dfsrc <- df2[shortRightCom, ]
dfsrc$playDescription = "short right complete"

# SHORT MIDDLE INCOMPLETE
shortMidInc <- grepl("short", df$playDescription) & grepl("middle", df$playDescription) & 
  grepl("incomplete", df$playDescription)

dfsmi <- df2[shortMidInc, ]
dfsmi$playDescription = "short middle incomplete"

# SHORT MIDDLE COMPLETE
shortMidCom <- grepl("short", df$playDescription) & grepl("middle", df$playDescription) & 
  !grepl("incomplete", df$playDescription)

dfsmc <- df2[shortMidCom, ]
dfsmc$playDescription = "short middle complete"


# DEEP

# DEEP LEFT INCOMPLETE
deepLeftInc <- grepl("deep", df$playDescription) & grepl("left", df$playDescription) & 
  grepl("incomplete", df$playDescription)

dfdli <- df2[deepLeftInc, ]
dfdli$playDescription = "deep left incomplete"

# DEEP RIGHT INCOMPLETE
deepRightInc <- grepl("deep", df$playDescription) & grepl("right", df$playDescription) & 
  grepl("incomplete", df$playDescription)

dfdri <- df2[deepRightInc, ]
dfdri$playDescription = "deep right incomplete"

# DEEP LEFT COMPLETE
deepLeftCom <- grepl("deep", df$playDescription) & grepl("left", df$playDescription) & 
  !grepl("incomplete", df$playDescription)

dfdlc <- df2[deepLeftCom, ]
dfdlc$playDescription = "deep left complete"

# DEEP RIGHT COMPLETE
deepRightCom <- grepl("deep", df$playDescription) & grepl("right", df$playDescription) & 
  !grepl("incomplete", df$playDescription)

dfdrc <- df2[deepRightCom, ]
dfdrc$playDescription = "deep right complete"

# DEEP MIDDLE INCOMPLETE
deepMidInc <- grepl("deep", df$playDescription) & grepl("middle", df$playDescription) & 
  grepl("incomplete", df$playDescription)

dfdmi <- df2[deepMidInc, ]
dfdmi$playDescription = "deep middle incomplete"

# DEEP MIDDLE COMPLETE
deepMidCom <- grepl("deep", df$playDescription) & grepl("middle", df$playDescription) & 
  !grepl("incomplete", df$playDescription)

dfdmc <- df2[deepMidCom, ]
dfdmc$playDescription = "deep middle complete"


finaldf <- rbind(dfdlc, dfdli, dfdmc, dfdmi, dfdrc, dfdri, dfslc, dfsli, dfsmc, dfsmi, dfsrc, dfsri)

write.csv(finaldf, file = "labels.csv", row.names = FALSE)