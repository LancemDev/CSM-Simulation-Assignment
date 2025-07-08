import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import Dict, List
import os

def plot_metrics(metrics: Dict[str, float], output_dir: str = 'visualizations'):
    """Plot key performance metrics."""
    # Create visualizations directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Prepare data for plotting
    metric_names = [
        'average_waiting_time', 
        'average_system_time',
        'server_utilization',
        'max_queue_length'
    ]
    values = [metrics[name] for name in metric_names]
    
    # Create bar plot
    plt.figure(figsize=(12, 6))
    bars = plt.bar(metric_names, values)
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}',
                ha='center', va='bottom')
    
    plt.title('Bank Queue Simulation Metrics')
    plt.ylabel('Value')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Save the plot
    output_path = os.path.join(output_dir, 'metrics_summary.png')
    plt.savefig(output_path)
    plt.close()
    
    return output_path

def plot_waiting_time_distribution(customer_data: List[Dict], output_dir: str = 'visualizations'):
    """Plot the distribution of customer waiting times."""
    df = pd.DataFrame(customer_data)
    
    plt.figure(figsize=(12, 6))
    sns.histplot(data=df, x='waiting_time', bins=30, kde=True)
    plt.title('Distribution of Customer Waiting Times')
    plt.xlabel('Waiting Time (minutes)')
    plt.ylabel('Number of Customers')
    plt.tight_layout()
    
    # Save the plot
    output_path = os.path.join(output_dir, 'waiting_time_distribution.png')
    plt.savefig(output_path)
    plt.close()
    
    return output_path

def plot_queue_length_over_time(customer_data: List[Dict], output_dir: str = 'visualizations'):
    """Plot the queue length over simulation time."""
    df = pd.DataFrame(customer_data).sort_values('arrival_time')
    
    # Calculate queue length over time
    time_points = []
    queue_lengths = []
    
    current_queue = 0
    for i, row in df.iterrows():
        time_points.append(row['arrival_time'])
        queue_lengths.append(current_queue)
        current_queue += 1
        
        time_points.append(row['departure_time'])
        queue_lengths.append(current_queue)
        current_queue = max(0, current_queue - 1)
    
    # Sort by time
    time_series = list(zip(time_points, queue_lengths))
    time_series.sort()
    time_points, queue_lengths = zip(*time_series)
    
    # Plot
    plt.figure(figsize=(12, 6))
    plt.step(time_points, queue_lengths, where='post')
    plt.title('Queue Length Over Time')
    plt.xlabel('Simulation Time (minutes)')
    plt.ylabel('Queue Length')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Save the plot
    output_path = os.path.join(output_dir, 'queue_length_over_time.png')
    plt.savefig(output_path)
    plt.close()
    
    return output_path

def generate_all_visualizations(metrics: Dict[str, float], customer_data: List[Dict]):
    """Generate all visualizations."""
    os.makedirs('visualizations', exist_ok=True)
    
    plots = {
        'metrics_summary': plot_metrics(metrics, 'visualizations'),
        'waiting_time_distribution': plot_waiting_time_distribution(customer_data, 'visualizations'),
        'queue_length_over_time': plot_queue_length_over_time(customer_data, 'visualizations')
    }
    
    return plots
