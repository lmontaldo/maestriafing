rm(list = ls())
# instalaciones necesarias
install.packages("devtools")
install.packages("stats")
install.packages("readr")
install.packages("pracma")
#devtools::install_github("cykbennie/fbi")
#
libraries=source("utils/load_libraries.R")
source("utils/functions_csv.R")
cat("My Working directory is: ", getwd(), "\n")
cat('Carga y transformacion de las series temporales:\n')
###################################################################
################  load data #######################################
###################################################################
filepath <- "https://files.stlouisfed.org/files/htdocs/fred-md/monthly/2021-08.csv"
data <- fredmd(filepath, date_start = NULL, date_end = NULL, transform = TRUE)
N <- ncol(data)
data(fredmd_description)
names(fredmd_description)
descripcion_df=fredmd_description[, c("fred", "gsi:description", "group")]
#write.csv2(descripcion_df, file = "data/prepro/descripcion_df.csv", row.names = FALSE, quote=FALSE)
###################################################################
################  Check for outliers and remove columns  ##########
###################################################################
data_clean <- rm_outliers.fredmd(data)
col_na_prop <- apply(is.na(data_clean), 2, mean)
data_select <- data_clean[, (col_na_prop < 0.05)]
###################################################################
################  Remove lines with na in head and tail  ##########
###################################################################
# Check if the head has NA values
head_has_na <- any(apply(head(data_select), 1, anyNA))
# Check if the tail has NA values
tail_has_na <- any(apply(tail(data_select), 1, anyNA))
# Remove rows from the head until there are no NA values
while (head_has_na) {
  data_select <- data_select[-1, ]  # Remove the first row
  head_has_na <- any(apply(head(data_select), 1, anyNA))
}
# Remove rows from the tail until there are no NA values
while (tail_has_na) {
  data_select <- data_select[-nrow(data_select), ]  # Remove the last row
  tail_has_na <- any(apply(tail(data_select), 1, anyNA))
}
date_df <- data.frame(date = data_select[, 1])

###################################################################
################  NA imputation using Kalman filter      ##########
###################################################################
# Identify numeric columns
numeric_cols <- sapply(data_select, is.numeric)
# Apply na_kalman to each numeric column
imputed_data_select <- lapply(data_select[, numeric_cols], function(x) {
  na_kalman(x, model = "StructTS", smooth = TRUE)
})

# Convert the list of imputed columns back to a dataframe
imputed_data_select <- as.data.frame(imputed_data_select)
# Combine the imputed numeric columns with non-numeric columns (if any)
imputed_data_select <- cbind(date_df, imputed_data_select)

###################################################################
################ check continuity of time series ##################
###################################################################
# Assuming 'date_column' is the name of your date column
date_column <- imputed_data_select$date
date_column <- as.Date(date_column)
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
###################################################################
################ save data ########################################
###################################################################
#commented line: not erase, change path if needed
#write.csv(imputed_data_select, file = "data/prepro/imputed_na_fred_data_prueba_borrar.csv", row.names = FALSE, sep=",")
path_imputed_na_fred_data="data/prepro/imputed_na_fred_data.csv"
#csv_file_exist(path_imputed_na_fred_data, data_to_write)
