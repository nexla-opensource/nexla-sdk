#!/usr/bin/env python3
"""Circuit breaker pattern implementation for Nexla operations."""

import time
import functools
from enum import Enum
from typing import Callable, TypeVar, Optional

T = TypeVar("T")


class CircuitState(Enum):
    """Circuit breaker states."""

    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Failing fast, not executing calls
    HALF_OPEN = "half_open"  # Testing if service recovered


class CircuitBreaker:
    """
    Circuit breaker to prevent cascading failures.

    Tracks failures and opens the circuit after a threshold is reached.
    When open, calls fail immediately without executing. After a timeout,
    the circuit enters half-open state to test if the service recovered.

    Args:
        failure_threshold: Number of failures before opening circuit (default: 5)
        timeout: Seconds to wait before attempting reset (default: 60)
        expected_exception: Exception type to catch (default: Exception)

    Example:
        breaker = CircuitBreaker(failure_threshold=3, timeout=30)

        def risky_operation():
            return client.sources.list()

        try:
            result = breaker.call(risky_operation)
        except Exception as e:
            print(f"Circuit breaker prevented call or operation failed: {e}")
    """

    def __init__(
        self,
        failure_threshold: int = 5,
        timeout: float = 60.0,
        expected_exception: type = Exception,
    ):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.expected_exception = expected_exception
        self.failure_count = 0
        self.last_failure_time: Optional[float] = None
        self.state = CircuitState.CLOSED

    def call(self, func: Callable[..., T], *args, **kwargs) -> T:
        """
        Call function through circuit breaker.

        Args:
            func: Function to call
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from func

        Raises:
            Exception: If circuit is open or func raises exception
        """
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
                print("Circuit breaker entering HALF_OPEN state")
            else:
                time_remaining = self._time_until_reset()
                raise Exception(
                    f"Circuit breaker is OPEN. Retry after {time_remaining:.0f}s"
                )

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except self.expected_exception:
            self._on_failure()
            raise

    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt reset."""
        if self.last_failure_time is None:
            return True
        elapsed = time.time() - self.last_failure_time
        return elapsed >= self.timeout

    def _time_until_reset(self) -> float:
        """Calculate time remaining until reset attempt."""
        if self.last_failure_time is None:
            return 0.0
        elapsed = time.time() - self.last_failure_time
        return max(0.0, self.timeout - elapsed)

    def _on_success(self):
        """Handle successful call."""
        if self.state == CircuitState.HALF_OPEN:
            print("Circuit breaker closing after successful test")
            self.state = CircuitState.CLOSED
        self.failure_count = 0

    def _on_failure(self):
        """Handle failed call."""
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.state == CircuitState.HALF_OPEN:
            # Failed in half-open state, reopen circuit
            print("Circuit breaker reopening after failed test")
            self.state = CircuitState.OPEN
        elif self.failure_count >= self.failure_threshold:
            # Threshold reached, open circuit
            print(
                f"Circuit breaker opening after {self.failure_count} failures "
                f"(threshold: {self.failure_threshold})"
            )
            self.state = CircuitState.OPEN

    def reset(self):
        """Manually reset circuit breaker to closed state."""
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = None
        print("Circuit breaker manually reset to CLOSED state")

    @property
    def is_open(self) -> bool:
        """Check if circuit is open."""
        return self.state == CircuitState.OPEN

    @property
    def is_closed(self) -> bool:
        """Check if circuit is closed."""
        return self.state == CircuitState.CLOSED


def circuit_breaker(
    failure_threshold: int = 5,
    timeout: float = 60.0,
    expected_exception: type = Exception,
):
    """
    Decorator for circuit breaker pattern.

    Args:
        failure_threshold: Number of failures before opening circuit
        timeout: Seconds to wait before attempting reset
        expected_exception: Exception type to catch

    Example:
        @circuit_breaker(failure_threshold=3, timeout=30)
        def get_source(client, source_id):
            return client.sources.get(source_id)
    """
    breaker = CircuitBreaker(failure_threshold, timeout, expected_exception)

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> T:
            return breaker.call(func, *args, **kwargs)

        return wrapper

    return decorator


# Example usage
if __name__ == "__main__":
    # Example 1: Using CircuitBreaker class directly
    breaker = CircuitBreaker(failure_threshold=3, timeout=5)

    def risky_operation(should_fail=True):
        """Simulated operation that might fail."""
        if should_fail:
            raise Exception("Simulated failure")
        return "Success!"

    print("Testing CircuitBreaker class:")
    print(f"Initial state: {breaker.state.value}")

    # Trigger failures to open circuit
    for i in range(5):
        try:
            result = breaker.call(risky_operation, should_fail=(i < 3))
            print(f"Attempt {i + 1}: {result}")
        except Exception as e:
            print(f"Attempt {i + 1}: {e}")
        print(f"State: {breaker.state.value}, Failures: {breaker.failure_count}")

    # Wait for timeout and test recovery
    print(f"\nWaiting {breaker.timeout}s for timeout...")
    time.sleep(breaker.timeout + 1)

    try:
        result = breaker.call(risky_operation, should_fail=False)
        print(f"After timeout: {result}")
    except Exception as e:
        print(f"After timeout: {e}")
    print(f"Final state: {breaker.state.value}")

    # Example 2: Using decorator
    print("\n\nTesting circuit_breaker decorator:")

    @circuit_breaker(failure_threshold=2, timeout=3)
    def another_operation(should_fail=True):
        """Another simulated operation."""
        if should_fail:
            raise Exception("Decorated function failure")
        return "Decorated success!"

    for i in range(4):
        try:
            result = another_operation(should_fail=(i < 2))
            print(f"Call {i + 1}: {result}")
        except Exception as e:
            print(f"Call {i + 1}: {e}")
