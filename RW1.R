
steps <- 100
people <- 100
starting_positions <- c(1, 5, 10, 20, 100)
left_probability <- 0.4

survival_prob <- function(starting_position) {
  survival_peeps <- 0
  
  for (i in 1:people) {
    Position <- starting_position
    
    for (step in 1:steps) {
      direction <- sample(c(-1, 1), 1, replace = TRUE, prob = c(left_probability, 1 - left_probability))
      Position <- Position + direction
      
      if (Position == 0) {
        break
      }
      
      if (step == steps) {
        survival_peeps <- survival_peeps + 1
      }
    }
  }
  
  prob <- survival_peeps / people
  return(prob)
}

prob1 <- sapply(starting_positions, survival_prob)
results <- data.frame(starting_position = starting_positions, probability = prob1)
print(results)










