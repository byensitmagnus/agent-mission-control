import statistics
import time

from analytics.events import summarize


events = [{"name": f"event-{index % 2500}", "metadata": index} for index in range(10000)]
samples = []
for _ in range(7):
    started = time.perf_counter()
    summarize(events)
    samples.append(time.perf_counter() - started)
print(f"median_seconds={statistics.median(samples):.6f}")
