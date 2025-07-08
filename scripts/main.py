#!/usr/bin/env python3
"""
Bank Queue Simulation

This script simulates a single-server queue system for a bank with the following characteristics:
- Inter-arrival times: Uniformly distributed between 1 and 8 minutes
- Service times: Uniformly distributed between 1 and 6 minutes
- Single server with FIFO queuing discipline
"""

import argparse
import json
import os
from datetime import datetime
from pathlib import Path

from simulation import BankQueueSimulation
from visualization import generate_all_visualizations

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Bank Queue Simulation')
    parser.add_argument('-n', '--num-customers', type=int, default=500,
                      help='Number of customers to simulate (default: 500)')
    parser.add_argument('-o', '--output-dir', type=str, default='results',
                      help='Output directory for results (default: results)')
    parser.add_argument('--seed', type=int, default=None,
                      help='Random seed for reproducibility')
    return parser.parse_args()

def save_results(metrics: dict, customer_data: list, output_dir: str):
    """Save simulation results to files."""
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Save metrics to JSON
    metrics_file = os.path.join(output_dir, 'metrics.json')
    with open(metrics_file, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    # Save customer data to CSV
    import pandas as pd
    df = pd.DataFrame(customer_data)
    df.to_csv(os.path.join(output_dir, 'customer_data.csv'), index=False)

def main():
    """Main function to run the simulation."""
    args = parse_arguments()
    
    # Set random seed for reproducibility
    if args.seed is not None:
        import numpy as np
        np.random.seed(args.seed)
    
    print(f"Starting simulation with {args.num_customers} customers...")
    
    # Create a timestamped output directory
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = os.path.join(args.output_dir, f'simulation_{timestamp}')
    
    # Run simulation
    simulation = BankQueueSimulation(num_customers=args.num_customers)
    metrics = simulation.run()
    customer_data = simulation.get_customer_data()
    
    # Save results
    save_results(metrics, customer_data, output_dir)
    
    # Generate visualizations
    print("Generating visualizations...")
    plots = generate_all_visualizations(metrics, customer_data)
    
    # Print summary
    print("\nSimulation completed successfully!")
    print(f"Results saved to: {os.path.abspath(output_dir)}")
    print("\nKey Metrics:")
    print(f"- Average Waiting Time: {metrics['average_waiting_time']:.2f} minutes")
    print(f"- Average System Time: {metrics['average_system_time']:.2f} minutes")
    print(f"- Server Utilization: {metrics['server_utilization']:.2f}%")
    print(f"- Maximum Queue Length: {metrics['max_queue_length']} customers")
    
    # Save metrics to a text file for easy reference
    with open(os.path.join(output_dir, 'summary.txt'), 'w') as f:
        f.write("Bank Queue Simulation Results\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Number of customers: {args.num_customers}\n")
        f.write(f"Random seed: {args.seed}\n")
        f.write(f"Simulation time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("Key Metrics:\n")
        f.write("-" * 20 + "\n")
        f.write(f"Average Waiting Time: {metrics['average_waiting_time']:.2f} minutes\n")
        f.write(f"Average System Time: {metrics['average_system_time']:.2f} minutes\n")
        f.write(f"Server Utilization: {metrics['server_utilization']:.2f}%\n")
        f.write(f"Maximum Queue Length: {metrics['max_queue_length']} customers\n")
        
        f.write("\nVisualizations Generated:\n")
        f.write("-" * 25 + "\n")
        for plot_name, plot_path in plots.items():
            f.write(f"- {plot_name}: {os.path.basename(plot_path)}\n")

if __name__ == "__main__":
    main()