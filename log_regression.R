library(corrplot)

# read in data
df = read.csv("/Users/trsorensen/Code/EECS448/football/data/all_features.csv")

# remove the 2022 data (for now) as madden only goes to 2021
df = df[-which(df$season == 13), ]

# remove the team offense and defnse codes
df = df[ ,-which(grepl('_OFF', names(df), fixed=TRUE))]
df = df[ ,-which(grepl('_DEF', names(df), fixed=TRUE))]

# remove the madden rankings :(
df = df[ ,-which(grepl('_rating', names(df), fixed=TRUE))]

# normalize madden ratings by taking their z-score
#df$qb_rating = (df$qb_rating - mean(df$qb_rating)) / sd(df$qb_rating)
#df$rb_rating = (df$rb_rating - mean(df$rb_rating)) / sd(df$rb_rating)
#df$wr_rating = (df$wr_rating - mean(df$wr_rating)) / sd(df$wr_rating)
#df$ol_rating = (df$ol_rating - mean(df$ol_rating)) / sd(df$ol_rating)
#df$db_rating = (df$db_rating - mean(df$db_rating)) / sd(df$db_rating)
#df$lb_rating = (df$lb_rating - mean(df$lb_rating)) / sd(df$lb_rating)
#df$dl_rating = (df$dl_rating - mean(df$dl_rating)) / sd(df$dl_rating)



# split data into training and testing sets
train_df = df[-which(df$season==12), ]
test_df = df[which(df$season==12), ]

# train logistic regression model
model = glm(play_type ~ . ,family=binomial(link='logit'), data=df)
# print(summary(model))

probabilities = predict(model, newdata=df, type='response')
predicted = ifelse(probabilities > 0.5, 1, 0)
# Model accuracy
print('Model accuracy: ')
print(mean(predicted == df$play_type))
print('Proportion of passes in data')
print(sum(df$play_type) / length(df$play_type))

# check for columns with NA
# indx <- apply(df, 2, function(x) any(is.na(x) | is.infinite(x)))
# print(names(df)[indx])

# make correlation matrix and save as png
cor = cor(df)
png("/Users/trsorensen/Code/EECS448/football/data/corr_matrix.png", height=1000, width=1000)
corrplot(cor, type = "upper", order = "hclust", 
         tl.col = "black", tl.srt = 45)
dev.off()



