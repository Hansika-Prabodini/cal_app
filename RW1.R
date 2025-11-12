# ==============================================================================
# Random Walk Simulation: Gambler's Ruin Probability
# ==============================================================================
#
# PURPOSE:
#   This script simulates the Gambler's Ruin problem, a classic random walk
#   scenario where a gambler starts with some initial capital and repeatedly
#   bets until either reaching zero (ruin) or surviving a fixed number of steps.
#
# MATHEMATICAL MODEL:
#   - A particle starts at position k > 0 on the number line
#   - At each time step, it moves left with probability p or right with
#     probability (1-p)
#   - The walk terminates if position reaches 0 (absorption/ruin)
#   - We estimate the probability of surviving N steps without reaching 0
#
# PARAMETERS:
#   - steps: Number of time steps in each random walk simulation (default: 100)
#   - people: Number of independent simulations to run for each starting
#             position (default: 100). More simulations improve accuracy.
#   - positions: Starting positions to test, as comma-separated values
#                (default: "1,5,10,20,100")
#   - probability: Probability of moving left (default: 0.4). The probability
#                  of moving right is automatically (1 - probability).
#   - save: Flag to enable CSV output (default: FALSE)
#
# USAGE:
#   Rscript RW1.R [--steps N] [--people N] [--positions x,y,z] [--probability p] [--save]
#
# EXAMPLES:
#   Rscript RW1.R
#   Rscript RW1.R --steps 200 --people 500
#   Rscript RW1.R --probability 0.5 --save
#   Rscript RW1.R --positions 5,10,15 --steps 150 --save
#
# ==============================================================================

# Parse command-line arguments
args <- commandArgs(trailingOnly = TRUE)

# Default parameter values
steps <- 100
people <- 100
starting_positions <- c(1, 5, 10, 20, 100)
left_probability <- 0.4
save_output <- FALSE

# Simple argument parser
if (length(args) > 0) {
  i <- 1
  while (i <= length(args)) {
    if (args[i] == "--steps" && i < length(args)) {
      steps <- as.numeric(args[i + 1])
      i <- i + 2
    } else if (args[i] == "--people" && i < length(args)) {
      people <- as.numeric(args[i + 1])
      i <- i + 2
    } else if (args[i] == "--positions" && i < length(args)) {
      starting_positions <- as.numeric(strsplit(args[i + 1], ",")[[1]])
      i <- i + 2
    } else if (args[i] == "--probability" && i < length(args)) {
      left_probability <- as.numeric(args[i + 1])
      i <- i + 2
    } else if (args[i] == "--save" || args[i] == "--output") {
      save_output <- TRUE
      i <- i + 1
    } else {
      i <- i + 1
    }
  }
}

# Survival probability function
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

# Run simulation
prob1 <- sapply(starting_positions, survival_prob)
results <- data.frame(starting_position = starting_positions, probability = prob1)

# Display results
print(results)

# Save to CSV if requested
if (save_output) {
  timestamp <- format(Sys.time(), "%Y%m%d_%H%M%S")
  filename <- paste0("rw_results_", timestamp, ".csv")
  write.csv(results, file = filename, row.names = FALSE)
  cat(sprintf("\nResults saved to: %s\n", filename))
}
