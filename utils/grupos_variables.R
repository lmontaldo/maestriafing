library(fbi)
library(dplyr)
modify_group_column <- function(ng) {
  # Create a new column 'grupos' based on the 'group' column using case_when
  ng <- ng %>%
    mutate(grupos = case_when(
      group == "Output and Income" ~ "Producto e ingresos",
      group == "Consumption, Orders, and Inventories" ~ "Consumo, órdenes e inventarios",
      group == "Labor Market" ~ "Mercado de trabajo",
      group == "Housing" ~ "Vivienda",
      group == "Money and Credit" ~ "Dinero y crédito",
      group == "Stock Market" ~ "Mercado de activos",
      group == "Interest and Exchange Rates" ~ "Tasas de interes y tipos de cambio",
      group == "Prices" ~ "Precios",
      TRUE ~ group
    ))

  return(ng)
}
