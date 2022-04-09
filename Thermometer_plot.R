library(tidyverse)

data_df <- read_csv("/Users/damianwilliams/Desktop/test_data.csv",col_names = F)%>%
  select(2:3)

names(data_df) <- c("Time", "Left_thermometer_temp")

ffg<-data_df %>%
  pivot_longer(-Time,values_to = "Temperature_C",names_to = "Thermometer")#%>%

ggplot(ffg,aes(Time,Temperature_C,color = Thermometer))+
  geom_line()+
  theme(legend.position = "none")
  
  

  


