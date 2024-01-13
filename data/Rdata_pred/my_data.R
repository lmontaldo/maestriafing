library(readxl)
library(readr)
library(xts)
library(dplyr)
library(zoo)
df_train <- read_csv("data/prepro/sfr_train.csv", show_col_types = FALSE)
print(names(df_train))
df_test <- read_csv("data/prepro/sfr_test.csv", show_col_types = FALSE)
slow <- read_csv("data/prepro/slow_columns.csv", show_col_types = FALSE)
#
df=df_train
df_train$index <- as.Date(df_train$index)
xts_train <- xts(df_train[, -which(colnames(df_train) == "index")], order.by = df_train$index)
train_xts_s = scale(xts_train, center = TRUE, scale = TRUE)

#
df_test$index <- as.Date(df_test$index)
xts_test <- xts(df_test[, -which(colnames(df_test) == "index")], order.by = df_test$index)
test_s = scale(xts_test, center = TRUE, scale = TRUE)
actual_xts_s=scale(test_s, center = TRUE, scale = TRUE)
test_set=df_test[,2:ncol(df_test)]
actual_df=scale(test_set, center = TRUE, scale = TRUE)
#
save(slow, train_xts_s,actual_df, actual_xts_s, file = "favarBBE/data/input_dfs.RData")

