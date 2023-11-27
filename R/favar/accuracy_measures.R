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
