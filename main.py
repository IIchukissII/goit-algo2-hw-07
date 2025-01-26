import time
import os
from task_2 import measure_performance as task_2_measure_performance, plot_results as task_2_plot_results, print_results_table as task_2_print_results_table
from task_1 import CachePerformanceTester

def main():
    # Task 1: Cache Performance for Range Sum and Update Queries
    print("Task 1: Cache Performance for Range Sum and Update Queries")
    tester = CachePerformanceTester()
    
    # Assuming the CachePerformanceTester has a method that directly provides the results
    task_1_results = tester.measure_performance()  # Or use the correct method for Task 1 results
    print("Task 1 Results (Debugging):", task_1_results)  # Debugging output
    
    tester.display_results()
    # tester.plot_performance()

    # Task 2: Fibonacci Calculation Performance with LRU Cache vs Splay Tree
    print("\nTask 2: Fibonacci Calculation Performance (LRU Cache vs Splay Tree)")
    task_2_results = task_2_measure_performance()
    task_2_print_results_table(task_2_results)
    task_2_plot_results(task_2_results)

    # Generate README.md
    generate_readme(task_1_results, task_2_results)

def generate_readme(task_1_results, task_2_results):
    """Generate README.md with results from Task 1 and Task 2"""
    readme_content = """
# Cache Performance and Fibonacci Calculation Comparison

## Task 1: Cache Performance for Range Sum and Update Queries

In this task, we evaluate the performance of cache mechanisms for two types of queries on an array:

1. **Range Sum Queries**: Calculate the sum of elements between indices L and R.
2. **Update Queries**: Update a specific index in the array.

### Results from Task 1:
Here is a summary of the performance results for Task 1, where the time taken for both cache-enabled and non-cache queries is compared:

| No Cache Time (s) | Cache Time (s) | Cache Hits |
|-------------------|----------------|------------|
"""
    # Assuming task_1_results is a list of tuples like ('no_cache_time', value), adjust the formatting
    readme_content += f"| {task_1_results['no_cache_time']:<18} | {task_1_results['cache_time']:<14.8f} | {task_1_results['cache_hits']:<10} |\n"  # Replace 'N/A' with actual data if available

    readme_content += """
## Conclusion

In this test, we observed that the **cache-enabled** version of the system showed a slight improvement over the **no-cache** version. The **No Cache Time** was approximately **{no_cache_time} seconds**, while the **Cache Time** was slightly lower at **{cache_time} seconds**. Additionally, there were **{cache_hits} cache hits**, which indicates that the caching mechanism successfully reused previous results to optimize performance.

Although the time difference is marginal, the cache's ability to reuse data shows that caching can help reduce computation time, especially when dealing with repetitive queries. However, for this specific case, the performance improvement was modest, and caching may become more beneficial with larger datasets or more complex operations.
""".format(no_cache_time=task_1_results['no_cache_time'], cache_time=task_1_results['cache_time'], cache_hits=task_1_results['cache_hits'])

    readme_content += """
    
    
    
## Task 2: Fibonacci Calculation with LRU Cache vs Splay Tree

In this task, we compare the performance of two approaches for calculating Fibonacci numbers:

1. **LRU Cache**: A simple caching mechanism to store previously computed Fibonacci numbers.
2. **Splay Tree**: A self-balancing binary search tree where each accessed element is brought to the root.

### Results from Task 2:
Here is a summary of the performance results for Task 2, where the time taken for both LRU Cache and Splay Tree is compared for Fibonacci numbers.

| n   | LRU Cache Time (s) | Splay Tree Time (s) |
|-----|--------------------|---------------------|
"""
    for n, lru_time, splay_time in task_2_results:
        readme_content += f"| {n:<3} | {lru_time:<18.8f} | {splay_time:<18.8f} |\n"

    readme_content += """
    
### Plots:
Below are the performance comparison plots:

#### Fibonacci Calculation Performance (LRU Cache vs Splay Tree)
![Fibonacci Calculation Performance](./plots/fibonacci_comparison.png)

## Conclusion

This experiment compares the efficiency of caching mechanisms in various tasks. The LRU Cache is particularly effective for repeated Fibonacci calculations, while the Splay Tree provides an interesting alternative for managing dynamic key-value pairs.
"""

    # Write to README.md file
    with open("README.md", "w") as readme_file:
        readme_file.write(readme_content)

    print("\nREADME.md file has been generated with the results and plots.")


if __name__ == "__main__":
    main()
