rm(list = ls())
factor3=load("data/Rdata/results_favar_factor_3.RData")
libraries=source("utils/load_libraries.R")
source("utils/accuracy_measures.R")
####
print(factor3)

##################################
# ESTIMACION DE LOS FACTORES
##################################
df=data_var
# Assuming your dataframe is named 'df'
xts_data <- xts(df[, -ncol(df)], order.by = as.Date(rownames(df)))

# Convert xts to data frame
df_plot <- data.frame(date = index(xts_data), coredata(xts_data))

# Reshape the data for ggplot2
df_plot_long <- tidyr::gather(df_plot, key = "variable", value = "value", -date)

# Plot using ggplot2
f3_estimacion_plot <-ggplot(df_plot_long, aes(x = date, y = value, color = variable)) +
  geom_line() +
  labs(title = "Tres Factores Estimados", x = "fecha", y = "valor") +
  theme_minimal() +
  theme(legend.position = c(0.95, 0.1), legend.title = element_blank()) +
  guides(color = guide_legend(title = NULL))
saveRDS(f3_estimacion_plot, file = "rds_files/estimacion3factores.rds")

# t(Lamda_F[2,])%*%Lamda_F[2,]: es la parte de abajo
#a_i/ t(Lamda_F[2,])%*%Lamda_F[2,] en cada componente
