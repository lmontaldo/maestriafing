rm(list = ls())
libraries=source("utils/load_libraries.R")
library(MASS)
library(kernelshap)
library(viridis)
load("data/Rdata/favar_dfms_output.RData")
load("data/Rdata/ng_dataframe/ng.RData")
load("data/Rdata/variable_importance/profundo.RData")
load("data/Rdata/variable_importance/lineal.RData")
source("utils/accuracy_measures.R")
########################################################################
# KernelSHAP: Practical Shapley Value Estimation via Linear Regression
#########################################################################
f1=F_pseudo_inv_t[,1]
X=as.data.frame(data_s)
fit <- lm(f1 ~ ., data = X)
X_explain <- X
set.seed(1)
bg_X <-X[sample(nrow(X), 118), ]
s <- kernelshap(fit, X_explain, bg_X = bg_X)
abs_S <- apply(s$S, 2, abs)

sum(abs(s$S[,1]))
18.50535/118 # en promedio me deberia dar aproximdada
# Compute the sum of each column
column_sums <- colSums(abs_S)

# Order the column sums in descending order
ordered_sums <- column_sums[order(-column_sums)]
top_15_sums <- rev(top_15_sums)
top_15_names <- rev(top_15_names)
matching_values <- ng$gsi[match(top_15_names, ng$fred)]
################################################################
# Create a horizontal bar plot
barplot(top_15_sums, horiz = TRUE, names.arg = top_15_names,
        main = "Top 15 variables que contribuyen al primer factor", xlab = "Suma de los valores absolutos por columna",
        cex.names = 0.7, las = 1, col =  viridis_pal()(15))
#################################### PLOT F1: 15 VARIABLES MAS IMPORTANTES
# Set the margin to accommodate longer names
par(mar = c(5, 8, 4, 2) + 0.1)
# Create a horizontal bar plot with the matching values as names
barplot(top_15_sums, horiz = TRUE, names.arg = matching_values,
        main = "Top 15 variables que contribuyen al primer factor (F1)",
        xlab = "Suma de los valores absolutos de los valores kernelshap por columna",
        cex.names = 0.7, las = 1, col = color_palette)


############################################################################
###### VI lineal
#################################################################################
load("data/Rdata/ng_dataframe/ng.RData")
class(loadings)
abs_loadings <- abs(loadings)
# Initialize a list to store dataframes
df_list <- list()
# Loop through each row name in the loadings matrix
for (row_name in rownames(loadings)) {
  # Create a dataframe for the current row
  df <- data.frame(variable = colnames(loadings),
                   abs_value = abs(loadings[row_name, ]))

  # Order the dataframe by abs_value in descending order
  df <- df[order(-df$abs_value), ]

  # Assign the row name as the name of the dataframe
  names(df) <- c("variable", "abs_value")
  row.names(df) <- NULL
  df$abs_value=round(df$abs_value,3)
  df_list[[row_name]] <- df
}

# Access a specific dataframe (for example, matriz_fhat1)
f1_vi <- head(df_list[["matriz_fhat1"]],15)
f2_vi <- head(df_list[["matriz_fhat2"]],15)
f3_vi <- head(df_list[["matriz_fhat3"]],15)
f4_vi <- head(df_list[["matriz_fhat4"]],15)
f5_vi <- head(df_list[["matriz_fhat5"]],15)
f6_vi <- head(df_list[["matriz_fhat6"]],15)
#f7_vi <- head(df_list[["matriz_fhat7"]],15)
# View the dataframe
f1_vi
f2_vi
f3_vi
f4_vi
f5_vi
f6_vi
#f7_vi

#########
ng$fred <- gsub("S.P.div.yield", "S&P div yield", ng$fred)
# Create gsi column in f2_vi using matched values from ng$gsi
f1_vi$gsi <- ng$gsi[match(f1_vi$variable, ng$fred)]
f2_vi$gsi <- ng$gsi[match(f2_vi$variable, ng$fred)]
f3_vi$gsi <- ng$gsi[match(f3_vi$variable, ng$fred)]
f4_vi$gsi <- ng$gsi[match(f4_vi$variable, ng$fred)]
f5_vi$gsi <- ng$gsi[match(f5_vi$variable, ng$fred)]
f6_vi$gsi <- ng$gsi[match(f6_vi$variable, ng$fred)]
#f7_vi$gsi <- ng$gsi[match(f7_vi$variable, ng$fred)]
##########
# Function to add ng$group to each dataframe
add_ng_group <- function(df, ng) {
  # Match variable names between dataframe and ng$fred
  match_indices <- match(df$variable, ng$fred)

  # Create new columns for ng$group and ng$gsi
  df$group <- ng$group[match_indices]
  df$gsi <- ng$gsi[match_indices]

  # Return the updated dataframe
  return(df)
}

# Add ng$group and ng$gsi to each dataframe
f1_vi_group <- add_ng_group(f1_vi, ng)
f2_vi_group <- add_ng_group(f2_vi, ng)
f3_vi_group <- add_ng_group(f3_vi, ng)
f4_vi_group <- add_ng_group(f4_vi, ng)
f5_vi_group <- add_ng_group(f5_vi, ng)
f6_vi_group <- add_ng_group(f6_vi, ng)

###############

f1_vi_group$abs_value <- as.numeric(gsub(",", ".", f1_vi_group$abs_value))
# Verify the conversion
print(f1_vi_group$abs_value)





################################################################
# Create a horizontal bar plot
barplot(f1_vi_group$abs_value, horiz = TRUE, names.arg = f1_vi_group$fred,
        main = "Top 15 variables que contribuyen al primer factor", xlab = "Suma de los valores absolutos por columna",
        cex.names = 0.7, las = 1, col =  viridis_pal()(15))
#################################### PLOT F1: 15 VARIABLES MAS IMPORTANTES
# Set the width of the plotting area
options(OutDec = ",") # Change the decimal point character
par(pin = c(8, 4))  # Adjust the width as needed

# Set the margin to accommodate longer names
par(mar = c(5, 4, 4, 2) + 0.1)

# Create a horizontal bar plot with the matching values as names
barplot(f1_vi_group$abs_value, horiz = TRUE, names.arg = f1_vi_group$gsi,
        main = "Top 15 variables que contribuyen al primer factor (F1)",
        xlab = "Suma de los valores absolutos de los valores kernelshap por columna",
        cex.names = 0.7, las = 1)




