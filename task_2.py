import timeit
from functools import lru_cache
import matplotlib.pyplot as plt


class SplayTreeNode:
    """A node in the Splay Tree."""
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None


class SplayTree:
    """Splay Tree implementation."""
    def __init__(self):
        self.root = None

    def _splay(self, root, key):
        """Splay operation to bring the key to the root."""
        if not root or root.key == key:
            return root

        if key < root.key:
            if not root.left:
                return root
            if key < root.left.key:
                root.left.left = self._splay(root.left.left, key)
                root = self._rotate_right(root)
            elif key > root.left.key:
                root.left.right = self._splay(root.left.right, key)
                if root.left.right:
                    root.left = self._rotate_left(root.left)
            return self._rotate_right(root) if root.left else root

        else:
            if not root.right:
                return root
            if key > root.right.key:
                root.right.right = self._splay(root.right.right, key)
                root = self._rotate_left(root)
            elif key < root.right.key:
                root.right.left = self._splay(root.right.left, key)
                if root.right.left:
                    root.right = self._rotate_right(root.right)
            return self._rotate_left(root) if root.right else root

    def _rotate_left(self, x):
        """Perform a left rotation."""
        y = x.right
        x.right = y.left
        y.left = x
        return y

    def _rotate_right(self, x):
        """Perform a right rotation."""
        y = x.left
        x.left = y.right
        y.right = x
        return y

    def search(self, key):
        """Search for a key in the Splay Tree."""
        self.root = self._splay(self.root, key)
        return self.root.value if self.root and self.root.key == key else None

    def insert(self, key, value):
        """Insert a key-value pair into the Splay Tree."""
        if not self.root:
            self.root = SplayTreeNode(key, value)
            return

        self.root = self._splay(self.root, key)

        if self.root.key == key:
            self.root.value = value
            return

        new_node = SplayTreeNode(key, value)
        if key < self.root.key:
            new_node.right = self.root
            new_node.left = self.root.left
            self.root.left = None
        else:
            new_node.left = self.root
            new_node.right = self.root.right
            self.root.right = None

        self.root = new_node


@lru_cache(maxsize=None)
def fibonacci_lru(n):
    """Fibonacci calculation with LRU Cache."""
    if n <= 1:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)


def fibonacci_splay(n, tree):
    """Fibonacci calculation with Splay Tree."""
    cached_value = tree.search(n)
    if cached_value is not None:
        return cached_value

    if n <= 1:
        result = n
    else:
        result = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)

    tree.insert(n, result)
    return result


def measure_performance():
    """Measure performance of Fibonacci calculation using both approaches."""
    results = []
    tree = SplayTree()

    for n in range(0, 1000, 50):
        # Measure time for LRU Cache
        lru_time = timeit.timeit(lambda: fibonacci_lru(n), number=1)

        # Measure time for Splay Tree
        splay_time = timeit.timeit(lambda: fibonacci_splay(n, tree), number=1)

        results.append((n, lru_time, splay_time))

    return results


def plot_results(results):
    """Plot performance results and save as an image."""
    n_values = [x[0] for x in results]
    lru_times = [x[1] for x in results]
    splay_times = [x[2] for x in results]

    plt.figure(figsize=(10, 6))
    plt.plot(n_values, lru_times, label="LRU Cache", marker='o')
    plt.plot(n_values, splay_times, label="Splay Tree", marker='s')

    plt.xlabel("n (Fibonacci Number Index)")
    plt.ylabel("Time (s)")
    plt.title("Performance Comparison: LRU Cache vs. Splay Tree")
    plt.legend()
    plt.grid()
    plt.tight_layout()

    # Save plot as PNG image
    plt.savefig("plots/fibonacci_comparison.png")
    plt.close()


def print_results_table(results):
    """Print results in a formatted table."""
    print(f"{'n':<10}{'LRU Cache Time (s)':<20}{'Splay Tree Time (s)':<20}")
    print("-" * 50)
    for n, lru_time, splay_time in results:
        print(f"{n:<10}{lru_time:<20.8f}{splay_time:<20.8f}")


if __name__ == "__main__":
    # Measure performance
    performance_results = measure_performance()

    # Print results as a table
    print_results_table(performance_results)

    # Plot the results
    plot_results(performance_results)
