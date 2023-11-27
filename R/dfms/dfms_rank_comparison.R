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
library(xtable)
source("favarBBE/R/accuracy_measures.R")
loaded_objects=load("favarBBE/data/initial_df.RData")
#train_xts_s
plot(train_xts_s, lwd = 1, main= "Stationary series (all)")
ic = ICr(train_xts_s)
ic_p2_factors=ic$r.star[2]
factors=c(2,3,4,ic_p2_factors)
#
actual_data <- actual_xts_s  # make sure to replace with your actual test data
results_list <- list()
for (factor in factors) {
  # Create model name and assign model to it
  model_name <- paste0("model_", factor)
  model <- DFM(train_xts_s, r = factor, p = 1, em.method="DGR", rQ="identity", rR="diagonal")
  assign(model_name, model)

  # Forecasting
  fc <- predict(model, h = dim(df_test)[1], method="pca", use="both")
  predictions_df <- as.data.frame(fc$X_fcst)

  # Computing accuracy
  results_df <- compute_accuracy_measures_df(actual_df, predictions_df)
  results_list[[model_name]] <- results_df

  # Calculating averages of the results
  averages <- colMeans(results_df, na.rm = TRUE)

  # Print the averages for each model
  print(paste("Averages for model", factor, ":"))
  print(averages)
}








