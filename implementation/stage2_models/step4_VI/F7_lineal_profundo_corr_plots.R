rm(list = ls())
libraries=source("utils/load_libraries.R")
library(MASS)
library(kernelshap)
library(viridis)
library(corrplot)
load("data/Rdata/input_data_models/favar_ddfm_input.RData")
load("data/Rdata/ng_dataframe/fred.RData")
data_p=load("data/Rdata/variable_importance/profundo.RData")
data_l=load("data/Rdata/variable_importance/lineal.RData")
source("utils/accuracy_measures.R")
str(load("data/Rdata/variable_importance/profundo.RData"))

############################################################
###########################################################
###### scaled and normalized factors
###########################################################
###########################################################
# lineales
f1_l=F_hat[,1]
f2_l=F_hat[,2]
f3_l=F_hat[,3]
f4_l=F_hat[,4]
f5_l=F_hat[,5]
f6_l=F_hat[,6]
f7_l=F_hat[,7]
fact_lineales <- scale(data.frame(f1_l, f2_l, f3_l, f4_l, f5_l, f6_l, f7_l))
# profundos
data.frame(F_pseudo_inv_t)
f1_p=F_pseudo_inv_t[,1]
f2_p=F_pseudo_inv_t[,2]
f3_p=F_pseudo_inv_t[,3]
f4_p=F_pseudo_inv_t[,4]
f5_p=F_pseudo_inv_t[,5]
f6_p=F_pseudo_inv_t[,6]
f7_p=F_pseudo_inv_t[,7]
fact_profundos <- scale(data.frame(f1_p, f2_p, f3_p, f4_p, f5_p, f6_p, f7_p))
########
# Function to normalize data between -1 and 1
########
normalize_data <- function(df) {
  normalized <- apply(df, 2, function(x) (x - min(x)) / (max(x) - min(x)) * 2 - 1)
  return(normalized)
}

# Normalize both data frames
normalized_fact_lineales <- normalize_data(fact_lineales)
normalized_fact_profundos <- normalize_data(fact_profundos)

########################################################################
########################################################################
# Function to find highest absolute correlation between two data frames
########################################################################
##########################################################################
find_highest_correlation <- function(df1, df2) {
  correlations <- matrix(NA, nrow = ncol(df1), ncol = ncol(df2))

  # Iterate over columns of both data frames
  for (i in 1:ncol(df1)) {
    for (j in 1:ncol(df2)) {
      # Calculate correlation between columns
      correlations[i, j] <- abs(cor(df1[, i], df2[, j]))
    }
  }

  # Find column index with highest correlation for each column in df1
  max_cor_indices <- apply(correlations, 1, which.max)

  # Extract the names of columns from df2 with highest correlations
  max_cor_cols <- colnames(df2)[max_cor_indices]

  # Return a named list of column names
  names(max_cor_cols) <- colnames(df1)

  return(max_cor_cols)
}

# Call the function with your normalized data frames
highest_correlations <- find_highest_correlation(normalized_fact_lineales, normalized_fact_profundos)

# Print the results
print(highest_correlations)

#print(highest_correlations)
#f1_l   f2_l   f3_l   f4_l   f5_l   f6_l   f7_l
#"f6_p" "f1_p" "f2_p" "f4_p" "f3_p" "f5_p" "f6_p"

##########
# Function to find absolute correlations between columns of two data frames
find_correlation_matrix <- function(df1, df2) {
  correlations <- matrix(NA, nrow = ncol(df1), ncol = ncol(df2))

  # Iterate over columns of both data frames
  for (i in 1:ncol(df1)) {
    for (j in 1:ncol(df2)) {
      # Calculate absolute correlation between columns
      correlations[i, j] <- abs(cor(df1[, i], df2[, j]))
    }
  }

  # Set row and column names
  rownames(correlations) <- colnames(df1)
  colnames(correlations) <- colnames(df2)

  return(correlations)
}


# Call the function with your normalized data frames
correlation_matrix <- find_correlation_matrix(normalized_fact_lineales, normalized_fact_profundos)
# Print the correlation matrix
print(round(correlation_matrix,2))

correlation_matrix <- find_correlation_matrix(fact_lineales, fact_profundos)
# Print the correlation matrix
print(round(correlation_matrix,2))
xtable(correlation_matrix, caption='Matríz de correlación de factores escalados')

