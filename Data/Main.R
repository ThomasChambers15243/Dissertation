library(mice)
library(magrittr)
library(ggplot2)

# Paths to data Set
humanDataDir <- "HumanResults/"
genDataDir <- "SampleResults/"

# Number of Imputations
imputations <- 5
number_of_problems <- 4

# Opens CSV's
problem = 0

## Functions
insert_sorted_value <- function(value, existing_list) {
  # Insert the value into the list while maintaining sorted order
  existing_list <- c(existing_list, value)
  existing_list <- sort(existing_list, decreasing = TRUE)
  return(existing_list)
}

calc_effect_size <- function(list1, list2) {
  SD1 <- sd(list1)
  SD2 <- sd(list2)
  pooledSD <- sqrt((SD1^2 + SD2^2) / 2)
  effectR <- (mean(list1) - mean(list2)) / pooledSD
  return (effectR)   
}


# Holds final values of all problems
final_results = data.frame(matrix( 
  vector(), 0, 4, dimnames=list(c(), c("ProblemNum", "Effect Size", "z-Value", "p-Values"))), 
  stringsAsFactors=F) 

## Data Collection using Multiple Imputation ##

for (problem in 0:number_of_problems) { 
  genSampleResults_P <- read.csv(gsub(" ", "", paste(genDataDir,'P',problem,".csv")))
  humanSampleResults_P <- read.csv(gsub(" ", "", paste(humanDataDir,'p',problem,".csv")))
  
  sampleSize = nrow(genSampleResults_P) 
  
  ## STAGE 1 - Create Imputation ##
  
  # Create Imputated data
  humanSampleResults_P.imp <- mice(humanSampleResults_P, m = imputations, method = "pmm")
  genSampleResults_P.imp <- mice(genSampleResults_P, m = imputations, method = "pmm")
  
  # Examine Data
  #print(complete(humanSampleResults_P.imp, 1))
  #print(complete(genSampleResults_P.imp, 1))
  
  #Plots Graph of Imputated Values
  # Visualize Shit
  # Extract the "tall" matrix which stacks the imputations
  humanSampleResults_P.comp <- complete(humanSampleResults_P.imp, "long", include = TRUE)
  # cci` returns logical whether its input is complete at each observation.
  humanSampleResults_P.comp$Score.NA <- cci(humanSampleResults_P$Score)
  head(humanSampleResults_P.comp[, c("Score", "Score.NA")])
  # Plot
  ggplot(humanSampleResults_P.comp,
         aes(x= .imp, y = Score, color = Score.NA)) +
    geom_jitter(show.legend = FALSE,
                width = .1)
  
  # Gets complete set of all imuputations
  humanSampleResults_P.comp <- complete(humanSampleResults_P.imp, "long", include = FALSE)
  genSampleResults_P.comp <- complete(genSampleResults_P.imp, "long", include = FALSE)
  
  
  # Creates data frame with both groups scores
  imp = humanSampleResults_P.comp$.imp
  humResults = humanSampleResults_P.comp$Score
  genResults = genSampleResults_P.comp$Score
  # DataGrame
  samples <- data.frame(imp, humResults, genResults)
  #print(samples)
  
  ## STAGE 2 - Analysis of Data ##
  
  pValueResults <- numeric(0)
  zValueResults <- numeric(0)
  effectSizes <- numeric(0)
  for (curImp in 1:imputations) {
    hum <- samples$humResults[samples$imp == curImp]
    gen <- samples$genResults[samples$imp == curImp]
    # Cohen's d Effect 
    CohendEffectSize <- calc_effect_size(hum, gen)
    # Perform Test
    results = wilcox.test(hum, gen,
                          alternative = "greater", paired = TRUE, exact = FALSE)
    # Append lists
    zValueResults <- append(results$statistic, zValueResults)
    pValueResults <- append(results$p.value, pValueResults)
    effectSizes <- append(CohendEffectSize, effectSizes)
    }
    
  ## STAGE 3 - Collect Data ##
  
  final_results[nrow(final_results) + 1, ] <- c(problem, mean(effectSizes), mean(zValueResults), mean(pValueResults))
  
}

## Type 1 Error Correction: Benjamini-Hochberg Procedure ## 
print(final_results)

# Sort List of pValues
unordered_pValues <- final_results$p.Values
ordered_pValues <- numeric(0)
for (value in unordered_pValues) {
  ordered_pValues <- insert_sorted_value(value, ordered_pValues)
} 

# Procedure 
significance = 0.05
remaining_Values = numeric(0)
for (index in 1:length(ordered_pValues)) {
  hochSig = (significance/index)
  
  if (ordered_pValues[index] < hochSig) {
    remaining_Values <- ordered_pValues[(index + 1):length(ordered_pValues)]
    break
  }
}


# Filter the data frame
significant_results <- final_results[final_results$p.Values %in% remaining_Values, ]
indicative_results <- final_results[!final_results$p.Values %in% remaining_Values, ]

# Print Final Results
print(significant_results)
print(indicative_results)









