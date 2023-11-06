library(readxl)
library(boot)
library(tsDyn)
library(vars)
library(repr)
library(dplyr)
library(ggplot2)  # Load ggplot2 for plotting

df <- read_csv("../data/prepro/sfr.csv")
slow <- read_csv("../data/prepro/slow_columns.csv")
fast <- read_csv("../data/prepro/fast_columns.csv")
descr <- read.table("../data/prepro/descripciones.txt", header = TRUE, sep = "\t")

data_s <- df[, 2:ncol(df)]
rank_values <- c(3, 5, 10)
results <- list()  # Create a list to store results for all ranks

# Create a directory to save the plots
if (!dir.exists("../docs/figures/")) {
  dir.create("../docs/figures/")
}

cat("\n------ Trying many ranks and assess results: \n")
for (rank_val in rank_values) {
  cat("\n------------------ Results: ------------------------\n")
  cat("Rank =", rank_val, "\n")
  
  # Step 1: Extract principal components of all X (including Y)
  pc_all <- prcomp(data_s, center = FALSE, scale. = FALSE, rank. = rank_val)
  C <- pc_all$x  # Saving the principal components
  
  # Calculate marginal R-squared for each PC
  variances <- sapply(1:rank_val, function(k) {
    sum(pc_all$x[, k]^2)
  })
  total_variance <- sum(pc_all$x^2)
  marginal_r2 <- variances / total_variance
  
  # Scree plot (Line)
  cumulative_var <- cumsum(pc_all$sdev^2) / sum(pc_all$sdev^2)
  scree_data_line <- data.frame(
    PrincipalComponent = 1:length(cumulative_var),
    CumulativeVariance = cumulative_var
  )
  
  p_line <- ggplot(scree_data_line, aes(x = PrincipalComponent, y = CumulativeVariance)) +
    geom_line() +
    geom_point() +
    labs(
      title = paste("Scree Plot (Rank =", rank_val, ")"),
      x = "Principal Component",
      y = "Cumulative Variance Explained"
    ) +
    theme_minimal()
  
  # Save the scree plot (line) as an image file
  filename_line <- paste0("../docs/figures/scree_plot_line_", rank_val, "rank.jpg")
  ggsave(filename_line, p_line, height = 8, width = 12)
  
  # Scree plot (Bar)
  scree_data_bar <- data.frame(
    PrincipalComponent = 1:rank_val,
    MarginalR2 = marginal_r2
  )
  
  p_bar <- ggplot(scree_data_bar, aes(x = PrincipalComponent, y = MarginalR2)) +
    geom_bar(stat = "identity") +
    labs(
      title = paste("Scree Plot (Rank =", rank_val, ")"),
      x = "Principal Component",
      y = "Marginal R-squared"
    ) +
    theme_minimal()
  
  # Save the scree plot (bar) as an image file
  filename_bar <- paste0("../docs/figures/scree_plot_bar_", rank_val, "rank.jpg")
  ggsave(filename_bar, p_bar, height = 8, width = 12)
  
  # Store results in the results list
  results[[as.character(rank_val)]] <- list(
    C = C,
    F_slow = F_slow,
    reg = reg,
    F_hat = F_hat,
    data_var = data_var,
    var = var,
    aic = aic,
    bic = bic
  )
}

cat("\n------ # PCA to keep and VAR results: \n")
# The rest of your code...
