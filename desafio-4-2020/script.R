require(dplyr)

train_data <- 
    readr::read_csv("train_dataset_algartech.csv") %>% 
    select(-c(`Possui carro`, 
              `Horas de trabalho padrão`,
              `Maior de idade`))

y = NULL
for (i in 1:ncol(train_data)) {
    
    y <- c(y, train_data %>% as.data.frame() %>% .[, i] %>% class())
    
}

train_data %>% names() %>% .[which(y == "character")]

scored <- 
    readr::read_csv("to_be_scored_algartech.csv")

scored %>% readr::write_csv("to_be_scored_algartech2.csv")

results <- readr::read_csv("results.csv")
