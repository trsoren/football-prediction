
setwd("/Users/grantsasina/desktop/eecs_448/football-prediction/")

data <- read.csv("nn_data.csv")

data <- data.frame(data)

map <- 1:6
words <- c("sl", "sm", "sr", "dl", "dm", "dr")

map <- rbind(map, words)

data$outcome[data$outcome =="short left"] <- 1
data$outcome[data$outcome =="short middle"] <- 2
data$outcome[data$outcome =="short right"] <- 3
data$outcome[data$outcome =="deep left"] <- 4
data$outcome[data$outcome =="deep middle"] <- 5
data$outcome[data$outcome =="deep right"] <- 6


data <- na.omit(data)
unique(data)
mod <- glm(data=data, outcome ~ .)
#cor(data)


