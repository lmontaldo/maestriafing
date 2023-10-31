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
rank_values <- c(3, 5, 10)
for (rank_val in rank_values) {
    cat("\n------------------ Results: ------------------------\n")
    cat("Rank =", rank_val, "\n")
  # Step 1: Extract principal components of all X (including Y)
  pc_all <- prcomp(data_s, center = FALSE, scale. = FALSE, rank. = rank_val)
  #print(summary(pc_all))
  C <- pc_all$x  # Saving the principal components
  print(dim(C))
  slow_vars <- unlist(slow$slow)
  data_slow <- data_s[, slow_vars]
  pc_slow <- prcomp(data_slow, center = FALSE, scale. = FALSE, rank. = rank_val)
  F_slow <- pc_slow$x
  fedfunds <- as.matrix(data_s[, "FEDFUNDS"])
  reg <- lm(C ~ F_slow + fedfunds)
  F_hat <- C - data.matrix(data_s[, "FEDFUNDS"]) %*% reg$coefficients[5,]
  # Step 4: Estimate FAVAR and get IRFs
  data_var <- data.frame(F_hat, "FEDFUNDS" = data_s[, "FEDFUNDS"])
  # Determine the number of lags using VARselect
  var_select <- VARselect(data_var, lag.max = 15, type = "both")
  best_lag <- var_select$selection
  best_model <- var_select$criteria
  cat("Best # lags according to AIC:", best_lag[1], "\n")
  cat("Best # lags according to FPE:", best_lag[4], "\n")
  # Fit the VAR model with the determined lag
  var <- VAR(data_var, p = best_lag[1], ic = "AIC")
  aic <- AIC(var)
  bic <- BIC(var)
  cat("Fit VAR with best number of lags and return information criteria: \n")
  cat("AIC:", aic, "\n")
  cat("BIC:", bic, "\n")
}