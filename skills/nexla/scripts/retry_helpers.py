#!/usr/bin/env python3
"""Retry and backoff utilities for Nexla operations."""

import functools
import random
import time
from typing import Callable, Tuple, Type, TypeVar

# Import Nexla SDK exceptions
try:
    from nexla_sdk import NexlaError, RateLimitError, ServerError
except ImportError:
    # Fallback for when SDK is not installed
    class NexlaError(Exception):
        pass

    class RateLimitError(NexlaError):
        def __init__(self, *args, **kwargs):
            super().__init__(*args)
            self.retry_after = kwargs.get("retry_after")

    class ServerError(NexlaError):
        pass


T = TypeVar("T")


def exponential_backoff_retry(
    max_attempts: int = 5,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exceptions: Tuple[Type[Exception], ...] = (RateLimitError, ServerError),
):
    """
    Decorator for exponential backoff retry with jitter.

    Args:
        max_attempts: Maximum number of retry attempts (default: 5)
        base_delay: Base delay in seconds for exponential backoff (default: 1.0)
        max_delay: Maximum delay in seconds (default: 60.0)
        exceptions: Tuple of exception types to catch and retry (default: RateLimitError, ServerError)

    Returns:
        Decorator function

    Example:
        @exponential_backoff_retry(max_attempts=3)
        def create_source(client, config):
            return client.sources.create(config)
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> T:
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts - 1:
                        # Last attempt, re-raise the exception
                        raise

                    # Calculate delay with exponential backoff
                    if (
                        isinstance(e, RateLimitError)
                        and hasattr(e, "retry_after")
                        and e.retry_after
                    ):
                        delay = min(e.retry_after, max_delay)
                    else:
                        delay = min(base_delay * (2**attempt), max_delay)

                    # Add jitter (0-10% of delay) to prevent thundering herd
                    jitter = random.uniform(0, delay * 0.1)
                    sleep_time = delay + jitter

                    print(f"Attempt {attempt + 1}/{max_attempts} failed: {e}")
                    print(f"Retrying in {sleep_time:.1f}s...")
                    time.sleep(sleep_time)

            # Should not reach here
            raise RuntimeError("Maximum retry attempts exceeded")

        return wrapper

    return decorator


def simple_retry(max_attempts: int = 3, delay: float = 1.0):
    """
    Simple retry decorator with fixed delay.

    Args:
        max_attempts: Maximum number of retry attempts (default: 3)
        delay: Fixed delay between retries in seconds (default: 1.0)

    Returns:
        Decorator function

    Example:
        @simple_retry(max_attempts=3, delay=2.0)
        def get_source(client, source_id):
            return client.sources.get(source_id)
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> T:
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    print(f"Attempt {attempt + 1}/{max_attempts} failed: {e}")
                    print(f"Retrying in {delay}s...")
                    time.sleep(delay)

            raise RuntimeError("Maximum retry attempts exceeded")

        return wrapper

    return decorator


# Example usage
if __name__ == "__main__":
    # Example 1: Using exponential_backoff_retry decorator
    @exponential_backoff_retry(max_attempts=3, base_delay=1.0)
    def example_operation():
        """Simulated operation that might fail."""
        import random

        if random.random() < 0.7:  # 70% chance of failure
            raise ServerError("Simulated server error")
        return "Success!"

    # Example 2: Using simple_retry decorator
    @simple_retry(max_attempts=3, delay=0.5)
    def another_operation():
        """Another simulated operation."""
        import random

        if random.random() < 0.5:  # 50% chance of failure
            raise Exception("Simulated error")
        return "Success!"

    # Test the decorators
    print("Testing exponential_backoff_retry:")
    try:
        result = example_operation()
        print(f"Result: {result}")
    except Exception as e:
        print(f"Failed after all retries: {e}")

    print("\nTesting simple_retry:")
    try:
        result = another_operation()
        print(f"Result: {result}")
    except Exception as e:
        print(f"Failed after all retries: {e}")
