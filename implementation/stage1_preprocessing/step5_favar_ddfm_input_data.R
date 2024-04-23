#
rm(list = ls())
libraries=source("utils/load_libraries.R")
source("utils/grupos_variables.R")
library(zoo)
cat("My Working directory is: ", getwd(), "\n")
df_train <- read_csv("data/train_test/sfr_train.csv", show_col_types = FALSE)
df_test <- read_csv("data/train_test/sfr_test.csv", show_col_types = FALSE)
slow <- read_csv("data/prepro/slow_variables.csv", show_col_types = FALSE)
#fast <- read_csv("../../data/prepro/fast_columns.csv", show_col_types = FALSE)
#escr <- read.table("../../data/prepro/descripciones.txt", header = TRUE, sep = "\t")
################################################
# Creación de objetos xts ######################
################################################
df_train$index <- as.Date(df_train$index)
xts_object_train <- xts(df_train[, -which(colnames(df_train) == "index")], order.by = df_train$index)
data_s = scale(xts_object_train, center = TRUE, scale = TRUE)
#cat("Rango de datos:", as.character(range(index(xts_object))), "\n")
#cat("Tamaño de mi muestra de entrenamiento:", dim(data_s), "\n")
#
df_test$index <- as.Date(df_test$index)
xts_object_test <- xts(df_test[, -which(colnames(df_test) == "index")], order.by = df_test$index)
actual_s = scale(xts_object_test, center = TRUE, scale = TRUE)
df_test_index=df_test$index
# Number of forecast steps
n_forecasts = dim(actual_s)[1]
######################################################################
# Cantidad óptima de factores #######################################
#####################################################################
ics = ICr(data_s)
ic_p2_factors=ics$r.star[2]
###########################################################################################################################################
# Tomo las variables como en in https://jbduarte.com/blog/time%20series/r/favar/2020/04/24/FAVAR-Replication.html#Step-4:-Estimate-FAVAR-and-get-IRFs
###########################################################################################################################################
colnames(data_s)[93] <- "S&P div yield"
variables = c(grep("^FEDFUNDS$", colnames(data_s)),#Fed Funds Rate
              grep("^INDPRO$", colnames(data_s)), #IP Index
              grep("^CPIAUCSL$", colnames(data_s)), #CPI : All Items
              grep("^TB3MS$", colnames(data_s)), #3-Month Treasury Bill:
              grep("^GS5$", colnames(data_s)), #5-Year Treasury Rate
              grep("^M1SL$", colnames(data_s)),# M1 Money Stock
              grep("^M2SL$", colnames(data_s)), #M2 Money Stock
              grep("^EXJPUSx$", colnames(data_s)), #Japan / U.S. Foreign Exchange Rate
              grep("^CUSR0000SAC$", colnames(data_s)),#CPI : Commodities
              grep("^CUMFNS$", colnames(data_s)),#Capacity Utilization: Manufacturing
              grep("^DPCERA3M086SBEA$", colnames(data_s)),#Real personal consumption expenditures
              grep("^DDURRG3M086SBEA$", colnames(data_s)), #Personal Cons. Exp: Durable goods
              grep("^DNDGRG3M086SBEA$", colnames(data_s)), #Personal Cons. Exp: Nondurable goods
              grep("^UNRATE$", colnames(data_s)), #Civilian Unemployment Rate
              grep("^CE16OV$", colnames(data_s)), #Civilian Employment
              grep("^CES0600000008$", colnames(data_s)), #Avg Hourly Earnings : Goods-Producing
              grep("^HOUST$", colnames(data_s)),	#Housing Starts: Total New Privately Owned
              grep("^AMDMNOx$", colnames(data_s)), #New Orders for Durable Goods
              grep("^S&P div yield$", colnames(data_s))#S&P s Composite Common Stock: Dividend Yield
)

var=c("FEDFUNDS","INDPRO","CPIAUCSL","TB3MS", "GS5", "M1SL", "M2SL", "EXJPUSx", "CUSR0000SAC", "CUMFNS", "DPCERA3M086SBEA", "DDURRG3M086SBEA",
"DNDGRG3M086SBEA", "UNRATE", "CE16OV", "CES0600000008", "HOUST", "AMDMNOx", "S&P div yield")
########################################################################################
# Empleo paquete fbi para crear tablas, listas de kpis y limpiar nombres de variables
########################################################################################
data("fredmd_description")
descrip=fredmd_description
kpis=descrip[descrip$fred %in% var, ]
kpis[, c("fred", "description")]
kpis_ordenado <- kpis[order(kpis$group), ]
kpis_ordenado <- modify_group_column(kpis_ordenado)
# xtable
print(xtable(kpis_ordenado[, c( "gsi:description", "grupos")],
       caption="variables para análisis de impacto de PL",
       label= "tab:vari_fir"), include.rownames=FALSE)
