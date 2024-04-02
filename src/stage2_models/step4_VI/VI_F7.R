rm(list = ls())
libraries=source("utils/load_libraries.R")
library(MASS)
library(kernelshap)
library(viridis)
library(xtable)
load("data/Rdata/favar_ddfm_output.RData")
load("data/Rdata/ng_dataframe/ng.RData")
data_p=load("data/Rdata/variable_importance/profundo.RData")
data_l=load("data/Rdata/variable_importance/lineal.RData")
source("utils/accuracy_measures.R")
str(load("data/Rdata/variable_importance/profundo.RData"))
load("data/Rdata/variable_importance/shapley.RData")
###################
## colors by goup
###################
distinct_colors_manual <- c("#1f77b4", "#ff7f0e", "#FFDB58", "#d62728", "#9467bd", "#808080", "#e377c2", "#00FFFF")
# Identify unique groups
unique_groups <- unique(fred$group)
color_mapping <- setNames(distinct_colors_manual, unique_groups)
fred$color <- color_mapping[fred$group]

group_color_df <- data.frame(
  group = names(color_mapping),
  color = as.character(color_mapping),
  stringsAsFactors = FALSE
)

# Print the dataframe
print(group_color_df)

########################################################################
# KernelSHAP: Practical Shapley Value Estimation via Linear Regression

######################################
######## F1 no lineal
#########################################
f1=F_pseudo_inv_t[,1]
X=as.data.frame(data_s)
fit <- lm(f1 ~ ., data = X)
X_explain <- X
set.seed(1)
bg_X <-X[sample(nrow(X), 118), ]
s <- kernelshap(fit, X_explain, bg_X = bg_X)
################################ VI
abs_S <- apply(s$S, 2, abs)
#sum(abs(s$S[,1]))
#18.50535/118 # en promedio me deberia dar aproximdada
# Compute the sum of each column
column_sums <- colSums(abs_S)
# Order the column sums in descending order
ordered_sums <- column_sums[order(-column_sums)]
top_15_sums<- ordered_sums[1:15]
top_15_names<- rev(top_15_sums)
matching_values <- rev(toupper(fred$gsi[match(names(top_15_sums), fred$fred)]))

#################################### PLOT F1: 15 VARIABLES MAS IMPORTANTES
layout(matrix(1))
par(mar = c(8, 12, 4, 2) + 0.9)  # Increase margin on the left

# Plotting the barplot
barplot(top_15_names, horiz = TRUE, names.arg = matching_values,
        main = "Top 15 variables que contribuyen al primer factor (F1)",
        xlab = "Suma de los valores absolutos de los valores kernelshap",
        cex.names = 1.1,cex.axis=1.2, las = 1, col = rev(viridis_pal()(15)))
#
##################################################
###### abs_shapley_matrices
####################################################
shapley_values_for_factor <- function(F_pseudo_inv_t, data_s) {
  abs_S_list <- list()  # Create an empty list to store abs_S matrices
  for (i in 1:ncol(F_pseudo_inv_t)) {
    f <- F_pseudo_inv_t[, i]  # Extract the i-th column of F_pseudo_inv_t
    X <- as.data.frame(data_s)  # Convert data_s to a data frame
    fit <- lm(f ~ ., data = X)  # Fit a linear model using all columns of X as predictors

    X_explain <- X  # Set X_explain to X (not sure if you intended to use it later)

    set.seed(1)  # Set seed for reproducibility
    bg_X <- X[sample(nrow(X), 118), ]  # Sample 118 rows from X
    s <- kernelshap(fit, X_explain, bg_X = bg_X)  # Calculate kernelshap values

    abs_S <- apply(s$S, 2, abs)  # Calculate absolute values of shapley values
    abs_S_list[[i]] <- abs_S  # Store abs_S in the list, indexed by the iteration number
  }
  return(abs_S_list)  # Return the list of abs_S matrices
}

abs_shapley_matrices <- shapley_values_for_factor(F_pseudo_inv_t, data_s)
abs_S_1 = abs_shapley_matrices[[1]]
abs_S_2 = abs_shapley_matrices[[2]]
abs_S_3 = abs_shapley_matrices[[3]]
abs_S_4 = abs_shapley_matrices[[4]]
abs_S_5 = abs_shapley_matrices[[5]]
abs_S_6 = abs_shapley_matrices[[6]]
abs_S_7 = abs_shapley_matrices[[7]]

save(
  abs_S_1 ,
  abs_S_2 ,
  abs_S_3,
  abs_S_4 ,
  abs_S_5 ,
  abs_S_6 ,
  abs_S_7 ,
  file = "data/Rdata/variable_importance/shapley.RData"
)