#################################################################
########## corrplot
#################################################################
find_and_plot_correlation <- function(df1, df2) {
  # Calculate correlations
  correlations <- find_correlation_matrix(df1, df2)

  # Plot correlation matrix with values
  corrplot(correlations, method = 'number',  mar = c(1,1, 0,2)+2,
           tl.col = "black", tl.srt = 45, is.corr=FALSE, tl.cex = 1.9, cl.cex = 1.1,
           number.cex = 1.6,
           number.font = 2,
           #title = "Correlacion absoluta entre factores lineales y profundos",
           col=COL1(sequential = c("Oranges", "Purples", "Reds", "Blues", "Greens",
           "Greys", "OrRd", "YlOrRd", "YlOrBr", "YlGn"), n = 200))
}

find_and_plot_correlation(normalized_fact_lineales, normalized_fact_profundos)

#####################################################
##############################################
# line plot factors lineales and profundos
###############################################
######################################################
f_l=as.data.frame(normalized_fact_lineales)
f_p=as.data.frame(normalized_fact_profundos)
#################### F1
dev.off()
# Plotting the first line with red color and adding legend
plot(f_l$f1_l, type = 'l', col = "red", ylim = range(c(f_l$f1_l, f_p$f7_p)), ylab = "", xlab='', xaxt = "n", cex.axis = 1.3, cex.lab = 1.2)
lines(f_p$f7_p, col = '#00008B')
legend("topright", legend = c("lineal", "profundo"), col = c("red", '#00008B'), lty = 1, cex = 1.5, xpd = TRUE, bty = "n", inset = c(0, 0))


# Determine the number of labels to show on the x-axis
n <- length(rownames(f_l))
label_indices <- seq(1, n, by = max(1, round(n / 10)))
label_values <- rownames(f_l)[label_indices]

# Adding index as labels on x-axis
axis(1, at = label_indices, labels = FALSE)  # Hide original labels
text(label_indices, par("usr")[3] - 0.1, labels = label_values, xpd = TRUE, srt = 45, adj = 1, cex = 1.1)  # Add rotated labels


######################## F2
dev.off()

plot(f_l$f2_l, type = 'l', col = "red", ylim = range(c(f_l$f1_l, f_p$f7_p)),xlab='', ylab = "", xaxt = "n",  cex.axis = 1.3, cex.lab = 1.2)
lines(f_p$f1_p, col = '#00008B')
legend("topright", legend = c("lineal", "profundo"), col = c("red", '#00008B'), lty = 1, cex = 1.5, xpd = TRUE, bty = "n", inset = c(0, 0))

# Determine the number of labels to show on the x-axis
n <- length(rownames(f_l))
label_indices <- seq(1, n, by = max(1, round(n / 10)))
label_values <- rownames(f_l)[label_indices]

# Adding index as labels on x-axis
axis(1, at = label_indices, labels = FALSE)  # Hide original labels
text(label_indices, par("usr")[3] - 0.1, labels = label_values, xpd = TRUE, srt = 45, adj = 1, cex = 1.1)  # Add rotated labels


######################## F3
dev.off()
# Plotting the first line with red color and adding legend
plot(f_l$f3_l, type = 'l', col = "red", ylim = range(c(f_l$f1_l, f_p$f7_p)), xlab='', ylab = "", xaxt = "n",  cex.axis = 1.3, cex.lab = 1.2)
lines(f_p$f2_p, col = '#00008B')
legend("topright", legend = c("lineal", "profundo"), col = c("red", '#00008B'), lty = 1, cex = 1.5, xpd = TRUE, bty = "n", inset = c(0, 0))


# Determine the number of labels to show on the x-axis
n <- length(rownames(f_l))
label_indices <- seq(1, n, by = max(1, round(n / 10)))
label_values <- rownames(f_l)[label_indices]

# Adding index as labels on x-axis
axis(1, at = label_indices, labels = FALSE)  # Hide original labels
text(label_indices, par("usr")[3] - 0.1, labels = label_values, xpd = TRUE, srt = 45, adj = 1,  cex = 1.1)  # Add rotated labels