# matching variables
descrip_tcode=kpis_ordenado[,c("tcode","fred", "grupos")]
ix <- match(var, descrip_tcode$fred)
ordered_descrip_tcode <- descrip_tcode[ix, ]
##########################
# KPIs ###################
##########################
variable_names = c("Fed Funds Rate",
                   "IP Index",
                   "CPI",
                   "3-Month Treasury Bill",
                   "5-Year Treasury Rate",
                   "M1 Money Stock",
                   "M2 Money Stock",
                   "Exchange rate: Japan/U.S.",
                   "CPI : Commodities",
                   "Capacity Utilization",
                   "Real personal consump.",
                   "Durable goods consump.",
                   "Nondurable goods consump.",
                   "Unemployment Rate",
                   "Employment",
                   "Avg Hourly Earnings",
                   "Housing Starts",
                   "New Orders",
                   "Dividend Yield")
transf_code <- as.numeric(as.character(ordered_descrip_tcode$tcode))
#transf_code = c(1,5,5,1,1,5,5,5,1,1,5,5,5,1,1,5,1,1,1)
################################################################################
# tabla resultados: variables para el impacto de PL #############################
################################################################################
ordered_descrip_tcode_copy <- ordered_descrip_tcode
# Agrego columna 'Variables'
ordered_descrip_tcode_copy$Variables <- variable_names
print(xtable(ordered_descrip_tcode_copy[,c("Variables", "grupos")] , caption="variables para análisis de impacto de PL",
             label= "tab:vari_fir"), include.rownames=FALSE)
################################################################################
# Grupos de variables y descripciones ##########################################
################################################################################
n_g=fredmd_description
ng=n_g[, c("fred", "group","gsi:description", "description", 'tcode')]
# List of values to be changed
values_to_change <- c("IPB51222s")
# New values to replace the old values
new_values <- c("IPB51222S")
# Loop through each value to be changed and replace them with new values
for (i in seq_along(values_to_change)) {
  ng$fred[ng$fred == values_to_change[i]] <- new_values[i]
}
colnames(ng)[colnames(ng) == "gsi:description"] <- "gsi"
########################################################################################
# Chequeo si columns de  data_s (train dataset) son iguales a actual_s (test dataset) ##
########################################################################################
if (identical(names(data_s), names(actual_s))) {
  print("The names of data_s and actual_s are equal.")
} else {
  print("The names of data_s and actual_s are not equal.")
}
#########################################################
df <- data.frame(data_s = names(data_s), stringsAsFactors = FALSE)
# Check if all names in df$data_s are in ng$fred
missing_names <- df$data_s[!(df$data_s %in% ng$fred)]
missing_names
############################################################
# Cuadros para apendice 1 con la descripción de variables ##
############################################################
filtered_ng <- ng %>% filter(fred %in% names(data_s))
slow_fast <- as.data.frame(read_delim("data/prepro/descripcion_df.csv",
                             delim = ";", escape_double = FALSE, trim_ws = TRUE))
#
not_in_slow_fast <- filtered_ng$fred[!filtered_ng$fred %in% slow_fast$fred]
#
old_values <- c("S.P.500", "S.P..indust", "S.P.div.yield", "S.P.PE.ratio")
new_values <- c("S&P 500", "S&P: indust", "S&P div yield", "S&P PE ratio")
slow_fast$fred <- ifelse(slow_fast$fred %in% old_values,
                         new_values[match(slow_fast$fred, old_values)],
                         slow_fast$fred)
#
filtered_slow_fast <- slow_fast[slow_fast$fred %in% names(data_s), ]
ordered_filtered_slow_fast <- filtered_slow_fast[order(filtered_slow_fast$group), ]
ordered_filtered_slow_fast_tcode <- modify_group_column(left_join(ordered_filtered_slow_fast, ng[, c("fred", "tcode")], by = "fred"))
dim(ordered_filtered_slow_fast_tcode)
names(ordered_filtered_slow_fast_tcode)
unique(ordered_filtered_slow_fast_tcode$grupos)
# xtable
print(xtable(ordered_filtered_slow_fast_tcode[, c( "fred", "description",
                                                   "grupos", "slow_1_fast_0", "tcode")],
digits=0), include.rownames=FALSE)
#
head(ordered_filtered_slow_fast)
dim(ordered_filtered_slow_fast)
#
ordered_filtered_slow_fast <- left_join(ordered_filtered_slow_fast, ng[, c("fred", "tcode")], by = "fred")

##########################
# Se guardan los datos ###
##########################
save(fred,  file = "data/Rdata/ng_dataframe/fred.RData")
save(transf_code,variables, variable_names, df_train, slow,data_s, actual_s,df_test_index,n_forecasts,
     ics,ic_p2_factors,  file = "data/Rdata/input_data_models/favar_ddfm_input.RData")
########################
df_actual_s <- fortify.zoo(actual_s)
df_data_s<- fortify.zoo(data_s)
write.csv(df_actual_s, 'data/scaled_train_test/scaled_test.csv', row.names=FALSE)
write.csv(df_data_s, 'data/scaled_train_test/scaled_train.csv', row.names=FALSE)
#save(transf_code,variables, variable_names, df_train, slow,data_s, actual_s,df_test_index,n_forecasts, ics,ic_p2_factors,  file = "data/Rdata/favar_ddfm_output.RData")

