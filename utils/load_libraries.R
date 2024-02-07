# List of packages
packages <- c("readxl", "readr", "boot", "tsDyn", "vars", "repr", "dplyr",
              "dfms", "xts", "fbi", "forecast", "OOS", "zoo", "xtable",
              "tseries", "Metrics", "forecast", "readxl","stats","pracma", "devtools", "imputeTS" )

# Install and load packages
for (package in packages) {
  if (!require(package, character.only = TRUE)) {
    install.packages(package, dependencies = TRUE)
  }
  library(package, character.only = TRUE)
}
devtools::install_github("cykbennie/fbi")
# Load packages
library(readxl)
library(readr)
library(boot)
library(tsDyn)
library(vars)
library(repr)
library(dplyr)
library(dfms)
library(xts)
library(fbi)
library(forecast)
library(OOS)
library(zoo)
library(xtable)
library(tseries)
library(Metrics)
library(imputeTS)
