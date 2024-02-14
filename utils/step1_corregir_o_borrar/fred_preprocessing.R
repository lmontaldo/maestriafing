# Clean and select data
clean_and_select_data <- function(input_data, na_threshold = 0.05) {
  # Step 1: Remove outliers using rm_outliers.fredmd
  cat("Step 1: Removing outliers...\n")
  cleaned_data <- rm_outliers.fredmd(input_data)

  # Step 2: Calculate column-wise NA proportion
  cat("Step 2: Calculating NA proportions...\n")
  col_na_prop <- apply(is.na(cleaned_data), 2, mean)

  # Step 3: Select columns with NA proportion less than the specified threshold
  cat("Step 3: Selecting columns with NA proportion < ", na_threshold, "...\n")
  selected_data <- cleaned_data[, col_na_prop < na_threshold]

  cat("Cleaning and selection process complete.\n")

  return(selected_data)
}

# NA rows removal
remove_na_rows <- function(input_data) {
  cat("Step 1: Checking if the head has NA values...\n")
  head_has_na <- any(apply(head(input_data), 1, anyNA))

  cat("Step 2: Checking if the tail has NA values...\n")
  tail_has_na <- any(apply(tail(input_data), 1, anyNA))

  cat("Step 3: Removing rows from the head until there are no NA values...\n")
  while (head_has_na) {
    input_data <- input_data[-1, ]  # Remove the first row
    head_has_na <- any(apply(head(input_data), 1, anyNA))
  }

  cat("Step 4: Removing rows from the tail until there are no NA values...\n")
  while (tail_has_na) {
    input_data <- input_data[-nrow(input_data), ]  # Remove the last row
    tail_has_na <- any(apply(tail(input_data), 1, anyNA))
  }

  cat("NA row removal process complete.\n")

  return(input_data)
}

# NA fill with kalman filter
impute_na_kalman <- function(input_data) {
  cat("Step 1: Identifying numeric columns...\n")
  # Identify numeric columns
  numeric_cols <- sapply(input_data, is.numeric)

  cat("Step 2: Applying na_kalman to each numeric column...\n")
  # Apply na_kalman to each numeric column
  imputed_data <- lapply(input_data[, numeric_cols], function(x) {
    na_kalman(x, model = "StructTS", smooth = TRUE)
  })

  cat("Step 3: Converting the list of imputed columns back to a dataframe...\n")
  # Convert the list of imputed columns back to a dataframe
  imputed_data <- as.data.frame(imputed_data)

  cat("NA imputation using Kalman filter complete.\n")

  return(imputed_data)
}

# check if time series is complete
check_time_series_completeness <- function(date_column) {
  cat("Step 1: Converting 'date_column' to Date format...\n")
  # Convert 'date_column' to Date format
  date_column <- as.Date(date_column)

  cat("Step 2: Checking if the date column forms a complete time series...\n")
  # Check if the date column is a complete time series
  min_date <- as.Date(min(date_column))
  max_date <- as.Date(max(date_column))
  expected_dates <- seq(min_date, max_date, by = "1 month")  # Assuming monthly data

  # Check if there are any missing dates
  missing_dates <- setdiff(expected_dates, unique(date_column))
  if (length(missing_dates) == 0) {
    cat("The date column forms a complete time series\n")
  } else {
    cat("There are missing dates in the time series.\n")
  }
}
