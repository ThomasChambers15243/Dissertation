library("ggpubr")
library(dplyr)

# Organise Data into Box Plots

data <- data.frame(
  group = rep(c("gpt","human"), each = 20),
  score = c(testData$gpt, testData$human)
)


group_by(data, group) %>%
  summarise(
    count = n(),
    mean = mean(score, na.rm = TRUE),
    sd = sd(score, na.rm = TRUE)
  )

# Plot Data
ggboxplot(data, x="group", y="score",
          color = "group", palette = c("#53A2BE","#BF5454"),
          ylab = "Score", xlab = "Groups"
          )


# Shapiro Test
#If p is > alpha then data is not significantly different from the normal distribution
with(testData, shapiro.test(testData$gpt))

ggqqplot(testData$gpt, ylab = "GPT Answers", xlab = "Human",
         ggtheme = theme_minimal())

# Calulate Human mean for single test
humanMean <- testData$human
result.mean <- mean(x)

# Two Sample t-test
res = t.test(testData$gpt,mu = result.mean, alternative="greater")
res
