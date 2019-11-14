library(dplyr)

yelp <- read.csv("cinema.csv")[,-(13:15)]
yelp$latitude <- jitter(yelp$latitude)
yelp$longitude <- jitter(yelp$longitude)
yelp$college <- yelp$stars
yelp$zipcode <- formatC(yelp$postal_code, width=5, format="d", flag="0")




cleantable <- yelp %>%
  select(
    Name = name,
    Business_id = business_id,
    City = city,
    State = state,
    Zipcode = postal_code,
    Rating = stars,
    Address = address,
    Lat = latitude,
    Long = longitude
  )

