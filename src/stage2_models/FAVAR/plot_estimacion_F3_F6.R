libraries=source("utils/load_libraries.R")

# Load the first ggplot object from the saved file
plot1 <- readRDS("rds_files/estimacion3factores.rds")

# Load the second ggplot object from the saved file
plot2 <- readRDS("rds_files/estimacion6factores.rds")

# Arrange the two plots side by side
combined_plots <- plot_grid(plot1, plot2, ncol = 2)

# Display the combined plots
print(combined_plots)
