library(ggpubr)
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
# If p is > alpha then data is not significantly different from the normal distribution
with(testData, shapiro.test(testData$gpt))
with(testData, shapiro.test(testData$human))

# F-test
# If the p > alpha then there is no significant difference between the variances
res.ftest <- var.test(testData$gpt, testData$human, alternative="two.sided")
res.ftest

# Two Sample t-test
res = t.test(testData$gpt,testData$human, alternative="greater", var.equal = TRUE)
res