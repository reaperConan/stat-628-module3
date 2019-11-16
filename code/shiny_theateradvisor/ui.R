library(leaflet)
library(shinydashboard)
library(RColorBrewer)
library(scales)
library(fmsb)
library(lattice)
library(dplyr)
library(plyr)
library(ggplot2)


# Choices for drop-downs


navbarPage("Theater Advisor", id="nav",
           tabPanel("Advisor",
                    div(class="outer",
                        
                        tags$head(
                          includeCSS("styles.css"),
                          includeScript("gomap.js")
                        ),
                        
                        # If not using custom CSS, set height of leafletOutput to a number instead of percent
                        leafletOutput("map", width="50%", height="100%"),
                        
                        absolutePanel(id = "controls", class = "panel panel-default", fixed = TRUE,
                                      draggable = TRUE, top = 60, left = "auto", right = 10, bottom = "auto",
                                      width = 780, height = "auto",
                                      h2("Theater Advisor"),
                                      splitLayout(style = "border: 1px solid silver:", cellWidths = c(375,375), 
                                                  plotOutput(outputId = "radarplot"),
                                                  plotOutput(outputId = "barplot")
                                      ),
                                      h4(htmlOutput("advisor")),
                                      textOutput("space"),
                                      textOutput("info"),
                                      textOutput("contact1"),textOutput("contact2") 
                                      # ,textInput("bus_id", "Business ID")
                                    
                        ),

                        absolutePanel(id = "controls", class = "panel panel-default", fixed = TRUE,
                                      draggable = TRUE, top = 60, left = "auto", right = 810, bottom = "auto",
                                      width = 300, height = "auto",
                                      
                                      h2("Theater Map"),
                                      selectInput("rating", "Rating", choices = 1:5, selected = 5)
                        ),
                        
                        
                        tags$div(id="cite",
                                 'Inspired by', tags$em('https://shiny.rstudio.com/gallery/superzip-example.html'), ' by Joe Cheng <joe@rstudio.com>.'),
                        
                    )
                    
                    
                    
           ),
           tabPanel("Theater explorer",
                    fluidRow(
                      column(3,
                             selectInput("states", "States", c("All states"="", structure(state.abb, names=state.abb), "Washington, DC"="DC"), multiple=TRUE)
                      ),
                      column(3,
                             conditionalPanel("input.states",
                                              selectInput("cities", "Cities", c("All cities"=""), multiple=TRUE)
                             )
                      ),
                      column(1,
                             numericInput("minScore", "Min Rating", min=1, max=5, value=1)
                      ),
                      column(1,
                             numericInput("maxScore", "Max Rating", min=1, max=5, value=5)
                      )),
                    hr(),
                    DT::dataTableOutput("theatertable")
           ),
          
  conditionalPanel("false", icon("crosshair"))
)
