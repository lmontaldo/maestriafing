library(tseries) 
library(fbi)
filepath <- "https://files.stlouisfed.org/files/htdocs/fred-md/monthly/2021-08.csv"
data <- fredmd(filepath, date_start = NULL, date_end = NULL, transform = TRUE)
N <- ncol(data)
print(head(data))
