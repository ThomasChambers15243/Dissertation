library("ggpubr")
library(dplyr)

# Organise Data into Box Plots

data <- data.frame(
  group = rep(c("gpt","human"), each = 20),
  score = c(SampleResults$Score, HumanResults$Score)
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
with(SampleResults, shapiro.test(SampleResults$Score))

# Q-Q Plot
ggqqplot(SampleResults$Score, ylab = "GPT Answers", xlab = "Human",
         ggtheme = theme_minimal())

# Density Plot
ggdensity(SampleResults$Score,
          main = "Density Plot of Generated Scores",
          xlab = "Generated Scores")

# Calulate Human mean for single test
humanMean <- HumanResults$Score
result.mean <- mean(humanMean)

# One Sample t-test
res = t.test(SampleResults$Score, mu = result.mean, alternative="greater")
res
