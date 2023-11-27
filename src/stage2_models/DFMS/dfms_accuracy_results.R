rm(list = ls())
obj=load("data/Rdata/favar_dfms_output.RData")
libraries=source("utils/load_libraries.R")
source("utils/accuracy_measures.R")
#
# Define factor values to iterate over
factor_values <- c(2,3,4,5, ic_p2_factors)
#
results_list <- list()
for (factor in factor_values) {
  # Create model name and assign model to it
  model_name <- paste0("model_", factor)
  model <- DFM(data_s, r = factor, p = 1, em.method="BM", rQ="identity", rR="diagonal")
  F_hat=model$F_qml
  assign(model_name, model)

  # Forecasting
  fc <- predict(model, h = n_forecasts, method="pca", use="both")
  plot(fc, xlim = c(320, 370))
  predictions_df <- as.data.frame(fc$X_fcst)
  predictions_xts=xts(predictions_df, order.by = df_test_index)

  # Computing accuracy
  results_df <- compute_accuracy_measures_df(actual_s, predictions_xts)
  results_list[[model_name]] <- results_df

  # Calculating averages of the results
  averages <- colMeans(results_df, na.rm = TRUE)

  # Print the averages for each model
  print(paste("Métricas promedio de desempeño, factores", factor, ":"))
  print(averages)
  results_df <- compute_accuracy_measures_df(actual_s, predictions_xts)
  filename <- paste0("data/Rdata/F_hat_dfms_factor_", factor, ".RData")
  # Save objects to that file
  #save(F_hat, file = filename)
}








