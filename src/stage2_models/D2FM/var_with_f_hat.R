libraries=source("utils/load_libraries.R")
rm(list = ls())
obj=load("data/Rdata/favar_dfms_output.RData")
data <- read.csv("data/ddfm/f_hat_ddfm.csv")
#
data$index <- as.Date(data$index)
xts_object_f <- xts(data[, -which(colnames(data) == "index")], order.by = data$index)
###############################################################################################
data_var <- data.frame(F_hat, "FEDFUNDS" = data_s[, "FEDFUNDS"])
var_select <- VARselect(data_var, lag.max = 15, type = "both")
best_lag <- var_select$selection
n_lags=best_lag[1]
#############################################################################################
# PREDICCIONES
var = VAR(data_var, p =n_lags)
matriz_s<- as.matrix(data_s)
matriz_fhat<- as.matrix(F_hat)
reg_loadings = lm(matriz_s ~ 0 + matriz_fhat + data_s[,"FEDFUNDS"])
print(dim(matriz_fhat))
loadings = reg_loadings$coefficients
Lamda_F=loadings[1:7,]
Lambda_ffr=loadings[nrow(loadings),]
predicciones=predict(var, n.ahead = n_forecasts)
vec_list <- list()
for(factor_name in names(predicciones$fcst)) {
  if (startsWith(factor_name, "PC")) {
    vec_list[[factor_name]] <- predicciones$fcst[[factor_name]][,1]
  }
}

pred_F <- do.call(cbind, vec_list)
pred_FFR=predicciones$fcst$FEDFUNDS[,1]
F_part=pred_F%*%Lamda_F
Y_part=outer(pred_FFR, Lambda_ffr)
X_pred=F_part+Y_part
X_forec=as.data.frame(X_pred)
predictions_df <- as.data.frame(X_pred)

predictions_xts=xts(predictions_df,
                    order.by = df_test_index)

# Desempeño
compute_accuracy_measures_df <- function(actual_df, predictions_df) {
  # Check if inputs are xts or zoo objects
  if(!("xts" %in% class(actual_df) | "zoo" %in% class(actual_df)) ||
     !("xts" %in% class(predictions_df) | "zoo" %in% class(predictions_df))) {
    stop("Both actual_df and predictions_df must be xts or zoo objects.")
  }

  # Align the time index of predictions_df to that of actual_df
  index(predictions_df) <- index(actual_df)

  # Ensure dimensions match
  if(ncol(actual_df) != ncol(predictions_df) || nrow(actual_df) != nrow(predictions_df)) {
    stop("Dimensions of actual and predicted data must match after index alignment.")
  }

  measures_list <- list()

  for(i in 1:ncol(actual_df)) {
    actual <- actual_df[, i]
    predicted <- predictions_df[, i]

    # MAE
    mae <- mean(abs(actual - predicted), na.rm = TRUE)

    # MSE
    mse <- mean((actual - predicted)^2, na.rm = TRUE)

    # Scaled MSE
    std_predicted <- sd(predicted)
    scaled_mse <- mse / std_predicted

    # RMSFE (Root Mean Squared Forecast Error)
    rmsfe <- sqrt(mse)

    # Store in list
    measures_list[[colnames(actual_df)[i]]] <- c(MAE = mae, MSE = mse, ScaledMSE = scaled_mse, RMSFE = rmsfe)
  }

  # Convert the list to a dataframe
  results_df <- do.call(rbind, measures_list)
  rownames(results_df) <- colnames(actual_df)
  return(results_df)
}

# Usage:
results_df <- compute_accuracy_measures_df(actual_s, predictions_xts)
#results_df
cat("\nMétricas promedio de desempeño: \n")
averages <- colMeans(results_df, na.rm = TRUE)
print(averages)
#filename <- paste0("data/Rdata/results_favar_factor_", factor, ".RData")
# Save objects to that file
#save(reg_loadings,data_var,n_lags, F_hat,var,Lamda_F,Lambda_ffr,pred_F,pred_FFR,F_part, Y_part, predictions_xts,   file = filename)


