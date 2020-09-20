require(dplyr)

dataset <- readr::read_csv("dataset.csv")

dataset %>% 
    arrange(row) %>% 
    select(Tempo:TARGET) %>% 
    filter(`Estação` == "Paraíso") %>% View
