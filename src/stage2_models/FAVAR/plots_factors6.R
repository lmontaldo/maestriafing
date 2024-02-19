rm(list = ls())
factor6=load("data/Rdata/results_favar_factor_6.RData")
libraries=source("utils/load_libraries.R")
source("utils/accuracy_measures.R")
##############################################
######### PARA LA CREACIÓN DE LOS GRUPOS
##############################################
data(fredmd_description)
n_g=fredmd_description
ng=n_g[, c("fred", "group","gsi:description")]
unique(ng$group)
# List of values to be changed
values_to_change <- c("S&P 500", "S&P: indust", "S&P div yield", "S&P PE ratio", "IPB51222s")
# New values to replace the old values
new_values <- c("S.P.500", "S.P..indust", "S.P.div.yield", "S.P.PE.ratio", "IPB51222S")
# Loop through each value to be changed and replace them with new values
for (i in seq_along(values_to_change)) {
  ng$fred[ng$fred == values_to_change[i]] <- new_values[i]
}
##########
# Extract column names from Lamda_F
Lamda_F_colnames <- colnames(Lamda_F)
# Check if column names of Lamda_F are in ng$fred
colnames_in_ng <- Lamda_F_colnames %in% ng$fred
print(colnames_in_ng )
print(Lamda_F_colnames[!colnames_in_ng])
#########################
# Check if a similar value to "IPB51222S" exists in ng$fred
similar_index <- grep("IPB51222S", ng$fred, ignore.case = TRUE)
# Check if any match is found
if (length(similar_index) > 0) {
  # Retrieve the name from ng$fred using the index
  similar_name <- ng$fred[similar_index]
  print(similar_name)
} else {
  print("No similar value found.")
}
####
print(factor6)

##################################
# GRAFICO DE FACTORES ESTIMADOS
##################################
df=data_var
# Assuming your dataframe is named 'df'
xts_data <- xts(df[, -ncol(df)], order.by = as.Date(rownames(df)))

# Convert xts to data frame
df_plot <- data.frame(date = index(xts_data), coredata(xts_data))

# Reshape the data for ggplot2
df_plot_long <- tidyr::gather(df_plot, key = "variable", value = "value", -date)

# Plot using ggplot2
f6_estimacion_plot <-ggplot(df_plot_long, aes(x = date, y = value, color = variable)) +
  geom_line() +
  labs(title = "Seis Factores Estimados", x = "fecha", y = "valor") +
  theme_minimal() +
  theme(legend.position = c(0.95, 0.1), legend.title = element_blank()) +
  guides(color = guide_legend(title = NULL))
saveRDS(f6_estimacion_plot, file = "rds_files/estimacion6factores.rds")


############################################################
# Calculate the absolute values of the factor loadings
abs_loadings <- abs(Lamda_F)
##########################################################



# Order the variables related to each row based on their absolute factor loadings
ordered_indices <- apply(abs_loadings, 1, order, decreasing = TRUE)


# Print the ordered variables and their factor loading values for each row
for (i in 1:nrow(abs_loadings)) {
  cat("Variables contributing the most to Lamda_F PC", i, ":\n")
  ordered_vars <- colnames(abs_loadings)[ordered_indices[i, ]]
  ordered_values <- abs_loadings[i, ordered_indices[i, ]]
  for (j in seq_along(ordered_vars)) {
    cat(ordered_vars[j], ": ", ordered_values[j], "\n")
  }
}

################ 1er resultado #########
#######################################
# Create an empty list to store the matched group values for each component
matched_groups <- list()

