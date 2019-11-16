library(ggplot2)
library(fmsb)
library(plyr)
library(ggplot2)
library(scales)
finalscore = read.csv("final_score.csv")[,c(2,6:12)]

my.scale = function(v){
  maximum = max(abs(v))
  return(v/maximum)
}

scale_final_score = cbind(finalscore[1], apply(finalscore[,-1], 2, my.scale))
write.csv(scale_final_score, "scale_final_score.csv")

mean_score = apply(scale_final_score[,-1], 2, mean)

scale_final_score[,-1] = scale_final_score[,-1]*10
cn = colnames(scale_final_score)
draw = data.frame(x = cn[-1], y = round(as.vector(t(scale_final_score[1,-1])),4))
maxmum = max(max(scale_final_score[18,-1]), max(mean_score))
minimum = min(min(scale_final_score[18,-1]), min(mean_score))
draw_radar = rbind(rep(maxmum,7),rep(minimum,7), scale_final_score[18,-1], mean_score)
radarchart(draw_radar, axistype=1 , 
     pfcol=rgb(0.2,0.5,0.5,0.5) , plwd=4 , 
           cglcol="grey", cglty=1, axislabcol="grey", caxislabels=seq(0,20,5), cglwd=0.8,
           vlcex=0.8 )

ggplot(data = draw, aes(x,y))  +
  geom_bar(stat = "identity", aes(fill = x)) + 
  geom_text(aes(label = paste(y * 100, "%"),
                vjust = ifelse(y >= 0, 0, 1))) +
  scale_y_continuous("Anteil in Prozent", labels = percent_format()) + 
  theme_bw() + theme(legend.position="none") + labs(x = '')


set.seed(99)
data <- as.data.frame(matrix( sample( 0:20 , 15 , replace=F) , ncol=5))
colnames(data) <- c("math" , "english" , "biology" , "music" , "R-coding" )
rownames(data) <- paste("mister" , letters[1:3] , sep="-")

# To use the fmsb package, I have to add 2 lines to the dataframe: the max and min of each variable to show on the plot!
data <- rbind(rep(20,5) , rep(0,5) , data)

# Color vector
colors_border=c( rgb(0.2,0.5,0.5,0.9), rgb(0.8,0.2,0.5,0.9) , rgb(0.7,0.5,0.1,0.9) )
colors_in=c( rgb(0.2,0.5,0.5,0.4), rgb(0.8,0.2,0.5,0.4) , rgb(0.7,0.5,0.1,0.4) )

# plot with default options:
radarchart( data  , axistype=1 , 
            #custom polygon
            pcol=colors_border , pfcol=colors_in , plwd=4 , plty=1,
            #custom the grid
            cglcol="grey", cglty=1, axislabcol="grey", caxislabels=seq(0,20,5), cglwd=0.8,
            #custom labels
            vlcex=0.8 
)
legend(x=0.7, y=1, legend = rownames(data[-c(1,2),]), bty = "n", pch=20 , col=colors_in , text.col = "grey", cex=1.2, pt.cex=3)
