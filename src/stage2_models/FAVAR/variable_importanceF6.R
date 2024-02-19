rm(list = ls())
factor6=load("data/Rdata/results_favar_factor_6.RData")
libraries=source("utils/load_libraries.R")
source("utils/accuracy_measures.R")
######### PARA LA CREACIÓN DE LOS GRUPOS
data(fredmd_description)
n_g=fredmd_description
ng=n_g[, c("fred", "group","gsi:description")]
# List of values to be changed
values_to_change <- c("S&P 500", "S&P: indust", "S&P div yield", "S&P PE ratio", "IPB51222s")
# New values to replace the old values
new_values <- c("S.P.500", "S.P..indust", "S.P.div.yield", "S.P.PE.ratio", "IPB51222S")
# Loop through each value to be changed and replace them with new values
for (i in seq_along(values_to_change)) {
  ng$fred[ng$fred == values_to_change[i]] <- new_values[i]
}
##########
# Extract column names from Lamda_F
Lamda_F_colnames <- colnames(Lamda_F)
# Check if column names of Lamda_F are in ng$fred
colnames_in_ng <- Lamda_F_colnames %in% ng$fred
print(colnames_in_ng )
print(Lamda_F_colnames[!colnames_in_ng])
#########################
# Check if a similar value to "IPB51222S" exists in ng$fred
similar_index <- grep("IPB51222S", ng$fred, ignore.case = TRUE)
# Check if any match is found
if (length(similar_index) > 0) {
  # Retrieve the name from ng$fred using the index
  similar_name <- ng$fred[similar_index]
  print(similar_name)
} else {
  print("No similar value found.")
}
####
print(factor6)


