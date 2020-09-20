require(rvest)
require(magrittr)

scrapyArticle <- function(link) {
    
    url <- 
        read_html(link)
    
    list_format <-
        list(
            author = url %>% 
                html_nodes("[class='meta-item meta-aut']") %>% 
                html_text(),
            body = url %>% 
                html_nodes("[class='mat-txt']") %>% 
                html_text() %>% 
                gsub("\\n|\\t|\\r|\u201c|\u201d|\"", "", .),
            title = url %>% 
                html_nodes("[class='mat-tit']") %>% 
                html_text(),
            type = "article",
            url = link
        ) 
    
    list_format %>% 
        jsonlite::toJSON(auto_unbox = TRUE, pretty = TRUE) %>% 
        jsonlite::write_json(glue::glue("R/articles/article{format(Sys.time(), '%Y%m%d%H%M%S')}.json"))
    
    Sys.sleep(2)
    
}

articles <- readr::read_lines("R/list_articles.txt")

articles %>% 
    purrr::map(~ scrapyArticle(.x))


