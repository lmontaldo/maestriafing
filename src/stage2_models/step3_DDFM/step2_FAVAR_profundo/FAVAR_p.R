rm(list = ls())
libraries=source("utils/load_libraries.R")
library(MASS)
load("data/Rdata/favar_dfms_output.RData")
source("utils/accuracy_measures.R")
F_hat <- read.csv("data/FAVAR_profundo/f_hat_DDFM_fact6.csv")
#######################################################################
################ gráfico de los factores estimados ####################
#######################################################################
library(ggplot2)
# Convert Index to Date format
F_hat$Index <- as.Date(F_hat$Index)

# Create the line plot
ggplot(F_hat, aes(x = Index)) +
  geom_line(aes(y = f1, color = "f1")) +
  geom_line(aes(y = f2, color = "f2")) +
  geom_line(aes(y = f3, color = "f3")) +
  geom_line(aes(y = f4, color = "f4")) +
  geom_line(aes(y = f5, color = "f5")) +
  geom_line(aes(y = f6, color = "f6")) +
  scale_color_manual(values = c("f1" = "blue", "f2" = "red", "f3" = "green", "f4" = "orange", "f5" = "purple", "f6" = "black")) +
  labs(title = "Factores estimados con DDFM",
       x = "Index",
       y = "Value") +
  theme_minimal() +
  theme(legend.title = element_blank())

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
Lamda_F=loadings[1:6,]
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



########################################
#### BOOTSTRAPING #######################
########################################
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
################################################
# plots
################################################
transf_cumsum=c(1,5,5,1,1,5,5,5,1,1,5,5,5,1,1,5,1,1,1)
options(repr.plot.width=12, repr.plot.height=8)
par(mfrow=c(5,4),
    mar = c(2, 2, 2, 2))
for(i in variables){
  index = which(variables == i)
  if(transf_cumsum[index] == 5){
    plot(cumsum(IRF[,i]), type ='l',lwd=2, main = variable_names[index],
         ylab= "", xlab="Steps", ylim=range(cumsum(Lower[,i]),cumsum(Upper[,i])),
         cex.main=1, cex.axis=1)
    lines(cumsum(Upper[,i]), lty=2, col="red")
    lines(cumsum(Lower[,i]), lty=2, col="red")
    abline(h=0)
  }
  else{
    plot(IRF[,i], type ='l',lwd=2, main = variable_names[index],
         ylab= "", xlab="Steps", ylim=range((Lower[,i]),(Upper[,i])),
         cex.main=1, cex.axis=1)
    lines((Upper[,i]), lty=2, col="red")
    lines((Lower[,i]), lty=2, col="red")
    abline(h=0)
  }
}

##################################################
####### DESCOMPOSICION DE LA VARIANZA
##################################################
hor=60
irf_points = irf(var, n.ahead = hor,  boot = FALSE)
results = summary(reg_loadings) # the warning comes because of FEDFUNDS
key_nvars = length(variables)
irf_X_pc1 = array(c(0,0), dim=c(hor+1, key_nvars))
irf_X_pc2 = array(c(0,0), dim=c(hor+1, key_nvars))
irf_X_pc3 = array(c(0,0), dim=c(hor+1, key_nvars))
irf_X_pc4 = array(c(0,0), dim=c(hor+1, key_nvars))
irf_X_pc5 = array(c(0,0), dim=c(hor+1, key_nvars))
irf_X_pc6 = array(c(0,0), dim=c(hor+1, key_nvars))
#irf_X_pc7 = array(c(0,0), dim=c(hor+1, key_nvars))
irf_X_ffr = array(c(0,0), dim=c(hor+1, key_nvars))
for(i in 1:key_nvars){
  irf_X_pc1[,i] = irf_points$irf$X1 %*% matrix(loadings[1:nrow(loadings), variables[i]])
  irf_X_pc2[,i] = irf_points$irf$X2 %*% matrix(loadings[1:nrow(loadings), variables[i]])
  irf_X_pc3[,i] = irf_points$irf$X3 %*% matrix(loadings[1:nrow(loadings), variables[i]])
  irf_X_pc4[,i] = irf_points$irf$X4 %*% matrix(loadings[1:nrow(loadings), variables[i]])
  irf_X_pc5[,i] = irf_points$irf$X5 %*% matrix(loadings[1:nrow(loadings), variables[i]])
  irf_X_pc6[,i] = irf_points$irf$X6 %*% matrix(loadings[1:nrow(loadings), variables[i]])
  #irf_X_pc7[,i] = irf_points$irf$f7 %*% matrix(loadings[1:nrow(loadings), variables[i]])
  irf_X_ffr[,i] = (irf_points$irf$FEDFUNDS) %*% matrix(loadings[1:nrow(loadings), variables[i]])
}
# Get the IRFs squared and accumulate them
psi2_pc1 = array(0, dim = key_nvars)
psi2_pc2 = array(0, dim = key_nvars)
psi2_pc3 = array(0, dim = key_nvars)
psi2_pc4 = array(0, dim = key_nvars)
psi2_pc5 = array(0, dim = key_nvars)
psi2_pc6 = array(0, dim = key_nvars)
#psi2_pc7 = array(0, dim = key_nvars)
psi2_ffr = array(0, dim = key_nvars)

