library(mice)

# Paths to data Set
humanDataDir <- "HumanResults/"
genDataDir <- "SampleResults/"

# Empty list to hold pValues in
hochberg_pValues <- numeric(0)

insert_sorted_value <- function(value, existing_list) {
  # Insert the value into the list while maintaining sorted order
  existing_list <- c(existing_list, value)
  existing_list <- sort(existing_list, decreasing = TRUE)
  return(existing_list)
}

for (problem in 0:4) {  
  genSampleResults_P <- read.csv(gsub(" ", "", paste(genDataDir,'P',problem,".csv")))
  humanSampleResults_P <- read.csv(gsub(" ", "", paste(humanDataDir,'p',problem,".csv")))


  print(genSampleResults_P)
  print(humanSampleResults_P)
  
  # Normality Test
  #print(shapiro.test(genSampleResults_P$Score))
  #print(shapiro.test(humanSampleResults_P$Score))
  
  # Calculate the median for genSampleResults_P
  gen_median <- median(genSampleResults_P$Score)
  
  # Calculate the median for humanSampleResults_P
  human_median <- median(humanSampleResults_P$Score)
  
  # Print the results
  cat("Median for genSampleResults_P:", gen_median, "\n")
  cat("Median for humanSampleResults_P:", human_median, "\n")
  
  
  sampleSize <- nrow(genSampleResults_P)
  
  # Create a data frame
  myData <- data.frame(
    group = rep(c("humanScore", "genScore"), each = sampleSize),
    weight = c(humanSampleResults_P$Score, genSampleResults_P$Score)
  )
  
  
  # Wilcox Test
  result = wilcox.test(humanSampleResults_P$Score, genSampleResults_P$Score, 
                       alternative = "greater", paired = TRUE, exact = FALSE)
  
  print(result)
  
  hochberg_pValues <- insert_sorted_value(result$p.value, hochberg_pValues)
  
  effectSize = result$statistic / sqrt(sampleSize*2)
  
  print(paste("effectSize is:", effectSize))
  
  boxplot(main=paste("Problem: ", problem+1), names=c("GPT","Human"), outline=FALSE, genSampleResults_P$Score, humanSampleResults_P$Score, horizontal = TRUE)
}

print(hochberg_pValues)