rm(list = ls())
# Import labraries
libraries=source("utils/load_libraries.R")
source("utils/step1_corregir_o_borrar/fred_preprocessing.R")
source("utils/functions_csv.R")
# install fbi
devtools::install_github("cykbennie/fbi")

#source("utils/fred_preprocessing.R")
cat("My Working directory is: ", getwd(), "\n")

# Load data
filepath <- "https://files.stlouisfed.org/files/htdocs/fred-md/monthly/2021-08.csv"
data <- fredmd(filepath, date_start = NULL, date_end = NULL, transform = TRUE)

# Create description dataframe
descripcion_df=fredmd_description[, c("fred", "gsi:description", "group")]

# If the descripcion_df csv does not exist then create else skip function
path_descripcion_df="data/prepro/descripcion_df.csv"
descripcion_df_file_exists <-csv_file_exist(path_descripcion_df, data_to_write)


# Clean and select data
data_select <- clean_and_select_data(data)

# NA rows removal
cleaned_data <- remove_na_rows(data_select)

# Create df with first column
date_df <- data.frame(date = data_select[, 1])

# NA fill with kalman filter
imputed_data <- impute_na_kalman(data_select)

# Combine date_df and imputed_data

imputed_data_select <- cbind(date_df, imputed_data)

# Check if the time series is complete
check_time_series_completeness(imputed_data_select$date)
