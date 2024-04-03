rm(list = ls())
libraries=source("utils/load_libraries.R")
library(MASS)
load("data/Rdata/input_data_models/favar_ddfm_input.RData")
load("data/Rdata/ng_dataframe/fred.RData")
source("utils/accuracy_measures.R")
F_hat <- read.csv("data/FAVAR_profundo/f_hat_DDFM_fact5.csv")
#######################################################################
################ F_hat with time index             ####################
#######################################################################

F_hat$Index <- as.Date(F_hat$Index)

# Set the 'Index' column as the index
rownames(F_hat) <- F_hat$Index
F_hat$Index <- NULL  # Remove the 'Index' column from the DataFrame

#######################################################################
################ Moore-Penrose pseudoinvers        ####################
#######################################################################
# Compute the Moore-Penrose pseudoinverse of the factor loading matrix F
F_matrix <- as.matrix(F_hat)
F_pseudoinverse <- ginv(F_matrix)
F_pseudo_inv_t=t(F_pseudoinverse)
rownames(F_pseudo_inv_t)<- rownames(F_matrix)
X=as.matrix(data_s)
moore_penrose_loadings <- F_pseudoinverse %*% X
dim(moore_penrose_loadings)
##################################################
####### IMPULSE-RESPONSE FUNCTIONS
##################################################
data_var <- data.frame(F_pseudo_inv_t, "FEDFUNDS" = data_s[, "FEDFUNDS"])
var_select <- VARselect(data_var, lag.max = 15, type = "both")
best_lag <- var_select$selection
n_lags=best_lag[1]
#
var = VAR(data_var, p =n_lags)
irf_point = irf(var, n.ahead = 48, impulse = "FEDFUNDS", response = "FEDFUNDS", boot = FALSE)
# Shock size of 25 basis points
impulse_sd = 0.25/sd(df_train$FEDFUNDS)
scale = impulse_sd/(irf_point$irf$FEDFUNDS[1]) # position of FYFF response at step 0
# Computing Loading Factors
matriz_s<- as.matrix(data_s)
matriz_fhat<- as.matrix(F_pseudo_inv_t)
reg_loadings = lm(matriz_s ~ 0 + matriz_fhat + data_s[,"FEDFUNDS"])
loadings = reg_loadings$coefficients
#head(reg_loadings$coefficients)
#summary(reg_loadings)
#

Lamda_F=loadings[1:nrow(loadings)-1,]
Lambda_ffr=loadings[nrow(loadings),]
cat("Predictions ahead in test timeframe \n")
predicciones=predict(var, n.ahead = n_forecasts)
vec_list <- list()
for(factor_name in names(predicciones$fcst)) {
  if (startsWith(factor_name, "X")) {
    vec_list[[factor_name]] <- predicciones$fcst[[factor_name]][,1]}}
pred_F <- do.call(cbind, vec_list)
pred_FFR=predicciones$fcst$FEDFUNDS[,1]
F_part=pred_F%*%Lamda_F
Y_part=outer(pred_FFR, Lambda_ffr)
X_pred=F_part+Y_part
X_forec=as.data.frame(X_pred)
predictions_df <- as.data.frame(X_pred)
predictions_xts=xts(predictions_df,
                    order.by = df_test_index)

cat('Accuracy measures \n')
results_df <- compute_accuracy_measures_df(actual_s, predictions_xts)
# print(results_df)
cat("\n Peformance metrics: \n")
averages <- colMeans(results_df, na.rm = TRUE)
print(averages)
