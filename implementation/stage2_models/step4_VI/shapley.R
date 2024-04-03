rm(list = ls())
libraries=source("utils/load_libraries.R")
source("utils/accuracy_measures.R")
library(MASS)
library(kernelshap)
library(viridis)
library(xtable)
load("data/Rdata/input_data_models/favar_ddfm_input.RData")
data_p=load("data/Rdata/variable_importance/profundo.RData")
data_l=load("data/Rdata/variable_importance/lineal.RData")
load("data/Rdata/variable_importance/profundo.RData")
load("data/Rdata/ng_dataframe/fred.RData")
########################################################################
# KernelSHAP: Practical Shapley Value Estimation via Linear Regression
##############################################################################
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

