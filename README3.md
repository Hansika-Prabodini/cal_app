# Other Components

This document describes the supporting components of the cal_app project, including R scripts, Java utilities, and configuration files.

## RW1.R - Random Walk Simulation

**Purpose:** Simulates random walk behavior to calculate survival probabilities.

**Description:**
- Simulates 100 people performing random walks over 100 steps
- Each person starts from different initial positions (1, 5, 10, 20, or 100)
- At each step, moves left (probability 0.4) or right (probability 0.6)
- If position reaches 0, the walk terminates (failure)
- Calculates and displays the probability of surviving all 100 steps for each starting position

**Output:** A data frame showing starting positions and their corresponding survival probabilities.

## Utils.java - Java Utility Class

**Purpose:** Provides basic utility methods for the project.

**Description:**
- Simple Java utility class with helper methods
- Contains a `printMessage()` method that outputs a utility message
- Can be extended with additional utility functions as needed

**Usage:** Basic demonstration utility that can be called from Java applications.

## default_config.yaml - Model Training Configuration

**Purpose:** Configuration file for machine learning model training.

**Description:**
Defines settings for training a Llama-3.2-1B language model using LoRA (Low-Rank Adaptation) fine-tuning technique.

**Configuration Sections:**
- **Model:** Specifies model name, cache directory, and attention settings
- **Training:** Defines training parameters including epochs, batch size, learning rate, and logging intervals
- **LoRA:** Configures Low-Rank Adaptation parameters for efficient fine-tuning
- **Data:** Specifies paths to training, validation, and test data files

**Key Parameters:**
- 3 training epochs with batch size 4
- Learning rate: 0.0002 with 100 warmup steps
- Maximum sequence length: 512 tokens
- FP16 precision enabled for efficient training

This configuration provides a complete setup for fine-tuning language models on custom datasets.
