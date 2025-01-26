import numpy as np
import random
import time
from functools import lru_cache
import matplotlib.pyplot as plt
import pandas as pd  # For table display

class CachePerformanceTester:
    def __init__(self, array_size=1000, num_queries=50_000):
        self.array_size = array_size
        self.num_queries = num_queries
        self.array = np.random.randint(1, 100_000, array_size, dtype=np.int64)
        self.updated_indices = set()  # Track updated indices

    def generate_queries(self):
        # Generate queries with repeated ranges to ensure cache hits
        queries = []
        for _ in range(self.num_queries):
            query_type = random.choice(["Range", "Update"])
            if query_type == "Range":
                # Random range query
                L = random.randint(0, self.array_size - 1)
                R = random.randint(L, self.array_size - 1)
                queries.append((query_type, L, R))
            elif query_type == "Update":
                # Random update query
                index = random.randint(0, self.array_size - 1)
                value = random.randint(1, 1000)
                queries.append((query_type, index, value))
        return queries

    def range_sum_no_cache(self, array, L, R):
        """Compute sum of elements between indices L and R without caching."""
        if L > R:
            L, R = R, L
        return np.sum(array[L:R + 1], dtype=np.int64)

    def update_no_cache(self, array, index, value):
        """Update value at the specified index without caching."""
        array[index] = value

    @lru_cache(maxsize=50_000)  # Increase cache size to store more results
    def range_sum_with_cache(self, L, R):
        """Compute sum of elements between indices L and R using LRU cache."""
        if L > R:
            L, R = R, L
        return np.sum(self.array[L:R + 1], dtype=np.int64)

    def update_with_cache(self, index, value):
        """Update value at the specified index and invalidate relevant cache."""
        self.array[index] = value
        self.updated_indices.add(index)  # Track updated index

    def execute_queries_with_cache(self, queries):
        """Execute queries with caching."""
        start_time = time.time()

        for query in queries:
            if query[0] == "Range":
                self.range_sum_with_cache(query[1], query[2])
            elif query[0] == "Update":
                self.update_with_cache(query[1], query[2])

        end_time = time.time()
        return end_time - start_time

    def execute_queries_no_cache(self, queries):
        """Execute queries without caching."""
        array = self.array.copy()
        start_time = time.time()

        for query in queries:
            if query[0] == "Range":
                self.range_sum_no_cache(array, query[1], query[2])
            elif query[0] == "Update":
                self.update_no_cache(array, query[1], query[2])

        end_time = time.time()
        return end_time - start_time

    def measure_performance(self):
        queries = self.generate_queries()

        # Measure performance with caching
        self.range_sum_with_cache.cache_clear()  # Clear cache before starting
        cache_time = self.execute_queries_with_cache(queries)

        # Measure performance without caching
        no_cache_time = self.execute_queries_no_cache(queries)

        # Get cache info
        cache_info = self.range_sum_with_cache.cache_info()

        return {
            'no_cache_time': no_cache_time,
            'cache_time': cache_time,
            'cache_hits': cache_info.hits
        }

    def plot_performance(self):
        # Collect execution time and cache hits
        num_tests = 10  # Perform 10 tests to get a variety of cache hits and times
        cache_hits_list = []
        time_list = []

        for _ in range(num_tests):
            performance_data = self.measure_performance()
            cache_hits_list.append(performance_data['cache_hits'])
            time_list.append(performance_data['cache_time'])

        # Plot execution time vs cache hits
        plt.figure(figsize=(10, 6))
        plt.scatter(cache_hits_list, time_list, color='blue', label="Execution Time vs Cache Hits")
        plt.xlabel('Cache Hits')
        plt.ylabel('Execution Time (seconds)')
        plt.title('Execution Time vs Cache Hits')
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def display_results(self):
        # Collect execution time and cache hits for multiple runs
        num_tests = 10  # Perform 10 tests to get a variety of cache hits and times
        results = []

        for _ in range(num_tests):
            performance_data = self.measure_performance()
            results.append({
                'No Cache Time (s)': performance_data['no_cache_time'],
                'Cache Time (s)': performance_data['cache_time'],
                'Cache Hits': performance_data['cache_hits']
            })

        # Create a DataFrame to display results as a table
        df = pd.DataFrame(results)
        print(df)


# Main execution
if __name__ == "__main__":
    # Create performance tester
    tester = CachePerformanceTester()

    # Display performance results as a table
    tester.display_results()

    # Plot performance
    tester.plot_performance()
