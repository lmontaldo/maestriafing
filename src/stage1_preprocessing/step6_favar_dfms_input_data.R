#
rm(list = ls())
library(Metrics)
library(forecast)
library(readxl)
libraries=source("utils/load_libraries.R")
cat("My Working directory is: ", getwd(), "\n")
df_train <- read_csv("data/train_test/sfr_train.csv", show_col_types = FALSE)
df_test <- read_csv("data/train_test/sfr_test.csv", show_col_types = FALSE)
slow <- read_csv("data/prepro/slow_variables.csv", show_col_types = FALSE)
#fast <- read_csv("../../data/prepro/fast_columns.csv", show_col_types = FALSE)
#escr <- read.table("../../data/prepro/descripciones.txt", header = TRUE, sep = "\t")
#####################################################################
# xts objects #######################################################
#####################################################################
df_train$index <- as.Date(df_train$index)
xts_object_train <- xts(df_train[, -which(colnames(df_train) == "index")], order.by = df_train$index)
data_s = scale(xts_object_train, center = TRUE, scale = TRUE)
#cat("Rango de datos:", as.character(range(index(xts_object))), "\n")
#cat("Tamaño de mi muestra de entrenamiento:", dim(data_s), "\n")
#
df_test$index <- as.Date(df_test$index)
xts_object_test <- xts(df_test[, -which(colnames(df_test) == "index")], order.by = df_test$index)
actual_s = scale(xts_object_test, center = TRUE, scale = TRUE)
df_test_index=df_test$index
# Number of forecast steps
n_forecasts = dim(actual_s)[1]
###########################################################################
# Optimal number of factors
###########################################################################
ics = ICr(data_s)
ic_p2_factors=ics$r.star[2]
###########################################################################################################################################
# variables as in https://jbduarte.com/blog/time%20series/r/favar/2020/04/24/FAVAR-Replication.html#Step-4:-Estimate-FAVAR-and-get-IRFs
###########################################################################################################################################
variables = c(grep("^FEDFUNDS$", colnames(data_s)),#Fed Funds Rate
              grep("^INDPRO$", colnames(data_s)), #IP Index
              grep("^CPIAUCSL$", colnames(data_s)), #CPI : All Items
              grep("^TB3MS$", colnames(data_s)), #3-Month Treasury Bill:
              grep("^GS5$", colnames(data_s)), #5-Year Treasury Rate
              grep("^M1SL$", colnames(data_s)),# M1 Money Stock
              grep("^M2SL$", colnames(data_s)), #M2 Money Stock
              grep("^EXJPUSx$", colnames(data_s)), #Japan / U.S. Foreign Exchange Rate
              grep("^CUSR0000SAC$", colnames(data_s)),#CPI : Commodities
              grep("^CUMFNS$", colnames(data_s)),#Capacity Utilization: Manufacturing
              grep("^DPCERA3M086SBEA$", colnames(data_s)),#Real personal consumption expenditures
              grep("^DDURRG3M086SBEA$", colnames(data_s)), #Personal Cons. Exp: Durable goods
              grep("^DNDGRG3M086SBEA$", colnames(data_s)), #Personal Cons. Exp: Nondurable goods
              grep("^UNRATE$", colnames(data_s)), #Civilian Unemployment Rate
              grep("^CE16OV$", colnames(data_s)), #Civilian Employment
              grep("^CES0600000008$", colnames(data_s)), #Avg Hourly Earnings : Goods-Producing
              grep("^HOUST$", colnames(data_s)),	#Housing Starts: Total New Privately Owned
              grep("^AMDMNOx$", colnames(data_s)), #New Orders for Durable Goods
              grep("^S.P.div.yield$", colnames(data_s))#S&P s Composite Common Stock: Dividend Yield
)
variable_names = c("Fed Funds Rate",
                   "IP Index",
                   "CPI",
                   "3-Month Treasury Bill",
                   "5-Year Treasury Rate",
                   "M1 Money Stock",
                   "M2 Money Stock",
                   "Exchange rate: Japan/U.S.",
                   "CPI : Commodities",
                   "Capacity Utilization",
                   "Real personal consump.",
                   "Durable goods consump.",
                   "Nondurable goods consump.",
                   "Unemployment Rate",
                   "Employment",
                   "Avg Hourly Earnings",
                   "Housing Starts",
                   "New Orders",
                   "Dividend Yield")

transf_code = c(1,5,5,1,1,5,5,5,1,1,5,5,5,1,1,5,1,1,1)
################################################################################
# save data ####################################################################
################################################################################
save(transf_code,variables, variable_names, df_train, slow,data_s, actual_s,df_test_index,n_forecasts, ics,ic_p2_factors,  file = "data/Rdata/favar_dfms_output.RData")