######################## F4
dev.off()
# Plotting the first line with red color and adding legend
plot(f_l$f4_l, type = 'l', col = "red", ylim = range(c(f_l$f1_l, f_p$f7_p)), xlab='',ylab = "", xaxt = "n", cex.axis = 1.3, cex.lab = 1.2)
lines(f_p$f4_p, col = '#00008B')
legend("topright", legend = c("lineal", "profundo"), col = c("red", '#00008B'), lty = 1, cex = 1.5, xpd = TRUE, bty = "n", inset = c(0, 0))


# Determine the number of labels to show on the x-axis
n <- length(rownames(f_l))
label_indices <- seq(1, n, by = max(1, round(n / 10)))
label_values <- rownames(f_l)[label_indices]

# Adding index as labels on x-axis
axis(1, at = label_indices, labels = FALSE)  # Hide original labels
text(label_indices, par("usr")[3] - 0.1, labels = label_values, xpd = TRUE, srt = 45, adj = 1, cex = 1.1)  # Add rotated labels


################################ F5
dev.off()
# Plotting the first line with red color and adding legend
plot(f_l$f5_l, type = 'l', col = "red", ylim = range(c(f_l$f1_l, f_p$f7_p)), xlab='',ylab = "", xaxt = "n", cex.axis = 1.3, cex.lab = 1.2)
lines(f_p$f3_p, col = '#00008B')
legend("topright", legend = c("lineal", "profundo"), col = c("red", '#00008B'), lty = 1, cex = 1.5, xpd = TRUE, bty = "n", inset = c(0, 0))


# Determine the number of labels to show on the x-axis
n <- length(rownames(f_l))
label_indices <- seq(1, n, by = max(1, round(n / 10)))
label_values <- rownames(f_l)[label_indices]

# Adding index as labels on x-axis
axis(1, at = label_indices, labels = FALSE)  # Hide original labels
text(label_indices, par("usr")[3] - 0.1, labels = label_values, xpd = TRUE, srt = 45, adj = 1, cex = 1.1)  # Add rotated labels


################################ F6
dev.off()
# Plotting the first line with red color and adding legend
plot(f_l$f6_l, type = 'l', col = "red", ylim = range(c(f_l$f1_l, f_p$f7_p)),xlab='', ylab = "", xaxt = "n", cex.axis = 1.3, cex.lab = 1.2)
lines(f_p$f5_p, col = '#00008B')
legend("topright", legend = c("lineal", "profundo"), col = c("red", '#00008B'), lty = 1, cex = 1.5, xpd = TRUE, bty = "n", inset = c(0, 0))


# Determine the number of labels to show on the x-axis
n <- length(rownames(f_l))
label_indices <- seq(1, n, by = max(1, round(n / 10)))
label_values <- rownames(f_l)[label_indices]

# Adding index as labels on x-axis
axis(1, at = label_indices, labels = FALSE)  # Hide original labels
text(label_indices, par("usr")[3] - 0.1, labels = label_values, xpd = TRUE, srt = 45, adj = 1, cex = 1.1)  # Add rotated labels


################################ F7
dev.off()
# Plotting the first line with red color and adding legend
plot(f_l$f7_l, type = 'l', col = "red", ylim = range(c(f_l$f1_l, f_p$f7_p)), xlab='',ylab = "", xaxt = "n", cex.axis = 1.3, cex.lab = 1.2)
lines(f_p$f6_p, col = '#00008B')
legend("topright", legend = c("lineal", "profundo"), col = c("red", '#00008B'), lty = 1, cex = 1.5, xpd = TRUE, bty = "n", inset = c(0, 0))


# Determine the number of labels to show on the x-axis
n <- length(rownames(f_l))
label_indices <- seq(1, n, by = max(1, round(n / 10)))
label_values <- rownames(f_l)[label_indices]

# Adding index as labels on x-axis
axis(1, at = label_indices, labels = FALSE)  # Hide original labels
text(label_indices, par("usr")[3] - 0.1, labels = label_values, xpd = TRUE, srt = 45, adj = 1, cex = 1.1)  # Add rotated labels


#####
write.csv(fact_lineales, "data/VI/fact_lineales.csv", row.names = FALSE)

write.csv(fact_lineales, "data/VI/fact_profundos.csv", row.names = FALSE)

