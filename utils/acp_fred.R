##########
rm(list=ls())
## import Data set
#serf <- read.csv("C://Users/marco.scavino/Documents/PCA/sfr_train.csv", header = TRUE, dec=".")

## Duarte - inicio
library(readxl)
serf1 <- read_excel("C://Users/marco.scavino/Documents/PCA/bbe_data.xlsx")
class(serf1)
dim(serf1) # 511 121
data_s <- scale(serf1[,2:121], center = TRUE, scale = TRUE)
apply(data_s,2,mean)
apply(data_s,2,sd)
pc_all = prcomp(data_s, center=FALSE, scale.=FALSE, rank. = 4) 
objects(pc_all)
# [1] "center"   "rotation" "scale"    "sdev"     "x"   

## Duarte - fin

Date <- which(colnames(serf1) == "Date")
serf2 <- serf1[,-Date]
class(serf2)
dim(serf2) # 511 120
X <- data.matrix(serf2)
apply(X,2,mean) # coincide con pc_all$center
apply(X,2,sd) # coincide con pc_all$scale

## Estandarización de los datos
## baricentro
pp <- matrix(rep(1/nrow(X),nrow(X))) # 511 X 1
cc <- t(X)%*%pp  # 120 X 1

unos <- matrix(rep(1,nrow(X)))
## matriz centrada 
Xc <- X - unos%*%t(cc)  # 511 X 120 Xc contiene la matrix centrada 
round(apply(Xc,2,mean),6)

# estandarizar la matriz centrada
Xce <- scale(Xc, scale = TRUE) # 511 X 120 Xc contiene la matrix estandarizada
var(Xce) # matriz de correlación 

desc <- eigen(var(Xce), symmetric = TRUE) 
desc$values # coincide con (pc_all$sdev)^2 a menos de redondeos numéricos en los últimos siete valores

### Análisis de componentes principales en el espacio de los individuos
## (Xc, M1, D)

# la métrica M1 está definida a través de los inversos de las varianzas
M1 <- nrow(Xc)/(nrow(Xc)-1)*solve(diag(x= apply(Xc,2,var),ncol(Xc), ncol(Xc)))
M1
D <- diag(x = 1/nrow(Xc), nrow(Xc), nrow(Xc))

iner1 <- rep(0,1)
# Inercia global 
for(i in 1:nrow(Xc)){
  term <- D[i,i]*t(Xc[i,])%*%M1%*%Xc[i,]
  iner1 <- iner1 + term
}
iner1
# Inercia global = traza (X^T D X M1)
I1 <- sum(diag(t(Xc)%*%D%*%Xc%*%M1))
I1

library(expm)
desc1 <- eigen(sqrtm(M1)%*%t(Xc)%*%D%*%Xc%*%sqrtm(M1))

lambda1 <- desc1$values # valores propios de (X^T D X M1) ordenados de mayor a menor
lambda1 # (serf2_pca$sdev)^2
sum(lambda1) # 119
cumsum(lambda1/sum(lambda1))

Ustar <- desc1$vectors
Ustar  # coincide con el output pc_all$rotation de prcomp (a menos de cambios de signo)
round(t(Ustar)%*%M1%*%Ustar,6)
U <- solve(sqrtm(M1)) %*% Ustar
U
round(t(U)%*%M1%*%U,6) # las columnas de U constituyen un sistema (base) ortonormal

F <- Xc%*%M1%*%U # Cada columna de F contiene una COMPONENTE PRINCIPAL (FACTOR)
# La primera columna de F, F[,1] contiene las proyecciones de las 24 atletas 
# en el primer eje de inercia, ...
round(F,6) # 577 X 119
# Se verifica que las normas al cuadrado de las componentes principales 
# F[,j], j=1,...7,
# en la métrica D son iguales a los valores propios:
t(F[,1])%*%D%*%F[,1] # 17.58163
t(F[,2])%*%D%*%F[,2] # 8.45622
t(F[,3])%*%D%*%F[,3] # 7.655948  ...
sum(diag(t(F)%*%D%*%F)) # 119
