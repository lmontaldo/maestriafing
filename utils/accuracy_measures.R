  compute_accuracy_measures_df <- function(actual_df, predictions_df) {
    # Check if inputs are xts or zoo objects
    if(!("xts" %in% class(actual_df) | "zoo" %in% class(actual_df)) ||
       !("xts" %in% class(predictions_df) | "zoo" %in% class(predictions_df))) {
      stop("Both actual_df and predictions_df must be xts or zoo objects.")
    }

    # Align the time index of predictions_df to that of actual_df
    index(predictions_df) <- index(actual_df)

    # Ensure dimensions match
    if(ncol(actual_df) != ncol(predictions_df) || nrow(actual_df) != nrow(predictions_df)) {
      stop("Dimensions of actual and predicted data must match after index alignment.")
    }

    measures_list <- list()

    for(i in 1:ncol(actual_df)) {
      actual <- actual_df[, i]
      predicted <- predictions_df[, i]

      # MAE
      mae <- mean(abs(actual - predicted), na.rm = TRUE)

      # MSE
      mse <- mean((actual - predicted)^2, na.rm = TRUE)

      # RMSFE (Root Mean Squared Forecast Error)
      rmsfe <- sqrt(mse)

      # Store in list
      measures_list[[colnames(actual_df)[i]]] <- c(MAE = mae, MSE = mse,  RMSFE = rmsfe)
    }

    # Convert the list to a dataframe
    results_df <- do.call(rbind, measures_list)
    rownames(results_df) <- colnames(actual_df)
    return(results_df)
  }
