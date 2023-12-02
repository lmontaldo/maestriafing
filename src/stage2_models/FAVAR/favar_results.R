#
rm(list = ls())
load("data/Rdata/favar_dfms_output.RData")
libraries=source("utils/load_libraries.R")
source("utils/accuracy_measures.R")
#
# Define factor values to iterate over
factor_values <- c(1,2,3, 4, ic_p2_factors-1)
# Initialize empty lists to store results
results_list <- list()
#
for(factor in factor_values){
  C<-ics$F_pca[, 1:factor, drop = FALSE]
  cat("\n---------------------------------------------- \n")
  cat("Resultados para", factor,"factores \n")
  cat("---------------------------------------------- \n")
  slow_vars <- unlist(slow$slow)
  data_slow <- data_s[, slow_vars]
  ics_slow = ICr(data_slow)
  F_slow<-ics$F_pca[,1:factor, drop = FALSE]
  fedfunds <- as.matrix(data_s[, "FEDFUNDS"])
  reg <- lm(C ~ F_slow + fedfunds)
  dim(reg$coefficients[nrow(reg$coefficients),])
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
  print(dim(matriz_fhat))
  loadings = reg_loadings$coefficients
  #head(reg_loadings$coefficients)
  #summary(reg_loadings)
  Lamda_F=loadings[1:factor,]
  Lambda_ffr=loadings[nrow(loadings),]
  #Predicciones
  predicciones=predict(var, n.ahead = n_forecasts)
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
  predictions_xts=xts(predictions_df,
                      order.by = df_test_index)

  ####################################################################################
  ####################################################################################
  # Usage:
  results_df <- compute_accuracy_measures_df(actual_s, predictions_xts)
  #results_df
  cat("\nMétricas promedio de desempeño: \n")
  averages <- colMeans(results_df, na.rm = TRUE)
  print(averages)
  #filename <- paste0("data/Rdata/results_favar_factor_", factor, ".RData")
  # Save objects to that file
  #save(reg_loadings,data_var,n_lags, F_hat,var,Lamda_F,Lambda_ffr,pred_F,pred_FFR,F_part, Y_part, predictions_xts,   file = filename)

}
