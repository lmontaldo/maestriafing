library(fbi)
library(dplyr)
load("data/Rdata/ng_dataframe/fred.RData")
###########################################################
# Función que crea nueva columna de grupos en español ####
###########################################################
modify_group_column <- function(ng) {
  ng <- ng %>%
    mutate(grupos = case_when(
      group == "Output and Income" ~ "Producto e ingresos",
      group == "Consumption, Orders, and Inventories" ~ "Consumo, órdenes e inventarios",
      group == "Labor Market" ~ "Mercado de trabajo",
      group == "Housing" ~ "Vivienda",
      group == "Money and Credit" ~ "Dinero y crédito",
      group == "Stock Market" ~ "Mercado de activos",
      group == "Interest and Exchange Rates" ~ "Tasas de interés y tipos de cambio",
      group == "Prices" ~ "Precios",
      TRUE ~ group
    ))

  return(ng)
}
#####################################################################
# Función que crea nueva columna de grupos en español abreviadas ####
#####################################################################
grupos_espagnol_abreviados <- function(ng) {
  ng <- ng %>%
    mutate(grupos = case_when(
      group == "Output and Income" ~ "Producto e ingresos",
      group == "Consumption, Orders, and Inventories" ~ "Cons., órdenes e invent.",
      group == "Labor Market" ~ "Mercado de trabajo",
      group == "Housing" ~ "Vivienda",
      group == "Money and Credit" ~ "Dinero y crédito",
      group == "Stock Market" ~ "Mercado de activos",
      group == "Interest and Exchange Rates" ~ "Tasas de interés y TC",
      group == "Prices" ~ "Precios",
      TRUE ~ group
    ))

  return(ng)
}
#####################################
## Dataframe con colores por grupo ##
#####################################
distinct_colors_manual <- c("#1f77b4", "#ff7f0e", "#FFDB58", "#d62728", "#9467bd",
                            "#808080", "#e377c2", "#00FFFF")
# Identify unique groups
unique_groups <- unique(fred$grupos)
color_mapping <- setNames(distinct_colors_manual,
                          unique_groups)
fred$color <- color_mapping[fred$grupos]

group_color_df <- data.frame(
  color = as.character(color_mapping),
  group = names(color_mapping),
  stringsAsFactors = FALSE
)
# Print the dataframe
print(group_color_df)

##############################
#
###############################
