ui <- fluidPage(
  titlePanel(h1("Business Reviewer")),
  sidebarPanel(h2("Your information"),
               numericInput("weight",h3("Weight"), value = 70),
               selectInput("unit_weight","Unit", choices = c("kg","lb")),
               numericInput("abodmen",h3("Circumference of abodmen"), value = 50),
               selectInput("unit_abodmen","Unit", choices = c("cm","inch")),
               #radioButtons("gender",h2("Gender"), choices=c("male","female")),
               submitButton(),
               
               h3(textOutput("space")),
               h4(textOutput("info")),
               textOutput("contact1"),textOutput("contact2")
  ),
  
  mainPanel(
    plotOutput(outputId = "plot"),
    htmlOutput(outputId = "bodyfat")
  )
  
)



server <- function(input,output) {
  
  output$plot = renderPlot({
    if (input$unit_weight == "lb") weight = input$weight else weight = input$weight*2.20462262
    if (input$unit_abodmen == "cm") abodmen = input$abodmen else abodmen = input$abodmen*2.54
    
    p <- predict(lm.final3, newdata = data.frame(WEIGHT = weight, ABDOMEN=abodmen*2), interval = "predict", level = 0.9)
    if (!is.na(bodyfat.judge("male", p[1])))  {
      ggplot(data=data.frame(ingredient=c("fat","other"), value=c(p[1],100-p[1])), aes(x="", y=value, fill=ingredient))+
        geom_bar(width = 1, stat = "identity")+coord_polar("y", start=0)+
        geom_text(aes(y = 75, label = percent(p[1]/100)), size=5)+theme_gray()+
        labs(x = "", y = "")
    }
  })
  
  
  output$bodyfat = renderUI({
    if (input$unit_weight == "lb") weight = input$weight else weight = input$weight*2.20462262
    if (input$unit_abodmen == "cm") abodmen = input$abodmen else abodmen = input$abodmen*2.54
    
    p <- predict(lm.final3, newdata = data.frame(WEIGHT = weight, ABDOMEN=abodmen*2), interval = "predict", level = 0.9)
    
    bodyfat.judge = function(gender,bodyfat){
      if (gender == "male"){
        if (bodyfat <= 10) return(NA) #"Extremely below normal range! Please check your input."
        if (10 < bodyfat & bodyfat <= 14) return("Essential fat")
        if (14 < bodyfat & bodyfat <= 21) return("Athletes")
        if (21 < bodyfat & bodyfat <= 25) return("Fitness")
        if (25 < bodyfat & bodyfat <= 32) return("Average")
        if (bodyfat > 31 & bodyfat <= 60) return("Obese")
        if (bodyfat > 60) return(NA)
      }
      else {
        if (bodyfat <= 3) return(NA) #"Extremely below normal range! Please check your input."
        if (3 < bodyfat & bodyfat <= 6) return("Essential fat")
        if (6 < bodyfat & bodyfat <= 14) return("Athletes")
        if (14 < bodyfat & bodyfat <= 18) return("Fitness")
        if (18 < bodyfat & bodyfat <= 25) return("Average")
        if (bodyfat > 25 & bodyfat <= 60) return("Obese")
        if (bodyfat > 60) return(NA)
      }
    }
    
    str1 <- paste0("You body fat percentage is: ", round(p[1],1), "%.")
    str2 <- paste0("The 90% confidence interval of your bodyfat is ", "[",round(p[2],1),"%,",round(p[3],1), "%].")
    if (is.na(bodyfat.judge("male", p[1]))) {
      HTML( paste(h3("Extremely below normal range! Please check your input.")) )
    } else HTML(paste(str1, str2, h4("You are:   "), h1(bodyfat.judge("male", p[1]), align = "center"), sep = '<br/>'))
  })
  
  output$space = renderText({"-------------------------------"})
  output$info = renderText({ "Contact us"})
  output$contact1 = renderText({ "E-mail: yzeng58@wisc.edu"})
  output$contact2 = renderText({ "Telephone number: 608-886-6291"})
}

shinyApp(ui = ui, server = server)