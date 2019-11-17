library(leaflet)
library(RColorBrewer)
library(scales)
library(lattice)
library(dplyr)
library(plyr)
library(fmsb)
library(ggplot2)
library(scales)

# Leaflet bindings are a bit slow; for now we'll just sample to compensate
# By ordering by centile, we ensure that the (comparatively rare) Superids
# will be drawn last and thus be easier to see
# yelp <- yelp[order(yelp$centile),]
yelp = yelp[order(yelp$stars),]
bus_id_search <<- 0


function(input, output, session) {
  ## Data Explorer ###########################################
  # Show a popup at the given location
  updateTabsetPanel(session, "nav", selected = "Theater explorer")
  
  locationwindow <- function(bus_id, lat, lng) {
    
    selectedZip <- yelp[yelp$business_id == bus_id,]
    content <- as.character(tagList(
      tags$h4("Rating:", as.integer(selectedZip$stars)),
      tags$strong(HTML(sprintf("%s, %s %s",
                               selectedZip$city, selectedZip$state, selectedZip$postal_code
      ))), tags$br(),
      sprintf("Name: %s", selectedZip$name), tags$br(),
      sprintf("Business ID: %s", selectedZip$business_id), tags$br(),
      sprintf("Address: %s", selectedZip$address)
    ))
    leafletProxy("map") %>% addPopups(lng, lat, content, layerId = bus_id)
  }
  
  observe({
    cities <- if (is.null(input$states)) character(0) else {
      filter(cleantable, State %in% input$states) %>%
        `$`('City') %>%
        unique() %>%
        sort()
    }
    stillSelected <- isolate(input$cities[input$cities %in% cities])
    updateSelectizeInput(session, "cities", choices = cities,
                         selected = stillSelected, server = TRUE)
  })
  
  observe({
    busns_id <- if (is.null(input$states)) character(0) else {
      cleantable %>%
        filter(State %in% input$states,
               is.null(input$cities) | City %in% input$cities) %>%
        `$`('Zipcode') %>%
        unique() %>%
        sort()
    }
    stillSelected <- isolate(input$busns_id[input$busns_id %in% busns_id])
    updateSelectizeInput(session, "busns_id", choices = busns_id,
                         selected = stillSelected, server = TRUE)
  })
  
  observe({
    if (is.null(input$goto))
      return()
    isolate({
      map <- leafletProxy("map")
      map %>% clearPopups()
      dist <- 0.5
      bus_id_search <<- input$goto$zip
      lat <- input$goto$lat
      lng <- input$goto$lng
      id = which(scale_final_score[,1] == bus_id_search)
      output$barplot = renderPlot({
        cn = colnames(scale_final_score)
        draw = data.frame(x = cn[-1], y = round(as.vector(t(scale_final_score[id,-1])),4))
        ggplot(data = draw, aes(x,y))  +
          geom_bar(stat = "identity", aes(fill = x)) + 
          geom_text(aes(label = paste(y * 100, "%"),
                        vjust = ifelse(y >= 0, 0, 1))) +
          scale_y_continuous("Score", labels = percent_format()) +
          theme_bw() + theme(legend.position="none") + labs(x = '')
      })
      output$radarplot = renderPlot({
        maxmum = max(max(scale_final_score[id,-1]), max(mean_score))
        minimum = min(min(scale_final_score[id,-1]), min(mean_score))
        colors_border=c( rgb(0.2,0.5,0.5,0.9), rgb(0.8,0.2,0.5,0.9))
        colors_in=c( rgb(0.2,0.5,0.5,0.4), rgb(0.8,0.2,0.5,0.4))
        draw_radar = rbind(rep(maxmum,7),rep(minimum,7), mean_score, scale_final_score[id,-1])
        radarchart(draw_radar, axistype=1 , 
                   #custom polygon
                   pcol=colors_border , pfcol=colors_in , plwd=4 , plty=1,
                   #custom the grid
                   cglcol="grey", cglty=1, axislabcol="grey", caxislabels=seq(0,15,5), cglwd=0.8,
                   #custom labels
                   vlcex=0.8 
        )
        legend(x=-1.4, y=1.2, legend = c("median", "cinema"), bty = "n", pch=20 , col=colors_in , text.col = "grey", cex=1, pt.cex=2)
      })
      output$advisor = renderUI({
        HTML(paste0(strsplit(advisor[advisor == bus_id_search, 2], '\n', fixed = TRUE)[[1]], sep = '<br/>'))
      })
      locationwindow(bus_id_search, lat, lng)
      map %>% fitBounds(lng - dist, lat - dist, lng + dist, lat + dist)
    })
    
  })
  
  
  output$theatertable <- DT::renderDataTable({
    df <- cleantable %>%
      filter(
        Rating >= input$minScore,
        Rating <= input$maxScore,
        is.null(input$states) | State %in% input$states,
        is.null(input$cities) | City %in% input$cities
      ) %>%
      mutate(Location = paste('<a class="go-map" href="" data-lat="', Lat, '" data-long="', Long, '" data-zip="', Business_id, '"><i class="fa fa-crosshairs"></i></a>', sep=""))
    action <- DT::dataTableAjax(session, df)
    DT::datatable(df, options = list(ajax = list(url = action)), escape = FALSE)
  })
  
  ## Interactive Map ###########################################
  
  # Create the map
  output$map <- renderLeaflet({
    leaflet() %>%
      addTiles(
        urlTemplate = "//{s}.tiles.mapbox.com/v3/jcheng.map-5ebohr46/{z}/{x}/{y}.png",
        attribution = 'Maps by <a href="http://www.mapbox.com/">Mapbox</a>'
      ) %>%
      setView(lng = -93.85, lat = 37.45, zoom = 4)
  })
  
  # A reactive expression that returns the set of zips that are
  # in bounds right now

  zipsInBounds <- reactive({
    if (is.null(input$map_bounds))
      return(yelp[FALSE,])
    bounds <- input$map_bounds
    latRng <- range(bounds$north, bounds$south)
    lngRng <- range(bounds$east, bounds$west)
    subset(yelp,
           latitude >= latRng[1] & latitude <= latRng[2] &
             longitude >= lngRng[1] & longitude <= lngRng[2])
  })
  # Precalculate the breaks we'll need for the two histograms
  output$space = renderText({"-------------------------------"})
  output$info = renderText({ "Contact us"})
  output$contact1 = renderText({ "E-mail: yzeng58@wisc.edu"})
  output$contact2 = renderText({ "Telephone number: 608-886-6291"})
  output$guide1 = renderUI({HTML( paste(HTML('&nbsp;'), "Search for your cinema"))})
  output$guide2 = renderUI({HTML( paste(HTML('&nbsp;'), "Business information"))})
  output$guide3 = renderText({"Tips: you can either find your cinema by filtering by location and rating, or input the relevant information such as business id on the top right of the table. By clicking of the blue button in the location button, the page would be redirected to the interactive map with a popup show more details about the cinema."})
  
  

  # This observer is responsible for maintaining the circles and legend,
  # according to the variables the user has chosen to map to color and size.
  observe({
    colorBy <- input$business_id
    
    colorData = as.factor(ifelse(round(yelp$stars) == input$rating, input$rating, "others"))
    pal = colorFactor("viridis", colorData)
    
    radius = 3000
    
    leafletProxy("map", data = yelp) %>%
      clearShapes() %>%
      addCircles(~longitude, ~latitude, radius=3000, layerId=~business_id,
                 stroke=FALSE, fillOpacity=0.4, fillColor=pal(colorData)) %>%
      addLegend("bottomleft", pal=pal, values=colorData, 
                title="Rating", layerId="colorLegend")
   })
  

  
  # When map is clicked, show a popup with city info
  observe({
    leafletProxy("map") %>% clearPopups()
    event <- input$map_shape_click
    if (is.null(event))
      return()
    bus_id_search <<- event$id
    id = which(scale_final_score[,1] == bus_id_search)
    isolate({
      output$barplot = renderPlot({
        cn = colnames(scale_final_score)
        draw = data.frame(x = cn[-1], y = round(as.vector(t(scale_final_score[id,-1])),4))
        ggplot(data = draw, aes(x,y))  +
          geom_bar(stat = "identity", aes(fill = x)) + 
          geom_text(aes(label = paste(y * 100, "%"),
                        vjust = ifelse(y >= 0, 0, 1))) +
          scale_y_continuous("Score", labels = percent_format()) +
          theme_bw() + theme(legend.position="none") + labs(x = '')
      })
      
      output$radarplot = renderPlot({
        maxmum = max(max(scale_final_score[id,-1]), max(mean_score))
        minimum = min(min(scale_final_score[id,-1]), min(mean_score))
        colors_border=c( rgb(0.2,0.5,0.5,0.9), rgb(0.8,0.2,0.5,0.9))
        colors_in=c( rgb(0.2,0.5,0.5,0.4), rgb(0.8,0.2,0.5,0.4))
        draw_radar = rbind(rep(maxmum,7),rep(minimum,7), mean_score, scale_final_score[id,-1])
        radarchart(draw_radar, axistype=1 , 
                    #custom polygon
                    pcol=colors_border , pfcol=colors_in , plwd=4 , plty=1,
                    #custom the grid
                    cglcol="grey", cglty=1, axislabcol="grey", caxislabels=seq(0,15,5), cglwd=0.8,
                    #custom labels
                    vlcex=0.8 
        )
        legend(x=1.5, y=1, legend = c("median", "cinema"), bty = "n", pch=20 , col=colors_in , text.col = "grey", cex=1.3, pt.cex=2)
      })
      output$advisor = renderUI({
        HTML(paste0(strsplit(advisor[advisor == bus_id_search, 2], '\n', fixed = TRUE)[[1]], sep = '<br/>'))
      })
      locationwindow(event$id, event$lat, event$lng)
      
    })
  })
  

}
