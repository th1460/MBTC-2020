require(rvest)
require(magrittr)

scrapyVideo <- function(link) {
    
    url <- 
        read_html(link)
    
    list_format <-
        list(
            author = url %>% 
                html_nodes(xpath = "/html/head/meta[@name='title']/@content") %>% 
                html_text() %>% 
                strsplit(":") %>% 
                .[[1]] %>% .[1] %>% stringr::str_trim(),
            body = url %>% 
                html_nodes(xpath = "//div[@class='Grid__cell flx-s:1 p-r:4']/p") %>% 
                html_text() %>% 
                gsub("\\n|\\t|\\r|\u201c|\u201d|\"", "", .) %>% 
                paste(collapse = ' '),
            title = url %>% 
                html_nodes(xpath = "/html/head/meta[@name='title']/@content") %>% 
                html_text() %>% 
                strsplit(":") %>% 
                .[[1]] %>% .[2] %>% stringr::str_trim(),
            type = "video",
            url = link
        ) 
    
    list_format %>% 
        jsonlite::toJSON(auto_unbox = TRUE, pretty = TRUE) %>% 
        jsonlite::write_json(glue::glue("R/videos/video{format(Sys.time(), '%Y%m%d%H%M%S')}.json"))
    
    Sys.sleep(2)
    
}

videos <- readr::read_lines("R/list_videos.txt")

videos %>% 
    purrr::map(~ scrapyVideo(.x))


