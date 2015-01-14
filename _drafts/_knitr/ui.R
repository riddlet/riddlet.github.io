library(shiny)
shinyUI(
  pageWithSidebar(
    headerPanel(title=HTML('Runs scored'), windowTitle='Runs Scored'),
    
    sidebarPanel(
      sliderInput('games', label="Minimum Number of Games Played:",
                  min=1, max=162, value=150, step=1),
    ),
    mainPanel(
      htmlOutput('plot')
    )
  )
)