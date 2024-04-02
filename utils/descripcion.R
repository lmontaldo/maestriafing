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

names_data_s=names(data_s)
names_actual_s=names(actual_s)

df <- data.frame(data_s = names(data_s), stringsAsFactors = FALSE)
# Check if all names in df$data_s are in ng$fred
missing_names <- df$data_s[!(df$data_s %in% ng$fred)]

# Get the positions and values of missing names
positions_and_values <- data.frame(position = which(!(df$data_s %in% ng$fred)),
                                   value = missing_names)

library(stringdist)
target_string <- positions_and_values$value[1]

# Calculate the distances between the target string and all strings in ng$gsi
distances <- stringdist::stringdist(target_string, ng$gsi)

# Find the index of the minimum distance
closest_match_index <- which.min(distances)

# Retrieve the most similar regex from ng$gsi
most_similar_regex <- ng$gsi[closest_match_index]