for(i in 1:key_nvars){
  for(j in 1:hor){
    psi2_pc1[i] = psi2_pc1[i] + irf_X_pc1[j,i]^2
    psi2_pc2[i] = psi2_pc2[i] + irf_X_pc2[j,i]^2
    psi2_pc3[i] = psi2_pc3[i] + irf_X_pc3[j,i]^2
    psi2_pc4[i] = psi2_pc4[i] + irf_X_pc4[j,i]^2
    psi2_pc5[i] = psi2_pc5[i] + irf_X_pc5[j,i]^2
    psi2_pc6[i] = psi2_pc6[i] + irf_X_pc6[j,i]^2
    #psi2_pc7[i] = psi2_pc7[i] + irf_X_pc7[j,i]^2
    psi2_ffr[i] = psi2_ffr[i] + irf_X_ffr[j,i]^2
  }
}
var_total= array(0, dim = key_nvars)
var_fac= array(0, dim = key_nvars)
var_e= array(0, dim = key_nvars)

for(i in 1:key_nvars){
  var_fac[i] = psi2_pc1[i] + psi2_pc2[i] + psi2_pc3[i] + psi2_pc4[i]+psi2_pc5[i]+psi2_pc6[i]+
    #psi2_pc7[i]+
    psi2_ffr[i]
  var_total[i] = psi2_pc1[i] + psi2_pc2[i] + psi2_pc3[i] +psi2_pc4[i]+psi2_pc5[i]+psi2_pc6[i]+
    #psi2_pc7[i]+
    psi2_ffr[i] + results[[variables[i]]]$sigma^2
  var_e[i] = results[[variables[i]]]$sigma^2
}
table = data.frame("PC1" = round((psi2_pc1),3),
                   "PC2" = round((psi2_pc2),3),
                   "PC3" = round((psi2_pc3),3),
                   "PC4" = round((psi2_pc4),3),
                   "PC5" = round((psi2_pc5),3),
                   "PC6" = round((psi2_pc6),3),
                   #"PC7" = round((psi2_pc7),3),
                   "FEDFUNDS" = round((psi2_ffr),3),
                   "Factor_Y_total" = round(var_fac,3) ,
                   "e" = round((var_e),3),
                   "Total" = round(var_total,3))
row.names(table) = variable_names
#
r2 = array(0, dim = key_nvars)
for(i in 1:key_nvars){
  r2[i] = results[[variables[i]]]$r.squared
}
tableddfm = data.frame("Variables" = variable_names, "Contribution" = round((psi2_ffr/var_total),3), "R-squared" = round(r2,3))
tableddfm$DV=tableddfm["Contribution"]*tableddfm["R.squared"]
xtable(tableddfm, digits=3)
##########################

##########################
# KernelSHAP: Practical Shapley Value Estimation via Linear Regression
##########################
# para F1
f1=F_pseudo_inv_t[,1]
X=as.data.frame(data_s)
fit <- lm(f1 ~ ., data = X)
X_explain <- X
set.seed(1)
bg_X <-X[sample(nrow(X), 118), ]
s <- kernelshap(fit, X_explain, bg_X = bg_X)
sum(abs(s$S[,1]))
18.50535/118 # en promedio me deberia dar aproximdada
# ordernar las variables
