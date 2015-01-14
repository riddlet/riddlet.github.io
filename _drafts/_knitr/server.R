library(plotly)
library(shiny)
shinyServer(function(input, output) {
  output$plot <- renderUI({
    df_sub <- df[df$G>input$games,]
    p <- ggplot(df_sub, aes(x=R)) + 
      geom_histogram(binwidth=1, fill="#144256") +
      ylab('Count') + xlab('Runs') +
      theme_bw()
    
    py <- plotly(triddle, lsjrbob3nl, 'https://plot.ly')
    
    res <- py$ggplotly(p, kwargs=list(filename='Runs',
                                      fileopt='overwrite',
                                      auto_open=F))
    
    tags$iframe(src=res$response$url,
                frameBorder='0')
  })
})