# Iterate over each component
for (i in 1:nrow(abs_loadings)) {
  cat("Variables contributing the most to Lamda_F PC", i, ":\n")

  # Get the ordered variables and their factor loading values for the current component
  ordered_vars <- colnames(abs_loadings)[ordered_indices[i, ]]
  ordered_values <- abs_loadings[i, ordered_indices[i, ]]

  # Initialize a vector to store the matched group values for the current component
  matched_groups[[i]] <- character(length(ordered_vars))

  # Iterate over each variable and match its group value
  for (j in seq_along(ordered_vars)) {
    # Match the variable name in the ng dataframe
    match_index <- match(ordered_vars[j], ng$fred)

    # Check if a match was found
    if (!is.na(match_index)) {
      # Store the matched group value
      matched_groups[[i]][j] <- ng$group[match_index]
    } else {
      # If no match was found, set the group value to NA
      matched_groups[[i]][j] <- NA
    }

    # Print the variable name, factor loading value, and matched group value
    cat(ordered_vars[j], ": ", ordered_values[j], " (Group: ", matched_groups[[i]][j], ")\n")
  }
}

# Create an empty list to store the average values for each component and group
average_values <- list()

# Iterate over each component
for (i in 1:length(matched_groups)) {
  # Get the matched group values for the current component
  groups <- matched_groups[[i]]

  # Initialize a data frame to store the variable names, their corresponding factor loading values, and matched group values
  df <- data.frame(Variable = ordered_vars, Value = ordered_values, Group = groups)

  # Remove rows with NA group values
  df <- df[complete.cases(df), ]

  # Group by the 'Group' column and calculate the average value for each group
  avg_values <- tapply(df$Value, df$Group, mean)

  # Store the average values in the list
  average_values[[i]] <- avg_values
}

# Iterate over each component
for (i in 1:length(average_values)) {
  cat("Component:", i, "\n")

  # Print the average values for each group
  print(average_values[[i]])
}

###############################################
###################### 2 intento
###############################################
# Calculate the absolute values of the factor loadings
abs_loadings <- abs(Lamda_F)

abs_loadings

# Order the variables related to each row based on their absolute factor loadings
ordered_indices <- apply(abs_loadings, 1, order, decreasing = TRUE)

# Print the ordered variables and their factor loading values for each row
for (i in 1:nrow(Lamda_F)) {
  cat("Variables contributing the most to Lamda_F PC", i, ":\n")
  ordered_vars <- colnames(Lamda_F)[ordered_indices[i, ]]
  ordered_values <- abs_loadings[i, ordered_indices[i, ]]
  for (j in seq_along(ordered_vars)) {
    cat(ordered_vars[j], ": ", ordered_values[j], "\n")
  }
}


#################################
###### 3 intento ################
#################################
t_abs_loadings=t(abs_loadings)

# Initialize an empty list to store the data frames
dataframes <- list()

# Iterate over each column of the transposed matrix
for (col_name in colnames(t_abs_loadings)) {
  # Create a data frame for the current column with row names preserved
  df <- data.frame(value = t_abs_loadings[, col_name])
  # Assign the column name
  colnames(df) <- col_name
  # Add the data frame to the list
  dataframes[[col_name]] <- df
}

# Accessing the data frames
# For example, to access the data frame corresponding to 'matriz_fhatPC1':

pc1=dataframes[['matriz_fhatPC1']]
pc2=dataframes[['matriz_fhatPC2']]
pc3=dataframes[['matriz_fhatPC3']]
pc4=dataframes[['matriz_fhatPC4']]
pc5=dataframes[['matriz_fhatPC5']]
pc6=dataframes[['matriz_fhatPC6']]

# Define a function to order a dataframe by its only column in descending order
order_dataframe <- function(df) {
  df_ordered <- df[order(-df[[1]]), , drop = FALSE]
  return(df_ordered)
}


pc1=order_dataframe(pc1)
pc2=order_dataframe(pc2)
pc3=order_dataframe(pc3)
pc4=order_dataframe(pc4)
pc5=order_dataframe(pc5)
pc6=order_dataframe(pc6)

check_descending <- function(df) {
  all(sapply(df, function(col) all(diff(col) < 0)))
}

check_descending(pc3)

merged_df <- cbind(pc1, pc2,pc3, pc4, pc5, pc6)

# If you want to keep the row names as a separate column, you can do:
merged_df <- cbind(rownames = rownames(merged_df), merged_df)

# Create a new column "group"
merged_df$group <- NA

