rm(list = ls())
libraries=source("utils/load_libraries.R")
source("utils/grupos_variables.R")
source("utils/make_ggplots.R")
library(MASS)
library(kernelshap)
library(viridis)
library(xtable)
library(tibble)
load("data/Rdata/favar_ddfm_input.RData")
load("data/Rdata/ng_dataframe/fred.RData")
load("data/Rdata/variable_importance/profundo.RData")
load("data/Rdata/favar_estimation_results/results_favar_factor_7.RData")
load("data/Rdata/variable_importance/shapley.RData") #"abs_S_1" "abs_S_2" "abs_S_3" "abs_S_4" "abs_S_5" "abs_S_6" "abs_S_7"
###############
# VI profundo #
###############
top15_vi_profundo <- function(abs_S_i, fred) {
  # Calculate column sums
  column_sums <- colSums(abs_S_i)

  # Order column sums
  ordered_sums <- column_sums[order(-column_sums)]

  # Select top 15 sums
  top_15_sums <- ordered_sums[1:15]

  # Create dataframe
  top_15_df <- data.frame(Values = top_15_sums, row.names = names(top_15_sums))

  # Add additional columns
  top_15_df$gsi <- toupper(fred$gsi[match(rownames(top_15_df), fred$fred)])
  top_15_df$descript <-fred$description[match(rownames(top_15_df), fred$fred)]
  top_15_df$group <-fred$grupos[match(rownames(top_15_df), fred$fred)]
  top_15_df$color <-fred$color[match(rownames(top_15_df), fred$fred)]

  return(top_15_df)
}
top15_f1_p <- top15_vi_profundo(abs_S_1, fred)
top15_f2_p <- top15_vi_profundo(abs_S_2, fred)
top15_f3_p <- top15_vi_profundo(abs_S_3, fred)
top15_f4_p <- top15_vi_profundo(abs_S_4, fred)
top15_f5_p <- top15_vi_profundo(abs_S_5, fred)
top15_f6_p <- top15_vi_profundo(abs_S_6, fred)
top15_f7_p <- top15_vi_profundo(abs_S_7, fred)
#################
## Bar plots ####
#################
generate_horizontal_bar_plot(top15_f1_p)
generate_horizontal_bar_plot(top15_f2_p)
generate_horizontal_bar_plot(top15_f3_p)
generate_horizontal_bar_plot(top15_f4_p)
generate_horizontal_bar_plot(top15_f5_p)
generate_horizontal_bar_plot(top15_f6_p)
generate_horizontal_bar_plot(top15_f7_p)
dev.off()
###################
###### VI lineal #
###################
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
  fred_g <- fred$grupos[match(row_names, fred$fred)]
  df$group <- fred_g
  fred_c <- fred$color[match(row_names, fred$fred)]
  df$color <- fred_c
  return(df)
}
# Apply the function to each top15_f data frame
top15_f1 <- add_gsi_column(dataframes[["matriz_fhat1"]], fred)
top15_f2 <- add_gsi_column(dataframes[["matriz_fhat2"]], fred)
top15_f3 <- add_gsi_column(dataframes[["matriz_fhat3"]], fred)
top15_f4 <- add_gsi_column(dataframes[["matriz_fhat4"]], fred)
top15_f5 <- add_gsi_column(dataframes[["matriz_fhat5"]], fred)
top15_f6 <- add_gsi_column(dataframes[["matriz_fhat6"]], fred)
top15_f7 <- add_gsi_column(dataframes[["matriz_fhat7"]], fred)
#################
## Bar plots ####
#################
generate_horizontal_bar_plot(top15_f1)
generate_horizontal_bar_plot(top15_f2)
generate_horizontal_bar_plot(top15_f3)
generate_horizontal_bar_plot(top15_f4)
generate_horizontal_bar_plot(top15_f5)
generate_horizontal_bar_plot(top15_f6)
generate_horizontal_bar_plot(top15_f7)

