rm(list = ls())
libraries=source("utils/load_libraries.R")
library(MASS)
library(kernelshap)
library(viridis)
load("data/Rdata/favar_ddfm_output.RData")
load("data/Rdata/ng_dataframe/ng.RData")
data_p=load("data/Rdata/variable_importance/profundo.RData")
data_l=load("data/Rdata/variable_importance/lineal.RData")
source("utils/accuracy_measures.R")
str(load("data/Rdata/variable_importance/profundo.RData"))
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
matching_values <- toupper(fred$gsi[match(names(top_15_sums), fred$fred)])
#################################### PLOT F1: 15 VARIABLES MAS IMPORTANTES
dev.off()
layout(matrix(1))
par(mar = c(8, 5, 4, 2) + 0.9)  # Increase margin on the left

# Plotting the barplot
barplot(top_15_names, horiz = TRUE, names.arg = matching_values,
        main = "Top 15 variables que contribuyen al primer factor (F1)",
        xlab = "Suma de los valores absolutos de los valores kernelshap por columna",
        cex.names = 0.7, las = 1, col = rev(viridis_pal()(15)))
#
max_label_width <- max(strwidth(top_15_names))
plot_width <- max_label_width * 0.7  # Adjust multiplier as needed

# Update plot margin to accommodate longer labels
par(mar = c(8, 5, 4, 2) + c(0, max_label_width * 0.9, 0, 0))

# Plotting the barplot with adjusted width
barplot(top_15_names, horiz = TRUE, names.arg = matching_values,
        main = "Top 15 variables que contribuyen al primer factor (F1)",
        xlab = "Suma de los valores absolutos de los valores kernelshap por columna",
        cex.names = 0.6, las = 1, col = rev(viridis_pal()(15)),
        width = plot_width)

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
    top_15_names<- rev(top_15_sums)
    matching_values <- toupper(fred$gsi[match(names(top_15_sums), fred$fred)])  # Assuming fred is defined
    ####################################################
    layout(matrix(1))
    par(mar = c(8, 10, 4, 2) + 0.3)  # Adjust the margin on the left to accommodate longer names
    barplot(top_15_names, horiz = TRUE, names.arg = matching_values,
            main = paste("Top 15 variables que contribuyen al factor", i),
            xlab = "Suma de los valores absolutos de los valores kernelshap por columna",
            cex.names = 1, las = 1, col = rev(viridis_pal()(15)))
  }
}



plot_top_contributing_variables(F_pseudo_inv_t, data_s)

############################################################################
###### VI lineal
#################################################################################
abs_loadings <- abs(loadings)
abs_loadings_matrix <- abs_loadings[-nrow(abs_loadings), ]
lambda_F=t(abs_loadings_matrix)
#
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
create_bar_plot <- function(top15_f, factor_index) {
  top_15_names <- top15_f$gsi
  matching_values <- toupper(rev(top15_f$Values))

  layout(matrix(1))
  par(mar = c(8, 10, 4, 2) + 0.1)  # Adjust the margin on the left to accommodate longer names

  barplot(matching_values, horiz = TRUE, names.arg = top_15_names,
          main = paste("Top 15 variables que contribuyen al factor", factor_index),
          xlab = "pesos en valores absolutos",
          cex.names = 1, las = 1, col = rev(viridis_pal()(15)))
}

# Apply the function to each top15_f data frame
create_bar_plot(top15_f1, 1)
create_bar_plot(top15_f2, 2)
create_bar_plot(top15_f3, 3)
create_bar_plot(top15_f4, 4)
create_bar_plot(top15_f5, 5)
create_bar_plot(top15_f6, 6)
create_bar_plot(top15_f7, 7)
#
# factores
f1_l=F_hat[,1]
f2_l=F_hat[,2]
f3_l=F_hat[,3]
f4_l=F_hat[,4]
f5_l=F_hat[,5]
f6_l=F_hat[,6]
f7_l=F_hat[,7]
plot(F_hat[,1], type="l")
#
f1_p=F_pseudo_inv_t[,1]
f2_p=F_pseudo_inv_t[,2]
f3_p=F_pseudo_inv_t[,3]
f4_p=F_pseudo_inv_t[,4]
f5_p=F_pseudo_inv_t[,5]
f6_p=F_pseudo_inv_t[,6]
f7_p=F_pseudo_inv_t[,7]




