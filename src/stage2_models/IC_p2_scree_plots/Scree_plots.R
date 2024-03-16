loaded_objects <-load("data/Rdata/favar_dfms_output.RData")
libraries=source("utils/load_libraries.R")


# Set the base plot path
base_plot_path <- "docs/images/scree_plots/"

# Plot and save each type of scree plot
plot_types <- c("opt_number", "ev", "pve", "cum.pve")

for (i in seq_along(plot_types)) {
  png(paste0(base_plot_path, paste0("screeplot_", plot_types[i], ".png")), width = 1000, height = 1200)

  if (plot_types[i] == "opt_number") {
    plot(ics)
  } else {
    screeplot(ics, type = plot_types[i], cex.lab = 1.5)
  }

  dev.off()
}

########################## sin guardar, si se corren quedan en plots

plot(ics)
screeplot(ics, type="ev", cex.lab = 1.5)
screeplot(ics, type="pve", cex.lab = 1.5)
screeplot(ics, type="cum.pve", cex.lab = 1.5)
################################
