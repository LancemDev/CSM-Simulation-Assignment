import numpy as np
from dataclasses import dataclass
from typing import List, Dict, Tuple

@dataclass
class Customer:
    """Represents a customer in the simulation."""
    id: int
    arrival_time: float
    service_time: float
    service_start: float = 0.0
    departure_time: float = 0.0

    @property
    def waiting_time(self) -> float:
        return self.service_start - self.arrival_time
    
    @property
    def time_in_system(self) -> float:
        return self.departure_time - self.arrival_time

class BankQueueSimulation:
    """Simulates a single-server queue system for a bank."""
    
    def __init__(self, num_customers: int = 500):
        self.num_customers = num_customers
        self.customers: List[Customer] = []
        self.clock = 0.0
        self.server_busy = False
        self.queue: List[Customer] = []
        self.next_event_time = float('inf')
        self.next_arrival = 0.0
        self.next_departure = float('inf')
        self.metrics: Dict[str, float] = {
            'total_waiting_time': 0.0,
            'total_system_time': 0.0,
            'max_queue_length': 0,
            'server_utilization': 0.0,
            'busy_time': 0.0
        }
    
    def generate_interarrival_time(self) -> float:
        """Generate interarrival time between 1 and 8 minutes."""
        return np.random.uniform(1, 8)
    
    def generate_service_time(self) -> float:
        """Generate service time between 1 and 6 minutes."""
        return np.random.uniform(1, 6)
    
    def schedule_arrival(self, time: float):
        """Schedule the next arrival event."""
        self.next_arrival = time
        self.next_event_time = min(self.next_event_time, self.next_arrival)
    
    def schedule_departure(self, time: float):
        """Schedule the next departure event."""
        self.next_departure = time
        self.next_event_time = min(self.next_event_time, self.next_departure)
    
    def handle_arrival(self, customer: Customer):
        """Handle customer arrival event."""
        if not self.server_busy:
            self.server_busy = True
            customer.service_start = self.clock
            customer.departure_time = self.clock + customer.service_time
            self.schedule_departure(customer.departure_time)
        else:
            self.queue.append(customer)
        
        # Schedule next arrival
        if len(self.customers) < self.num_customers - 1:
            next_customer = Customer(
                id=len(self.customers) + 1,
                arrival_time=self.clock + self.generate_interarrival_time(),
                service_time=self.generate_service_time()
            )
            self.schedule_arrival(next_customer.arrival_time)
        
        # Update max queue length
        self.metrics['max_queue_length'] = max(
            self.metrics['max_queue_length'], 
            len(self.queue)
        )
    
    def handle_departure(self, customer: Customer):
        """Handle customer departure event."""
        self.metrics['total_waiting_time'] += customer.waiting_time
        self.metrics['total_system_time'] += customer.time_in_system
        self.metrics['busy_time'] += customer.service_time
        
        if self.queue:
            next_customer = self.queue.pop(0)
            next_customer.service_start = self.clock
            next_customer.departure_time = self.clock + next_customer.service_time
            self.schedule_departure(next_customer.departure_time)
        else:
            self.server_busy = False
            self.next_departure = float('inf')
    
    def run(self) -> Dict[str, float]:
        """Run the simulation."""
        # Initialize first customer
        first_customer = Customer(
            id=0,
            arrival_time=0.0,
            service_time=self.generate_service_time()
        )
        self.schedule_arrival(first_customer.arrival_time)
        
        # Main simulation loop
        while self.clock < float('inf'):
            self.clock = self.next_event_time
            
            if self.clock == float('inf'):
                break
                
            if self.next_arrival <= self.next_departure and len(self.customers) < self.num_customers:
                # Process arrival
                current_customer = Customer(
                    id=len(self.customers),
                    arrival_time=self.next_arrival,
                    service_time=self.generate_service_time()
                )
                self.customers.append(current_customer)
                self.handle_arrival(current_customer)
            else:
                # Process departure
                current_customer = next(
                    c for c in self.customers 
                    if abs(c.departure_time - self.clock) < 1e-6
                )
                self.handle_departure(current_customer)
            
            # Update next event time
            self.next_event_time = min(self.next_arrival, self.next_departure)
        
        # Calculate final metrics
        self.metrics['server_utilization'] = (self.metrics['busy_time'] / self.clock) * 100
        self.metrics['average_waiting_time'] = self.metrics['total_waiting_time'] / self.num_customers
        self.metrics['average_system_time'] = self.metrics['total_system_time'] / self.num_customers
        
        return self.metrics
    
    def get_customer_data(self) -> List[Dict]:
        """Return customer data for analysis."""
        return [
            {
                'id': c.id,
                'arrival_time': c.arrival_time,
                'service_time': c.service_time,
                'waiting_time': c.waiting_time,
                'departure_time': c.departure_time,
                'time_in_system': c.time_in_system
            }
            for c in self.customers
        ]
