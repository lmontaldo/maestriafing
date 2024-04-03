rm(list = ls())
dat=load("data/Rdata/input_data_models/favar_ddfm_input.RData")
libraries=source("utils/load_libraries.R")
source("utils/accuracy_measures.R")
source("utils/pca_norm.R")


# Define factor values to iterate over
#n_factors =7
factor_values <- c(2,3,4,5, 6, ic_p2_factors)
# Initialize empty lists to store results
path <- "docs/images/favar_n_factor_estimated"
results_list <- list()
for(n_factors in factor_values){
  cat("\n---------------------------------------------- \n")
  cat("Results for", n_factors,"latent factors \n")
  cat("---------------------------------------------- \n")
  cat('Step 1: Extract principal componentes of all X (including Y) \n')
  print(names(data_s))
  result <- perform_pca(data_s, n_components =n_factors)
  C<-result$principal_components
  cat('Step 2: Extract principal componentes of Slow Variables \n')
  slow_vars <- unlist(slow$slow)
  data_slow <- data_s[, slow_vars]
  pc_slow= perform_pca(data_slow, n_components =n_factors)
  F_slow=pc_slow$principal_components
  cat('Step 3: Clean the PC from the effect of observed Y \n')
  fedfunds <- as.matrix(data_s[, "FEDFUNDS"])
  reg <- lm(C ~ F_slow + fedfunds)
  F_hat <- C - data.matrix(data_s[, "FEDFUNDS"]) %*% reg$coefficients[nrow(reg$coefficients),]
  cat('Step 4: Estimate FAVAR and get IRFs \n')
  data_var <- data.frame(F_hat, "FEDFUNDS" = data_s[, "FEDFUNDS"])
  var_select <- VARselect(data_var, lag.max = 15, type="none")
  best_lag <- var_select$selection
  n_lags=best_lag[1]
  cat("Lags number in VAR according AIC:", n_lags, "\n")
  var = VAR(data_var, p =n_lags)
  # Calculando el peso de los factores
  cat("Computing Loading Factors \n")
  matriz_s<- as.matrix(data_s)
  matriz_fhat<- as.matrix(F_hat)
  reg_loadings = lm(matriz_s ~ 0 + matriz_fhat + data_s[,"FEDFUNDS"])
  loadings = reg_loadings$coefficients
  Lamda_F=loadings[1:n_factors,]
  Lambda_ffr=loadings[nrow(loadings),]
  ##########################################
  # Absolute values of Lambda_F
  ##########################################
  # Absolute values of Lambda_F
  abs_Lambda_F <- abs(Lamda_F)
  # Order columns in descending order based on the maximum absolute value in each column
  ordered_columns <- order(apply(abs_Lambda_F, 2, max), decreasing = TRUE)
  # Reorder the columns
  Lambda_F_ordered <- abs_Lambda_F[, ordered_columns]
  #print(Lambda_F_ordered)
  #############################################
  cat("Predictions ahead in test timeframe \n")
  ##############################################
  predicciones=predict(var, n.ahead = n_forecasts)
  vec_list <- list()
  for(factor_name in names(predicciones$fcst)) {
    if (startsWith(factor_name, "X")) {
      vec_list[[factor_name]] <- predicciones$fcst[[factor_name]][,1]}}
  pred_F <- do.call(cbind, vec_list)
  pred_FFR=predicciones$fcst$FEDFUNDS[,1]
  F_part=pred_F%*%Lamda_F
  Y_part=outer(pred_FFR, Lambda_ffr)
  X_pred=F_part+Y_part
  X_forec=as.data.frame(X_pred)
  predictions_df <- as.data.frame(X_pred)
  predictions_xts=xts(predictions_df,
                      order.by = df_test_index)

  cat('Accuracy measures \n')
  results_df <- compute_accuracy_measures_df(actual_s, predictions_xts)
  # print(results_df)
  cat("\n Peformance metrics: \n")
  averages <- colMeans(results_df, na.rm = TRUE)
  print(averages)
  #############################################################
  ######################## SAVE DATA ##########################
  #############################################################
  filename <- paste0("data/Rdata/favar_estimation_results/results_favar_factor_", n_factors, ".RData")
  cat('Saved objects in data/Rdata/favar_estimation_results \n')
  save(abs_Lambda_F,Lambda_F_ordered, loadings, data_s, data_slow,F_slow, reg_loadings,data_var,n_lags, F_hat,var,Lamda_F,Lambda_ffr,pred_F,pred_FFR,F_part, Y_part, predictions_xts,   file = filename)
  #######################################################################

}

