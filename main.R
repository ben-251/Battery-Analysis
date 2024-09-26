library(readr)
library(dplyr)
library(ggplot2)

data6 <- read_csv("Data/6.csv")
data7 <- read_csv("Data/7.csv")
data8 <- read_csv("Data/8.csv") %>% 
  filter(status %in% c("Charging", "Discharging"))

ggplot(data8, aes(x = seq_along(battery)*0.00833333, y = battery)) + 
  geom_line(color = "slateblue", size = 1, alpha = 0.9, linetype = 1) + 
  labs(x = "Time (Hours)", 
       y = "Battery (%)", 
       title = "Battery use")