# Loop through each row in merged_df
for (i in 1:nrow(merged_df)) {
  # Get the row name (which is also present in ng$fred)
  row_name <- rownames(merged_df)[i]

  # Find the corresponding value in ng$group based on ng$fred matching the row name
  group_value <- ng$group[ng$fred == row_name]

  # Assign the group value to the corresponding row in merged_df
  merged_df[i, "group"] <- group_value
}

group_means <- merged_df %>%
  group_by(group) %>%
  summarise(across(where(is.numeric), mean, na.rm = TRUE))
print(group_means)

# Remove the "matriz_fhat" part from the column names in group_means
colnames(group_means) <- gsub("matriz_fhat", "", colnames(group_means))

mat_group_means <- as.matrix(group_means)
mat_group_means_numeric <- apply(mat_group_means[, -1], 2, as.numeric)

# Set row names
rownames(mat_group_means_numeric) <- mat_group_means[, 1]

print(mat_group_means_numeric)


# Create heatmap
heatmap(mat_group_means_numeric,
        Rowv = NA,
        Colv = NA,
        col = cm.colors(256),
        scale = "column",
        margins = c(5, 10))
# Install and load necessary packages
#install.packages("pheatmap")
library(pheatmap)

# Create the heatmap
pheatmap(group_means,
         cluster_rows = FALSE,  # Don't cluster rows
         cluster_cols = TRUE,   # Cluster columns
         main = "Heatmap of Mean Values by Group",  # Main title
         xlab = "Columns",      # Label for x-axis
         ylab = "Row Names"     # Label for y-axis
)


#############

############# PC1

pc1$group <- NA
# Loop through each row in pc1
for (i in 1:nrow(pc1)) {
  # Get the row name (which is also present in ng$fred)
  row_name <- rownames(pc1)[i]

  # Find the corresponding value in ng$group based on ng$fred matching the row name
  group_value <- ng$group[ng$fred == row_name]

  # Assign the group value to the corresponding row in pc1
  pc1[i, "group"] <- group_value
}

group_averages <- aggregate(matriz_fhatPC1 ~ group, data = pc1, FUN = mean)
group_averages <- group_averages[order(-group_averages$matriz_fhatPC1), ]
# Print the resulting dataframe with group averages
print(group_averages)



# Reorder the levels of the "group" factor based on the averaged values in descending order
group_averages$group <- factor(group_averages$group, levels = group_averages$group[order(group_averages$matriz_fhatPC1, decreasing = TRUE)])

ggplot(group_averages, aes(x = group, y = matriz_fhatPC1)) +
  geom_bar(stat = "identity") +
  labs(x = "Group", y = "Average Value", title = "Group Averages") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))
#########
# PC 2
pc2$group <- NA
# Loop through each row in pc1
for (i in 1:nrow(pc2)) {
  # Get the row name (which is also present in ng$fred)
  row_name <- rownames(pc2)[i]

  # Find the corresponding value in ng$group based on ng$fred matching the row name
  group_value <- ng$group[ng$fred == row_name]

  # Assign the group value to the corresponding row in pc1
  pc2[i, "group"] <- group_value
}

group_averages <- aggregate(matriz_fhatPC2 ~ group, data = pc2, FUN = mean)
group_averages <- group_averages[order(-group_averages$matriz_fhatPC2), ]
# Print the resulting dataframe with group averages
print(group_averages)



# Reorder the levels of the "group" factor based on the averaged values in descending order
group_averages$group <- factor(group_averages$group, levels = group_averages$group[order(group_averages$matriz_fhatPC2,
                                                                                         decreasing = TRUE)])

ggplot(group_averages, aes(x = group, y = matriz_fhatPC2)) +
  geom_bar(stat = "identity") +
  labs(x = "Group", y = "Average Value", title = "PC2") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))







#####
# Create an empty list to store the matched group values for each component
matched_groups <- list()

