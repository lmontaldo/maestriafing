library(readxl)
library(boot)
library(tsDyn)
library(vars)
library(repr)
library(dplyr)
df <- read_csv("../data/prepro/sfr.csv")
slow <- read_csv("../data/prepro/slow_columns.csv")
fast <- read_csv("../data/prepro/fast_columns.csv")
descr <- read.table("../data/prepro/descripciones.txt", header = TRUE, sep = "\t")
#
data_s <- df[, 2:ncol(df)]
rank_values <- c(3, 5, 10)
results <- list()  # Create a list to store results for all ranks
cat("\n------ Trying many ranks and assess results: \n")
for (rank_val in rank_values) {
    cat("\n------------------ Results: ------------------------\n")
    cat("Rank =", rank_val, "\n")
    # Step 1: Extract principal components of all X (including Y)
    pc_all <- prcomp(data_s, center = FALSE, scale. = FALSE, rank. = rank_val)
    C <- pc_all$x  # Saving the principal components
    slow_vars <- unlist(slow$slow)
    data_slow <- data_s[, slow_vars]
    pc_slow <- prcomp(data_slow, center = FALSE, scale. = FALSE, rank. = rank_val)
    F_slow <- pc_slow$x
    fedfunds <- as.matrix(data_s[, "FEDFUNDS"])
    reg <- lm(C ~ F_slow + fedfunds)
    F_hat <- C - data.matrix(data_s[, "FEDFUNDS"]) %*% reg$coefficients[5,]
    
    # Step 4: Estimate FAVAR and get IRFs
    data_var <- data.frame(F_hat, "FEDFUNDS" = data_s[, "FEDFUNDS"])
    var_select <- VARselect(data_var, lag.max = 15, type = "both")
    best_lag <- var_select$selection
    best_model <- var_select$criteria
    
    cat("Best # lags according to AIC:", best_lag[1], "\n")
    cat("Best # lags according to FPE:", best_lag[4], "\n")
    
    # Fit the VAR model with the determined lag
    var <- VAR(data_var, p = best_lag[1], ic = "AIC")
    aic <- AIC(var)
    bic <- BIC(var)
    
    cat("Fit VAR with best number of lags and return information criteria: \n")
    cat("AIC:", aic, "\n")
    cat("BIC:", bic, "\n")
    
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
best_rank <- rank_values[which.min(sapply(results, function(result) result$aic))]
cat("Best rank according to min AIC:", best_rank, "\n")
var_rank3 <- results[[as.character(best_rank)]]$var
data_var_rank3 <- results[[as.character(best_rank)]]$data_var
F_hat_rank3 <- results[[as.character(best_rank)]]$F_hat
irf_point = irf(var_rank3, n.ahead = 48, impulse = "FEDFUNDS", response = "FEDFUNDS", boot = FALSE)
# Shock size of 25 basis points
impulse_sd = 0.25/sd(df$FEDFUNDS)
scale = impulse_sd/(irf_point$irf$FEDFUNDS[1]) # position of FYFF response at step 0
# Computing Loading Factors
matriz_s<- as.matrix(data_s)
matriz_fhat<- as.matrix(F_hat_rank3)
reg_loadings = lm(matriz_s ~ 0 + matriz_fhat + data_s$FEDFUNDS)
loadings = reg_loadings$coefficients
#### BOOTSTRAPING ########
R = 500 # Number of simulations
nvars = dim(data_s)[2] # Number of variables
nsteps = 49 # numbers of steps
IRFs = array(c(0,0,0), dim = c(nsteps,nvars,R))
var_3 = lineVar(data_var_rank3, lag = 5, include = "const")

for(j in 1:R){    
    data_boot = VAR.boot(var_3, boot.scheme ="resample")
    var_boot = VAR(data_boot, lag = 5)
    irf1 = irf(var_boot, n.ahead = 48, impulse = "FEDFUNDS", boot = FALSE)
    for(i in 1:nvars){
        IRFs[,i,j] = (irf1$irf$FEDFUNDS %*% matrix(loadings[1:4, i]))*scale
        }
} ## Boot simulations done

# Extract the quantiles of IRFs we are interested: 90% confidence intervals in BBE
Upper = array(c(0,0), dim = c(nsteps, nvars))
for(k in 1:nsteps){
    for(i in 1:nvars){
        Upper[k,i] = quantile(IRFs[k,i,], probs = c(0.95))[1]
        }
}
Lower = array(c(0,0), dim = c(nsteps, nvars))
for(k in 1:nsteps){
    for(i in 1:nvars){
        Lower[k,i] = quantile(IRFs[k,i,], probs = c(0.05))[1]
        }
}
IRF = array(c(0,0), dim = c(nsteps, nvars))
for(k in 1:nsteps){
    for(i in 1:nvars){
        IRF[k,i] = quantile(IRFs[k,i,], probs = c(0.5))[1]
        }
}
rm(var_boot)
rm(IRFs)
#
print("\n------ IRF plots: \n")
cols_d<-c("fred", "description")
var_descr<-descr[,cols_d]
# Get the column names of data_s
data_s_column_names <- colnames(data_s)
# Subset var_descr to keep only matching rows
var_descr_subset <- var_descr[var_descr$fred %in% data_s_column_names, ]
print(var_descr_subset)
# Print the resulting var_descr_subset dataframe
print(head(data_s))
data_s_ordered <- data_s[, c("FEDFUNDS", setdiff(names(data_s), c("FEDFUNDS")))]
print(dim(data_s_ordered))
#"FEDFUNDS", "CUSR0000SAC", "TB3MS","GS5",  "EXJPUSx", "M1SL", "M2SL", "EXJPUSx", "CUSR0000SAC", "CUSR0000SA0L5","CPIMEDSL", 
#"CUMFNS",  "PCEPI", "DDURRG3M086SBEA", "DNDGRG3M086SBEA"