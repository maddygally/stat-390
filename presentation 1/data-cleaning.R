### DATA CLEANING

library(readxl)
library(tidymodels)
library(skimr)
library(janitor)


combined_CMIL_scoring_V5 <- read_excel("presentation 1/data/combined CMIL scoring V5.xlsx") %>% 
  clean_names %>% 
  slice(-1)

skim(combined_CMIL_scoring_V5)