####################################################################
process_abs_S <- function(abs_S, fred) {
  # Calculate column sums of abs_S
  column_sums <- colSums(abs_S)

  # Order the sums and get the top 15
  ordered_sums <- column_sums[order(-column_sums)]
  top_15_sums <- ordered_sums[1:15]
  print(top_15_sums)

  # Reverse the top 15 sums
  top_15_names <- rev(top_15_sums)

  # Get matching values, descriptions, and groups from fred
  matching_values <- rev(toupper(fred$gsi[match(names(top_15_sums), fred$fred)]))
  matching_descrip <- rev(fred$description[match(names(top_15_sums), fred$fred)])
  matching_group <- rev(fred$group[match(names(top_15_sums), fred$fred)])

  # Create a combined data frame
  combined_df <- data.frame(Variable = rev(matching_values),
                            Descripcion = rev(matching_descrip))

  # Return the combined data frame
  return(combined_df)
}
combined_df1 <- process_abs_S(abs_S_1, fred)
combined_df2 <- process_abs_S(abs_S_2, fred)
combined_df3 <- process_abs_S(abs_S_3, fred)
combined_df4 <- process_abs_S(abs_S_4 ,fred)
combined_df5 <- process_abs_S(abs_S_5 ,fred)
combined_df6 <- process_abs_S(abs_S_6, fred)
combined_df7 <- process_abs_S(abs_S_7, fred)
########

xtable(combined_df7, include.rownames = FALSE, caption = "Factor: Variable, descripción y grupo", label="tab:fp1")

xtable(combined_df1, include.rownames = FALSE, caption = "Factor 1: Variable, descripción", label="tab:fp1")
xtable(combined_df2, include.rownames = FALSE, caption = "Factor 2: Variable, descripción", label="tab:fp2")
xtable(combined_df3, include.rownames = FALSE, caption = "Factor 3: Variable, descripción", label="tab:fp3")
xtable(combined_df4, include.rownames = FALSE, caption = "Factor 4: Variable, descripción", label="tab:fp4")
xtable(combined_df5, include.rownames = FALSE, caption = "Factor 5: Variable, descripción", label="tab:fp5")
xtable(combined_df6, include.rownames = FALSE, caption = "Factor 6: Variable, descripción", label="tab:fp6")
xtable(combined_df7, include.rownames = FALSE, caption = "Factor 7: Variable, descripción", label="tab:fp7")






#########################################################
##################################################################################
######## function plot for all the factores in FAVAR profundo
###################################################################################
############################################################
plot_top_contributing_variables <- function(F_pseudo_inv_t, data_s) {
  for (i in 1:ncol(F_pseudo_inv_t)) {
    f <- F_pseudo_inv_t[, i]
    X <- as.data.frame(data_s)
    fit <- lm(f ~ ., data = X)
    X_explain <- X
    set.seed(1)
    bg_X <- X[sample(nrow(X), 118), ]
    s <- kernelshap(fit, X_explain, bg_X = bg_X)
    #################################################
    abs_S <- apply(s$S, 2, abs)
    column_sums <- colSums(abs_S)
    ordered_sums <- column_sums[order(-column_sums)]
    top_15_sums <- ordered_sums[1:15]
    print(top_15_sums)
    top_15_names<- rev(top_15_sums)
    #matching_values <- toupper(fred$gsi[match(names(top_15_sums), fred$fred)])
    matching_values <- rev(toupper(fred$gsi[match(names(top_15_sums), fred$fred)]))
    matching_descrip<- rev(fred$description[match(names(top_15_sums), fred$fred)])
    matching_group<- rev(fred$group[match(names(top_15_sums), fred$fred)])
    matching_color<- rev(fred$color[match(names(top_15_sums), fred$fred)])
    combined_df <- data.frame(Variable=rev(matching_values), Descripcion=rev(matching_descrip), Grupo=rev(matching_group))
    x_table <- xtable(combined_df, caption = "Factor : Variable, descripcion y grupo", include.rownames = FALSE)
    cat('factor', i, '\n')
    print(x_table)
    ####################################################
    layout(matrix(1))
    par(mar = c(8, 14, 4, 2) + 0.9)  # Adjust the margin on the left to accommodate longer names
    barplot(top_15_names, horiz = TRUE, names.arg = matching_values,
            main = paste("Top 15 variables que contribuyen al factor", i),
            xlab = "pesos en valores absolutos",
            cex.main = 2,
            cex.names = 1.5,
            las = 1,
            cex.axis = 2,
            cex.lab=1.5,
            col = matching_color)

  }
}

