rm(list = ls())
#load("data/Rdata/favar_dfms_output.RData")
libraries=source("utils/load_libraries.R")
source("utils/accuracy_measures.R")

#
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

  # Print eigenvalues
  # cat("Eigenvalues:\n")
  # print(round(desc$values))

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

  # Print global inertia
  # cat("Global inertia:\n")
  # print(I1)



  # Perform PCA
  desc1 <- eigen(sqrtm(M1) %*% t(Xc) %*% D %*% Xc %*% sqrtm(M1))

  # Get eigenvalues
  lambda1 <- desc1$values

  # Print eigenvalues

  # cat("Eigenvalues (lambda1): \n")
  # print(lambda1)

  # Cumulative sum of eigenvalues
  cumulative_eigenvalues <- cumsum(lambda1 / sum(lambda1))

  # Print cumulative sum of eigenvalues

  # cat("Cumulative sum of eigenvalues: \n")
  # print(cumulative_eigenvalues)


  # Get eigenvectors
  Ustar <- desc1$vectors

  # Calculate U
  U <- solve(sqrtm(M1)) %*% Ustar

  # Calculate F
  F <- Xc %*% M1 %*% U

  # Print F

  # cat("F:\n")
  # print(round(F, 6))

  # Verify norms
  # cat("Norms of the principal components:\n")
  # print(t(F[,1]) %*% D %*% F[,1])
  # print(t(F[,2]) %*% D %*% F[,2])
  # print(t(F[,3]) %*% D %*% F[,3])
  # print(sum(diag(t(F) %*% D %*% F)))


  # Determine the number of components to return
  if (!is.null(n_components)) {
    F <- F[, 1:n_components]
  }

  # Return principal components and global inertia
  return(list(principal_components = F, global_inertia = I1))
}

# Example usage:

#result <- perform_pca(data_s, n_components =7)
#principal_components <- result$principal_components
#global_inertia <- result$global_inertia

