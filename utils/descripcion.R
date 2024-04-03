rm(list = ls())
obj1=load("data/Rdata/favar_dfms_output.RData")
libraries=source("utils/load_libraries.R")
###############################
# Nombres variables
################################
library(fbi)
data(fredmd_description)
n_g=fredmd_description
ng=n_g[, c("fred", "group","gsi:description", "description")]
# List of values to be changed
values_to_change <- c("S&P 500", "S&P: indust", "S&P div yield", "S&P PE ratio", "IPB51222s")
# New values to replace the old values
new_values <- c("S.P.500", "S.P..indust", "S.P.div.yield", "S.P.PE.ratio", "IPB51222S")
# Loop through each value to be changed and replace them with new values
for (i in seq_along(values_to_change)) {
  ng$fred[ng$fred == values_to_change[i]] <- new_values[i]
}
colnames(ng)[colnames(ng) == "gsi:description"] <- "gsi"
#####################
names_data_s=names(data_s) # "S.P.500"         "S.P..indust"     "S&P div yield"   "S.P.PE.ratio"
names_actual_s=names(actual_s)

df <- data.frame(data_s = names(data_s), stringsAsFactors = FALSE)
# Check if all names in df$data_s are in ng$fred
missing_names <- df$data_s[!(df$data_s %in% ng$fred)]

# Get the positions and values of missing names
positions_and_values <- data.frame(position = which(!(df$data_s %in% ng$fred)),
                                   value = missing_names)

ng$fred #"S.P.500"         "S.P..indust"     "S.P.div.yield"   "S.P.PE.ratio"

# replace by
ng$fred <- gsub("[\\\\\\.\\&\\_]", "", ng$fred)
names(data_s) <- gsub("[\\\\\\.\\&\\_ ]", "", names(data_s))

# check again
df <- data.frame(data_s = names(data_s), stringsAsFactors = FALSE)
# Check if all names in df$data_s are in ng$fred
missing_names <- df$data_s[!(df$data_s %in% ng$fred)]

head(ng)

save(ng,  file = "data/Rdata/ng_dataframe/fred.RData")
# in replacement of load("data/Rdata/ng_dataframe/ng.RData")