# Iterate over each component
for (i in 1:nrow(Lamda_F)) {
  cat("Variables contributing the most to Lamda_F PC", i, ":\n")

  # Get the ordered variables and their factor loading values for the current component
  ordered_vars <- colnames(Lamda_F)[ordered_indices[i, ]]
  ordered_values <- abs_loadings[i, ordered_indices[i, ]]

  # Initialize a vector to store the matched group values for the current component
  matched_groups[[i]] <- character(length(ordered_vars))

  # Iterate over each variable and match its group value
  for (j in seq_along(ordered_vars)) {
    # Match the variable name in the ng dataframe
    match_index <- match(ordered_vars[j], ng$fred)

    # Check if a match was found
    if (!is.na(match_index)) {
      # Store the matched group value
      matched_groups[[i]][j] <- ng$group[match_index]
    } else {
      # If no match was found, set the group value to NA
      matched_groups[[i]][j] <- NA
    }

    # Print the variable name, factor loading value, and matched group value
    cat(ordered_vars[j], ": ", ordered_values[j], " (Group: ", matched_groups[[i]][j], ")\n")
  }
}

# Create an empty list to store the average values for each component and group
average_values <- list()

# Iterate over each component
for (i in 1:length(matched_groups)) {
  # Get the matched group values for the current component
  groups <- matched_groups[[i]]

  # Initialize a data frame to store the variable names, their corresponding factor loading values, and matched group values
  df <- data.frame(Variable = ordered_vars, Value = ordered_values, Group = groups)

  # Remove rows with NA group values
  df <- df[complete.cases(df), ]

  # Group by the 'Group' column and calculate the average value for each group
  avg_values <- tapply(df$Value, df$Group, mean)

  # Store the average values in the list
  average_values[[i]] <- avg_values
}

# Iterate over each component
for (i in 1:length(average_values)) {
  cat("Component:", i, "\n")

  # Print the average values for each group
  print(average_values[[i]])
}

#####
# Calculate the absolute values of the factor loadings
abs_loadings <- abs(Lamda_F)

# Order the variables related to each row based on their absolute factor loadings
ordered_indices <- apply(abs_loadings, 1, order, decreasing = TRUE)

# Create an empty list to store the matched group values for each component
matched_groups <- list()

# Iterate over each component
for (i in 1:nrow(Lamda_F)) {
  cat("Variables contributing the most to Lamda_F PC", i, ":\n")

  # Get the ordered variables and their factor loading values for the current component
  ordered_vars <- colnames(Lamda_F)[ordered_indices[i, ]]
  ordered_values <- abs_loadings[i, ordered_indices[i, ]]

  # Initialize a vector to store the matched group values for the current component
  matched_groups[[i]] <- character(length(ordered_vars))

  # Iterate over each variable and match its group value
  for (j in seq_along(ordered_vars)) {
    # Match the variable name in the ng dataframe
    match_index <- match(ordered_vars[j], ng$fred)

    # Check if a match was found
    if (!is.na(match_index)) {
      # Store the matched group value
      matched_groups[[i]][j] <- ng$group[match_index]
    } else {
      # If no match was found, set the group value to NA
      matched_groups[[i]][j] <- NA
    }

    # Print the variable name, factor loading value, and matched group value
    cat(ordered_vars[j], ": ", ordered_values[j], " (Group: ", matched_groups[[i]][j], ")\n")
  }
}

# Create a data frame to store the matched group values for each component
matched_df <- data.frame(matrix(unlist(matched_groups), nrow = length(matched_groups), byrow = TRUE))

# Add column names for the data frame
colnames(matched_df) <- paste0("PC", 1:ncol(matched_df))

# Print the matched group values data frame
print(matched_df)

# Calculate the average values for each group and component
average_values <- lapply(matched_df, function(x) tapply(ordered_values, x, mean))

# Print the average values for each group and component
for (i in seq_along(average_values)) {
  cat("Component:", i, "\n")
  print(average_values[[i]])
}

###################################
############## PYTHON
####################################
#write.csv(ng, file = "data/variable_importance/ng.csv", row.names = TRUE)
#write.csv(abs_loadings, file = "data/variable_importance/abs_lambda_F6.csv", row.names = TRUE)
install.packages("reticulate")
library(reticulate)
getwd()
py_run_file("src/stage2_models/FAVAR/VI_f6.py")