#######################################################################################
# FIRS Y DV
irf_point = irf(var, n.ahead = 48, impulse = "FEDFUNDS", response = "FEDFUNDS", boot = FALSE)
# Shock size of 25 basis points
impulse_sd = 0.25/sd(df_train$FEDFUNDS)
scale = impulse_sd/(irf_point$irf$FEDFUNDS[1]) # position of FYFF response at step 0
# Computing Loading Factors
matriz_s<- as.matrix(data_s)
matriz_fhat<- as.matrix(F_hat)
reg_loadings = lm(matriz_s ~ 0 + matriz_fhat + data_s[,"FEDFUNDS"])
loadings = reg_loadings$coefficients
##############################################################################################
#### BOOTSTRAPING ########

R = 500 # Number of simulations
nvars = dim(data_s)[2] # Number of variables
nsteps = 49 # numbers of steps
IRFs = array(c(0,0,0), dim = c(nsteps,nvars,R))
var = lineVar(data_var, lag = best_lag[1], include = "const")
for(j in 1:R){
    data_boot = VAR.boot(var, boot.scheme ="resample")
    var_boot = VAR(data_boot, lag = best_lag[1])
    irf1 = irf(var_boot, n.ahead = 48, impulse = "FEDFUNDS", boot = FALSE)
    for(i in 1:nvars){
    IRFs[,i,j] = (irf1$irf$FEDFUNDS %*% matrix(loadings[, i]))*scale
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
options(repr.plot.width=1000, repr.plot.height=1000)
par(mfrow=c(5,4),
mar = c(2, 2, 2, 2))
for(i in variables){
    index = which(variables == i)
    if(transf_code[index] == 5){
    plot(cumsum(IRF[,i]), type ='l',lwd=2, main = variable_names[index],
    ylab= "", xlab="Steps", ylim=range(cumsum(Lower[,i]),cumsum(Upper[,i])),
    cex.main=2, cex.axis=1)
    lines(cumsum(Upper[,i]), lty=2, col="red")
    lines(cumsum(Lower[,i]), lty=2, col="red")
    abline(h=0)
    }
    else{
    plot(IRF[,i], type ='l',lwd=2, main = variable_names[index],
    ylab= "", xlab="Steps", ylim=range((Lower[,i]),(Upper[,i])),
    cex.main=2, cex.axis=1)
    lines((Upper[,i]), lty=2, col="red")
    lines((Lower[,i]), lty=2, col="red")
    abline(h=0)
    }
}
# Get the VAR point estimates
hor=60
irf_points = irf(var, n.ahead = hor,  boot = FALSE)
irf_points$response
# Get IRFs for all of X we are interested in, Dimensions: (hor, key_nvars)
# Find loadings
results = summary(reg_loadings) # the warning comes because of FEDFUNDS
key_nvars = length(variables)
#
irf_X_pc1 = array(c(0,0), dim=c(hor+1, key_nvars))
irf_X_pc2 = array(c(0,0), dim=c(hor+1, key_nvars))
irf_X_pc3 = array(c(0,0), dim=c(hor+1, key_nvars))
irf_X_pc4 = array(c(0,0), dim=c(hor+1, key_nvars))
irf_X_pc5 = array(c(0,0), dim=c(hor+1, key_nvars))
irf_X_pc6 = array(c(0,0), dim=c(hor+1, key_nvars))
irf_X_pc7 = array(c(0,0), dim=c(hor+1, key_nvars))
irf_X_ffr = array(c(0,0), dim=c(hor+1, key_nvars))
for(i in 1:key_nvars){
  irf_X_pc1[,i] = irf_points$irf$PC1 %*% matrix(loadings[1:nrow(loadings), variables[i]])
  irf_X_pc2[,i] = irf_points$irf$PC2 %*% matrix(loadings[1:nrow(loadings), variables[i]])
  irf_X_pc3[,i] = irf_points$irf$PC3 %*% matrix(loadings[1:nrow(loadings), variables[i]])
  irf_X_pc4[,i] = irf_points$irf$PC4 %*% matrix(loadings[1:nrow(loadings), variables[i]])
  irf_X_pc5[,i] = irf_points$irf$PC5 %*% matrix(loadings[1:nrow(loadings), variables[i]])
  irf_X_pc6[,i] = irf_points$irf$PC6 %*% matrix(loadings[1:nrow(loadings), variables[i]])
  irf_X_pc7[,i] = irf_points$irf$PC7 %*% matrix(loadings[1:nrow(loadings), variables[i]])
  irf_X_ffr[,i] = (irf_points$irf$FEDFUNDS) %*% matrix(loadings[1:nrow(loadings), variables[i]])
}
# Get the IRFs squared and accumulate them
psi2_pc1 = array(0, dim = key_nvars)
psi2_pc2 = array(0, dim = key_nvars)
psi2_pc3 = array(0, dim = key_nvars)
psi2_pc4 = array(0, dim = key_nvars)
psi2_pc5 = array(0, dim = key_nvars)
psi2_pc6 = array(0, dim = key_nvars)
psi2_pc7 = array(0, dim = key_nvars)
psi2_ffr = array(0, dim = key_nvars)

for(i in 1:key_nvars){
  for(j in 1:hor){
    psi2_pc1[i] = psi2_pc1[i] + irf_X_pc1[j,i]^2
    psi2_pc2[i] = psi2_pc2[i] + irf_X_pc2[j,i]^2
    psi2_pc3[i] = psi2_pc3[i] + irf_X_pc3[j,i]^2
    psi2_pc4[i] = psi2_pc4[i] + irf_X_pc4[j,i]^2
    psi2_pc5[i] = psi2_pc5[i] + irf_X_pc5[j,i]^2
    psi2_pc6[i] = psi2_pc6[i] + irf_X_pc6[j,i]^2
    psi2_pc7[i] = psi2_pc7[i] + irf_X_pc7[j,i]^2
    psi2_ffr[i] = psi2_ffr[i] + irf_X_ffr[j,i]^2
  }
}
var_total= array(0, dim = key_nvars)
var_fac= array(0, dim = key_nvars)
var_e= array(0, dim = key_nvars)

for(i in 1:key_nvars){
  var_fac[i] = psi2_pc1[i] + psi2_pc2[i] + psi2_pc3[i] + psi2_pc4[i]+psi2_pc5[i]+psi2_pc6[i]+psi2_pc7[i]+psi2_ffr[i]
  var_total[i] = psi2_pc1[i] + psi2_pc2[i] + psi2_pc3[i] +psi2_pc4[i]+psi2_pc5[i]+psi2_pc6[i]+psi2_pc7[i]+ psi2_ffr[i] + results[[variables[i]]]$sigma^2
  var_e[i] = results[[variables[i]]]$sigma^2
}
table = data.frame("PC1" = round((psi2_pc1),3),
                   "PC2" = round((psi2_pc2),3),
                   "PC3" = round((psi2_pc3),3),
                   "PC4" = round((psi2_pc4),3),
                   "PC5" = round((psi2_pc5),3),
                   "PC6" = round((psi2_pc6),3),
                   "PC7" = round((psi2_pc7),3),
                   "FEDFUNDS" = round((psi2_ffr),3),
                   "Factor_Y_total" = round(var_fac,3) ,
                   "e" = round((var_e),3),
                   "Total" = round(var_total,3))
row.names(table) = variable_names
xtable(table, digits=2)
#
r2 = array(0, dim = key_nvars)
for(i in 1:key_nvars){
  r2[i] = results[[variables[i]]]$r.squared
}
table2 = data.frame("Variables" = variable_names, "Contribution" = round((psi2_ffr/var_total),3), "R-squared" = round(r2,3))
xtable(table2, digits=3)
