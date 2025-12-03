import time
from functools import wraps
from typing import Callable, Any

def timer(name: str | None = None) -> Callable:
    """Decorator to time the execution of a function."""
    def decorator(func: Callable) -> Callable:
        label = name or func.__name__
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
            print(f"Time taken to execute {label}: {execution_time:.3f}ms\n")
            return result
        return wrapper
    return decorator

def time_both_parts(part_one_func: Callable, part_two_func: Callable, *args, **kwargs) -> None:
    """Time both parts of an AOC solution."""
    total_start = time.perf_counter()
    
    timer(part_one_func(*args, **kwargs))
    timer(part_two_func(*args, **kwargs))
    
    total_end = time.perf_counter()
    total_time = (total_end - total_start) * 1000
    
    print("="*50)
    print(f"Total execution time: {total_time:.3f}ms")
    print("="*50)
    