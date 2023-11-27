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

favar_performance <- function(train_xts_s, test_set, slow, n_forecasts = NULL, max_lags = 15) {
  if(is.null(n_forecasts)) {
    n_forecasts = dim(test_set)[1]
  }

  ics <- ICr(train_xts_s)
  ic_p2_factors <- ics$r.star[2]

  factor_values <- c(2, 3, 4,ic_p2_factors)
  results_list <- list()

  for(factor in factor_values) {
    C <- ics$F_pca[, 1:factor]
    cat("\n---------------------------------------------- \n")
    cat("Resultados para", factor, "factores \n")
    cat("---------------------------------------------- \n")

    slow_vars <- unlist(slow$slow)
    data_slow <- train_xts_s[, slow_vars]
    ics_slow <- ICr(data_slow)
    F_slow <- ics_slow$F_pca[, 1:factor]

    fedfunds <- as.matrix(train_xts_s[, "FEDFUNDS"])
    reg <- lm(C ~ F_slow + fedfunds)
    F_hat <- C - fedfunds %*% reg$coefficients[nrow(reg$coefficients),]

    data_var <- data.frame(F_hat, "FEDFUNDS" = train_xts_s[, "FEDFUNDS"])
    var_select <- VARselect(data_var, lag.max = max_lags, type="none")
    best_lag <- var_select$selection["AIC"]

    cat("Cantidad de rezagos del VAR según AIC:", best_lag, "\n")

    var_model <- VAR(data_var, p = best_lag)

    matriz_s <- as.matrix(train_xts_s)
    matriz_fhat <- as.matrix(F_hat)
    reg_loadings <- lm(matriz_s ~ 0 + matriz_fhat + train_xts_s[, "FEDFUNDS"])
    loadings <- reg_loadings$coefficients
    Lambda_F <- loadings[1:factor,]
    Lambda_ffr <- loadings[nrow(loadings),]

    predictions <- predict(var_model, n.ahead = n_forecasts)

    vec_list <- list()
    for(factor_name in names(predictions$fcst)) {
      if (startsWith(factor_name, "PC")) {
        vec_list[[factor_name]] <- predictions$fcst[[factor_name]][, "fcst"]
      }
    }

    pred_F <- do.call(cbind, vec_list)
    pred_FFR <- predictions$fcst$FEDFUNDS[, "fcst"]
    F_part <- pred_F %*% Lambda_F
    Y_part <- outer(pred_FFR, Lambda_ffr)

    X_pred <- F_part + Y_part
    predictions_df <- as.data.frame(X_pred)

    results_list[[paste(factor, "factors")]] <- predictions_df
  }

  return(results_list)
}
# What is in the R directory before adding a function?
dir("favarBBE/R")

# Use the dump() function to write the numeric_summary function
dump("favar_performance", file = "C:/Users/user/Desktop/favarBBE/R/avg_performance.R")

# Verify that the file is in the correct directory
dir("favarBBE/R")


