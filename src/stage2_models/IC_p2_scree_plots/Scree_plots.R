loaded_objects <-load("data/Rdata/favar_dfms_output.RData")
libraries=source("utils/load_libraries.R")
base_plot_path <- "docs/images/"
# Open a PNG device
png(paste0(base_plot_path, "ic_bai_ng.png"), width = 800, height = 600)
# Create the plot
plot(ics)
# Close the device to save the file
dev.off()
#
plot(ics)
#
save_screeplot <- function(ics=ics, type, main="para la muestra de entrenamiento", cex.main=2, filename, plot_path = "docs/images/") {
  # Create the directory if it doesn't exist
  if (!dir.exists(plot_path)) {
    dir.create(plot_path, recursive = TRUE)
  }

  # Full path for the plot
  full_plot_path <- paste0(plot_path, filename)

  # Open a PNG device with the full path
  png(full_plot_path, width = 800, height = 600)

  # Create the plot
  screeplot(ics, type = type, main = main, cex.main = cex.main)

  # Close the device to save the file
  dev.off()
}

# Now call the function for each plot
save_screeplot(ics, type=  "pve", filename = "screeplot_pve.png")
save_screeplot(ics, type = "ev",  filename = "screeplot_ev.png")
save_screeplot(ics, type = "cum.pve",  filename = "screeplot_cum_pve.png")
