#setwd("C:/Users/user/Desktop/Tesis_Maestria - copia")
# What is in the R directory before adding a function?
cat("My Working directory is: ", getwd(), "\n")
# libraries
library(Metrics)
library(forecast)
library(readxl)
library(readr)
library(boot)
library(tsDyn)
library(vars)
library(repr)
library(dplyr)
library(dfms)
library(xts)
library(vars)
library(fbi)
library(forecast)
library(OOS)
library(zoo)
#
df_train <- read_csv("data/prepro/sfr_train.csv", show_col_types = FALSE)
print(names(df_train))
df_test <- read_csv("data/prepro/sfr_test.csv", show_col_types = FALSE)
slow <- read_csv("data/prepro/slow_columns.csv", show_col_types = FALSE)
#
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
data_s=train_xts_s
n_forecasts = dim(test_set)[1]  # assuming this is the forecast length
# Initialize matrix to store forecasts
ics = ICr(train_xts_s)
IC_p2_optimal_factors=ics$r.star[2]
save(ics,IC_p2_optimal_factors, file = "C:/Users/user/Desktop/favarBBE/data/fact_opt_IC.RData")

