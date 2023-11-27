library(readxl)
library(boot)
library(tsDyn)
library(vars)
library(repr)
df=read_csv("../data/prepro/sfr.csv")
slow=read_csv("../data/prepro/slow_columns.csv")
fast=read_csv("../data/prepro/fast_columns.csv")
print(head(df))
print(dim(df))
print(colnames(df))
data_s<- df[, 2:ncol(df)]
# Step 1: Extract principal componentes of all X (including Y)
pc_all = prcomp(data_s, center=FALSE, scale.=FALSE, rank. = 3)
print(summary(pc_all))
C = pc_all$x # saving the principal components
slow_vars <- unlist(slow$slow)
data_slow = data_s[, slow_vars]
pc_slow = prcomp(data_slow, center=FALSE, scale.=FALSE, rank. = 3)
F_slow = pc_slow$x
fedfunds <- as.matrix(data_s[, "FEDFUNDS"])
reg = lm(C ~ F_slow + fedfunds)
F_hat = C - data.matrix(data_s[,"FEDFUNDS"])%*%reg$coefficients[5,]
# Step 4: Estimate FAVAR and get IRFs
data_var = data.frame(F_hat, "FEDFUNDS" = data_s[,"FEDFUNDS"])
var = VAR(data_var, p = 13)
print(summary(var))