rm(list = ls())
obj1=load("data/Rdata/favar_dfms_output.RData")
obj2=load("data/Rdata/favar_estimation_results/results_favar_factor_6.RData")
libraries=source("utils/load_libraries.R")

###############################
# Nombres variables
################################
data(fredmd_description)
n_g=fredmd_description
ng=n_g[, c("fred", "group","gsi:description")]
# List of values to be changed
values_to_change <- c("S&P 500", "S&P: indust", "S&P div yield", "S&P PE ratio", "IPB51222s")
# New values to replace the old values
new_values <- c("S.P.500", "S.P..indust", "S.P.div.yield", "S.P.PE.ratio", "IPB51222S")
# Loop through each value to be changed and replace them with new values
for (i in seq_along(values_to_change)) {
  ng$fred[ng$fred == values_to_change[i]] <- new_values[i]
}
colnames(ng)[colnames(ng) == "gsi:description"] <- "gsi"


################################################################
#### CONTRIBUTION 15 VARIABLES MAS IMPORTANTES A CADA FACTOR
####################################################################
# Create a list to store the data frames
result_dfs <- list()

# Iterate over each row (factor) of the absolute lambda matrix
for (i in 1:nrow(abs_Lambda_F)) {
  # Extract the absolute lambda values for the current factor
  factor_abs_lambda <- abs_Lambda_F[i, ]

  # Order the columns in descending order based on absolute lambda values
  ordered_columns <- order(factor_abs_lambda, decreasing = TRUE)

  # Extract the first 15 columns with the highest absolute lambda values
  top_15_columns <- ordered_columns[1:min(15, length(ordered_columns))]

  # Create a data frame with the top 15 columns for the current factor
  factor_df <- data.frame(variable = colnames(abs_Lambda_F), lambda = factor_abs_lambda)
  factor_df <- factor_df[top_15_columns, ]

  # Assign a meaningful name to the data frame and store it in the list
  factor_name <- paste("Factor", i, sep = "_")
  result_dfs[[factor_name]] <- factor_df
}

# Print the first few rows of each data frame
for (factor_df_name in names(result_dfs)) {
  cat(factor_df_name, ":\n")
  print(result_dfs[[factor_df_name]])
  cat("\n")
}

factor_1_df <- result_dfs$Factor_1
factor_2_df <- result_dfs$Factor_2
factor_3_df <- result_dfs$Factor_3
factor_4_df <- result_dfs$Factor_4
factor_5_df <- result_dfs$Factor_5
factor_6_df <- result_dfs$Factor_6

############################################
#### NOMBRE DE CADA VARIABLE Y GRUPO ######
############################################

# Create a list to store the updated data frames
updated_dfs <- list()

# Loop through each factor dataframe
for (i in 1:6) {
  # Get the current factor dataframe
  factor_df <- result_dfs[[paste("Factor", i, sep = "_")]]

  # Loop through each variable in the factor dataframe
  for (j in 1:nrow(factor_df)) {
    # Get the current variable from the factor dataframe
    current_variable <- factor_df[j, "variable"]

    # Find the index of the matching variable in ng$fred (using partial string match)
    match_index <- grep(current_variable, ng$fred, ignore.case = TRUE)

    # If a match is found, replace the variable with the corresponding gsi:description
    if (length(match_index) > 0) {
      # Select the first matched value (you can adjust this based on your preference)
      factor_df[j, "variable"] <- ng$gsi[match_index[1]]

      # Add the corresponding group value to the dataframe
      factor_df[j, "group"] <- ng$group[match_index[1]]
    }
  }

  # Store the updated dataframe in the list
  updated_dfs[[paste("Factor", i, sep = "_")]] <- factor_df
}

# Assign updated dataframes to individual variables
factor_1_lineal <- updated_dfs$Factor_1
factor_2_lineal <- updated_dfs$Factor_2
factor_3_lineal <- updated_dfs$Factor_3
factor_4_lineal <- updated_dfs$Factor_4
factor_5_lineal <- updated_dfs$Factor_5
factor_6_lineal<- updated_dfs$Factor_6

# Save the updated dataframes as an RData object
# Save the dataframes as an RData object
save(factor_1_lineal, factor_2_lineal, factor_3_lineal, factor_4_lineal, factor_5_lineal, factor_6_lineal, file = "data/Rdata/factor_comparison/VI_factors_lineal.RData")
