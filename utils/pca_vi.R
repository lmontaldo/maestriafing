
rm(list = ls())
load("data/Rdata/favar_dfms_output.RData")
libraries=source("utils/load_libraries.R")
source("utils/accuracy_measures.R")

perform_pca <- function(data_s, n_components = NULL) {
  # Convert data_s to a matrix X
  X <- data.matrix(data_s)

  # Calculate mean and standard deviation
  mean_values <- apply(X, 2, mean)
  sd_values <- apply(X, 2, sd)

  # Calculate baricentro
  pp <- matrix(rep(1/nrow(X), nrow(X)))
  cc <- t(X) %*% pp

  # Matriz centrada
  unos <- matrix(rep(1, nrow(X)))
  Xc <- X - unos %*% t(cc)

  # Standardize the centered matrix
  Xce <- scale(Xc, scale = TRUE)

  # Calculate correlation matrix
  correlation_matrix <- var(Xce)

  # Calculate eigenvalues of the correlation matrix
  desc <- eigen(correlation_matrix, symmetric = TRUE)
  desc$values # coincide con (pc_all$sdev)^2 a menos de redondeos numéricos en los últimos siete valores

  # Calculate M1
  M1 <- nrow(Xc) / (nrow(Xc) - 1) * solve(diag(x = apply(Xc, 2, var), ncol(Xc), ncol(Xc)))

  # Calculate D
  D <- diag(x = 1/nrow(Xc), nrow(Xc), nrow(Xc))

  # Calculate global inertia
  iner1 <- rep(0, 1)
  for(i in 1:nrow(Xc)){
    term <- D[i,i] * t(Xc[i,]) %*% M1 %*% Xc[i,]
    iner1 <- iner1 + term
  }
  I1 <- sum(diag(t(Xc) %*% D %*% Xc %*% M1))

  # Perform PCA
  desc1 <- eigen(sqrtm(M1) %*% t(Xc) %*% D %*% Xc %*% sqrtm(M1))

  # Get eigenvalues
  lambda1 <- desc1$values

  # Get eigenvectors
  Ustar <- desc1$vectors

  # Calculate U
  U <- solve(sqrtm(M1)) %*% Ustar

  # Calculate F
  F <- Xc %*% M1 %*% U

  # Determine the number of components to return
  if (!is.null(n_components)) {
    F <- F[, 1:n_components]
  }

  # Calculate squared norm of each factor
  loading_scores <- apply(F, 2, function(x) sum(x^2))

  # Organize loading scores into a dataframe
  loading_df <- data.frame(Factor = paste("Factor", seq_along(loading_scores)), Loading_Score = loading_scores)

  # Sort dataframe by loading score in descending order
  loading_df <- loading_df[order(loading_df$Loading_Score, decreasing = TRUE), ]

  # Return principal components, global inertia, and loading dataframe
  return(list(principal_components = F, global_inertia = I1, loading_df = loading_df))
}


result <- perform_pca(data_s, n_components =7)
principal_components <- result$principal_components
global_inertia <- result$global_inertia
