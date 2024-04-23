library(ggplot2)
###############
# VI lineal
###############
generate_horizontal_bar_plot <- function(df) {
  # Order the dataframe by Values column in descending order
  df <- df[order(-df$Values), ]

  # Create the horizontal bar plot
  ggplot(df, aes(x = Values, y = reorder(toupper(gsi), Values), fill = group)) +
    geom_bar(stat = "identity") +
    labs(title = "", x = "PESOS EN VALORES ABSOLUTOS", y = "") +
    scale_fill_manual(name = "GRUPOS DE VARIABLES",
                      values = setNames(df$color, df$group)) +
    theme_minimal() +
    theme(axis.text.y = element_text(size = 20),
          axis.text.x = element_text(size = 20),
          legend.text = element_text(size = 30),
          axis.title.x = element_text(size = 25)) +
    guides(fill = guide_legend(title = "GRUPOS DE VARIABLES", title.theme = element_text(size = 25)))
}

# Call the function with the dataframe `top15_f1` as argument
#generate_horizontal_bar_plot(top15_f1)
