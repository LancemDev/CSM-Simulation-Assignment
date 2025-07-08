# Bank Queue Simulation

This project simulates a single-server queue system for a bank using discrete-event simulation. The simulation models customer arrivals, service times, and queue dynamics to analyze the performance of the system.

## Features

- Simulates a single-server queue with FIFO (First-In-First-Out) discipline
- Generates inter-arrival times uniformly distributed between 1 and 8 minutes
- Generates service times uniformly distributed between 1 and 6 minutes
- Tracks key performance metrics including:
  - Average waiting time
  - Average system time
  - Server utilization
  - Maximum queue length
- Generates visualizations of the simulation results

## Requirements

- Python 3.8+
- Required Python packages are listed in `requirements.txt`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/LancemDev/CSM-Simulation-Assignment.git
   cd CSM-Simulation-Assignment
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the simulation with default parameters (500 customers):
```bash
python -m scripts.main
```

### Command Line Options

- `-n, --num-customers`: Number of customers to simulate (default: 500)
- `-o, --output-dir`: Output directory for results (default: 'results')
- `--seed`: Random seed for reproducibility

Example with custom parameters:
```bash
python -m scripts.main -n 1000 --seed 42 -o my_results
```

## Output

The simulation generates the following output files in the specified output directory:

- `metrics.json`: Detailed metrics from the simulation
- `customer_data.csv`: Raw data for each customer
- `summary.txt`: Summary of the simulation results
- Visualization files in the `visualizations` subdirectory:
  - `metrics_summary.png`: Bar chart of key metrics
  - `waiting_time_distribution.png`: Histogram of customer waiting times
  - `queue_length_over_time.png`: Queue length over the simulation time

## Project Structure

- `scripts/`
  - `main.py`: Main script to run the simulation
  - `simulation.py`: Core simulation logic
  - `visualization.py`: Functions for generating visualizations
- `requirements.txt`: Python package dependencies

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