plot_top_contributing_variables(F_pseudo_inv_t, data_s)
#col = rev(viridis_pal()(15)))
############################################################################
###### VI lineal
#################################################################################
abs_loadings <- abs(loadings)
abs_loadings_matrix <- abs_loadings[-nrow(abs_loadings), ]
lambda_F=t(abs_loadings_matrix)
num_cols <- ncol(lambda_F)
#
dataframes <- list()
for (i in 1:num_cols) {
  column_name <- colnames(lambda_F)[i]
  sorted_values <- sort(lambda_F[, i], decreasing = TRUE)
  selected_values <- sorted_values[1:15]
  dataframe <- data.frame(Values = selected_values)
  dataframes[[column_name]] <- dataframe
}
# List the column names
col_names <- names(dataframes)
col_names
#
add_gsi_column <- function(df, fred) {
  row_names <- rownames(df)
  fred_gsi <- fred$gsi[match(row_names, fred$fred)]
  df$gsi <- fred_gsi
  fred_des <- fred$description[match(row_names, fred$fred)]
  df$descript <- fred_des
  fred_g <- fred$group[match(row_names, fred$fred)]
  df$group <- fred_g
  fred_c <- fred$color[match(row_names, fred$fred)]
  df$color <- fred_c
  return(df)
}
#
# Apply the function to each top15_f data frame
top15_f1 <- add_gsi_column(dataframes[["matriz_fhat1"]], fred)
top15_f2 <- add_gsi_column(dataframes[["matriz_fhat2"]], fred)
top15_f3 <- add_gsi_column(dataframes[["matriz_fhat3"]], fred)
top15_f4 <- add_gsi_column(dataframes[["matriz_fhat4"]], fred)
top15_f5 <- add_gsi_column(dataframes[["matriz_fhat5"]], fred)
top15_f6 <- add_gsi_column(dataframes[["matriz_fhat6"]], fred)
top15_f7 <- add_gsi_column(dataframes[["matriz_fhat7"]], fred)
#
################### ESTE POR LOS COLORES DE GRUPO
################
create_bar_plot <- function(top15_f, factor_index) {
  top_15_names <- rev(toupper(top15_f$gsi))
  matching_values <- rev(top15_f$Values)
  matching_d <- rev(top15_f$descript)
  matching_g <- rev(top15_f$group)
  matching_c<- rev(top15_f$color)

  #####
  layout(matrix(1))
  par(mar = c(8, 14, 4, 2) + 0.9)   # Adjust the margin on the left to accommodate longer names


  barplot(matching_values, horiz = TRUE, names.arg = top_15_names,
          main = paste("Top 15 variables que contribuyen al factor", factor_index),
          xlab = "pesos en valores absolutos",
          cex.main = 2,
          cex.names = 1.5,
          las = 1,
          cex.axis = 2,
          cex.lab=1.5,
          col = matching_c)  # Use color_vector for specifying bar colors
  #####
  table_data <- data.frame(Variable = rev(top_15_names), Descripcion =  rev(matching_d))
  x_table <- xtable(table_data, include.rownames = FALSE,
                    caption = paste("Factor", factor_index, ": Variable, descripción"),
                    label = paste("tab", factor_index, sep = ":fli"))
  print(x_table)

}

#################
# Apply the function to each top15_f data frame
create_bar_plot(top15_f1, 1)
create_bar_plot(top15_f2, 2)
create_bar_plot(top15_f3, 3)
create_bar_plot(top15_f4, 4)
create_bar_plot(top15_f5, 5)
create_bar_plot(top15_f6, 6)
create_bar_plot(top15_f7, 7)
#

#########################
# factores
# f1_l=F_hat[,1]
# f2_l=F_hat[,2]
# f3_l=F_hat[,3]
# f4_l=F_hat[,4]
# f5_l=F_hat[,5]
# f6_l=F_hat[,6]
# f7_l=F_hat[,7]
# plot(F_hat[,1], type="l")
# #
# f1_p=F_pseudo_inv_t[,1]
# f2_p=F_pseudo_inv_t[,2]
# f3_p=F_pseudo_inv_t[,3]
# f4_p=F_pseudo_inv_t[,4]
# f5_p=F_pseudo_inv_t[,5]
# f6_p=F_pseudo_inv_t[,6]
# f7_p=F_pseudo_inv_t[,7]

########## borrar
create_bar_plot <- function(top15_f, factor_index) {
  top_15_names <- rev(toupper(top15_f$gsi))
  matching_values <- rev(top15_f$Values)
  matching_d <- rev(top15_f$descript)
  matching_g <- rev(top15_f$group)

  #####
  layout(matrix(1))
  par(mar = c(8, 14, 4, 2) + 0.9)   # Adjust the margin on the left to accommodate longer names
  barplot(matching_values, horiz = TRUE, names.arg = top_15_names,
          main = paste("Top 15 variables que contribuyen al factor", factor_index),
          xlab = "pesos en valores absolutos",
          cex.main = 1.7,
          cex.names = 1.5,
          las = 1,
          cex.axis = 1.5,
          cex.lab=1.5,
          col = rev(viridis_pal()(15)))
  #####
  table_data <-data.frame(Variable = rev(top_15_names),Descripcion =  rev(matching_d))
  x_table <- xtable(table_data, include.rownames = FALSE,
                    caption = paste("Factor", factor_index, ": Variable, descripción"),
                    label = paste("tab", factor_index, sep = ":fli"))
  print(x_table)

}


