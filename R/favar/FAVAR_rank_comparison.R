#
rm(list = ls())
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

#setwd("C:/Users/user/Desktop/Tesis_Maestria/src/stage2_models")
cat("My Working directory is: ", getwd(), "\n")
df_train <- read_csv("data/prepro/sfr_train.csv", show_col_types = FALSE)
df_test <- read_csv("data/prepro/sfr_test.csv", show_col_types = FALSE)
slow <- read_csv("data/prepro/slow_columns.csv", show_col_types = FALSE)
fast <- read_csv("data/prepro/fast_columns.csv", show_col_types = FALSE)
descr <- read.table("data/prepro/descripciones.txt", header = TRUE, sep = "\t")
#
df=df_train
# Convert the date_column to Date type
df$index <- as.Date(df$index)
# Create an xts object with the date_column as the index
xts_object <- xts(df[, -which(colnames(df) == "index")], order.by = df$index)
cat("Rango de datos:", as.character(range(index(xts_object))), "\n")
data_s = scale(xts_object, center = TRUE, scale = TRUE)
cat("Tamaño de mi muestra de entrenamiento:", dim(data_s), "\n")
#
df_test$index <- as.Date(df_test$index)
test_set=df_test[,2:ncol(df_test)]
actual_df=scale(test_set, center = TRUE, scale = TRUE)
cat("Tamaño de mi muestra de prueba:", dim(df_test), "\n")
#
n_forecasts = dim(df_test)[1]  # assuming this is the forecast length
# Initialize matrix to store forecasts
ics = ICr(data_s)
ic_p2_factors=ics$r.star[2]
#
# Define factor values to iterate over
factor_values <- c(2,3,ic_p2_factors)
# Initialize empty lists to store results
results_list <- list()
#
for(factor in factor_values){
  C<-ics$F_pca[, 1:factor]
  cat("\n---------------------------------------------- \n")
  cat("Resultados para", factor,"factores \n")
  cat("---------------------------------------------- \n")
  slow_vars <- unlist(slow$slow)
  data_slow <- data_s[, slow_vars]
  ics_slow = ICr(data_slow)
  F_slow<-ics$F_pca[,1:factor]
  fedfunds <- as.matrix(data_s[, "FEDFUNDS"])
  reg <- lm(C ~ F_slow + fedfunds)
  F_hat <- C - data.matrix(data_s[, "FEDFUNDS"]) %*% reg$coefficients[nrow(reg$coefficients),]
  data_var <- data.frame(F_hat, "FEDFUNDS" = data_s[, "FEDFUNDS"])
  var_select <- VARselect(data_var, lag.max = 15, type="none")
  best_lag <- var_select$selection
  n_lags=best_lag[1]
  cat("Cantidad de rezagos del VAR según AIC:", n_lags, "\n")
  var = VAR(data_var, p =n_lags)
  # Calculando el peso de los factores
  matriz_s<- as.matrix(data_s)
  matriz_fhat<- as.matrix(F_hat)
  reg_loadings = lm(matriz_s ~ 0 + matriz_fhat + data_s[,"FEDFUNDS"])
  loadings = reg_loadings$coefficients
  #head(reg_loadings$coefficients)
  #summary(reg_loadings)
  Lamda_F=loadings[1:factor,]
  Lambda_ffr=loadings[nrow(loadings),]
  #Predicciones
  predicciones=predict(var, n.ahead = dim(df_test)[1])
  #predicciones$fcst$PC1[,1]
  #predicciones$fcst$PC2[,1]
  #predicciones$fcst$PC3[,1]
  #pred_F <- cbind(predicciones$fcst$PC1[,1],
  #                       predicciones$fcst$PC2[,1],
  #                       predicciones$fcst$PC3[,1])
  vec_list <- list()
  for(factor_name in names(predicciones$fcst)) {
    if (startsWith(factor_name, "PC")) {
      vec_list[[factor_name]] <- predicciones$fcst[[factor_name]][,1]
    }
  }

  pred_F <- do.call(cbind, vec_list)
  pred_FFR=predicciones$fcst$FEDFUNDS[,1]
  F_part=pred_F%*%Lamda_F
  Y_part=outer(pred_FFR, Lambda_ffr)
  X_pred=F_part+Y_part
  X_forec=as.data.frame(X_pred)
  predictions_df <- as.data.frame(X_pred)
  # Desempeño
  compute_accuracy_measures_df <- function(actual_df, predictions_df) {
    if(ncol(actual_df) != ncol(predictions_df) || nrow(actual_df) != nrow(predictions_df)) {
      stop("Dimensions of actual and predicted data must match.")
    }

    measures_list <- list()

    for(i in 1:ncol(actual_df)) {
      actual <- actual_df[, i]
      predicted <- predictions_df[, i]

      # MAE
      mae <- mean(abs(actual - predicted), na.rm = TRUE)

      # MSE
      mse <- mean((actual - predicted)^2, na.rm = TRUE)

      # MAPE
      mape <- mean(abs((actual - predicted) / actual) * 100, na.rm = TRUE)

      # RMSFE (Root Mean Squared Forecast Error)
      rmsfe <- sqrt(mse)

      # Store in list
      measures_list[[colnames(actual_df)[i]]] <- c(MAE = mae, MSE = mse, MAPE = mape, RMSFE = rmsfe)
    }

    # Convert the list to a dataframe
    results_df <- do.call(rbind, measures_list)
    return(results_df)
  }

  # Usage:
  results_df <- compute_accuracy_measures_df(actual_df, predictions_df)
  #results_df
  cat("\nMétricas promedio de desempeño: \n")
  averages <- colMeans(results_df, na.rm = TRUE)
  print(averages)#
  #filename <- paste0("favarBBE/data/results_factor_", factor, ".RData")
  # Save objects to that file
  #save(list = ls(), file = filename)

}
