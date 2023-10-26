install.packages("reticulate")
install.packages("here")
packages_to_install <- c("reticulate", "here", "readr")
for (package in packages_to_install) {
  if (!requireNamespace(package, quietly = TRUE)) {
    install.packages(package)
  }
}
library(reticulate)
library(here)
library(readr)
setwd(here())
use_python("../python/python.exe")
pickle_slow_fast <- "../data/prepro/x_slow_fast.pkl"
df_slow_fast <- readRDS(pickle_slow_fast)
print(head(df_slow_fast))



