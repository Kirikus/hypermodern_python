# flamegraph: measuring performance

Measure first, optimize second, celebrate third.

## Measuring performance

Profiling refers to the systematic measurement and analysis of a running program to collect statistics on execution time, function calls, memory usage, and other metrics. These statistics reveal performance bottlenecks, often called hot spots, where the majority of time or resources are consumed.

Improving performance always starts with profiling because intuition about slow sections is frequently incorrect. Changes made without data can introduce new issues or fail to deliver meaningful gains. Profiling ensures that optimization efforts focus on the most impactful areas first.

While a lot of performance metrics can be measured, such as memory and time usage, disk operations, cache misses, etc., this manual focuses on measuring what code parts (functions or individual lines) contibute to the total execution time.

## Naive approach

A common initial approach to measuring execution speed involves wrapping code in calls to `time.time()` or similar functions from the [time](https://docs.python.org/3/library/time.html) module and subtracting start and end times. While simple, this method suffers from several drawbacks:

- Captures only a single run, making it impossible to calculate standard deviation.
- Remains sensitive to background system load, garbage collection, and other transient factors.
- Produces results that are hard to reproduce or compare reliably.
- Can have some system- or OS-specific differences between PCs.
- Clocks from this package are not always monotonic—system clock adjustments (NTP, daylight saving, manual changes) could make it jump backward.

The built-in [timeit](https://docs.python.org/3/library/timeit.html) module provides a better alternative:

- It executes the target code snippet many times automatically.
- Disables garbage collection during timing for consistency.
- Reports the best or average time across repetitions.
- Distinguishes between setup and execution.
- Has many interfaces: python, command-line and [Jupiter magic](https://ipython.readthedocs.io/en/stable/interactive/magics.html#magic-timeit).

## Profilers

**Profiler** is a tool that measures, for example, the space (memory) or time usage of a program, frequencies of particular instructions, frequency and duration of function calls, or other statistics important for the performance.

There are two types of profilers:

- **Deterministic**, **event-based** or **instrumentation profilers**. These profilers measure some constant metric by affect program execution. For example, such profilers may add hooks on function calls to monitor every change of context. Running them again on the same code will, if code execution by itself is deterministic, provide the same results.
- **Statistical** or **sampling** profilers. These profilers probe the target program at regular intervals to get its current state. Running them again on the same code will, even if code execution by itself is deterministic, provide different results.

Neither category is "more precise": while only the first group accurately measures function calls (which can be used, for example, to compare required number of iterations for algorithm convergence), the later are much less invasive. Using deterministic profilers can, dependent on the code in question, slow down code by the orders of magnitude.

## Outputs

Different profilers can also provide results in different forms:

- **Function statistics table**\
  Lists each function or method with columns for: number of calls, total time, cumulative time, time per call, and percentage of total runtime.

- **Line-by-line statistics**\
  Detailed table showing execution time or memory usage broken down by individual source code lines.

- **Call tree / call graph (textual)**\
  Hierarchical representation of function calls showing parent–child relationships and aggregated times.

- **Flat profile**\
  Sorted list of functions by time spent, without call hierarchy (often the default “flat” view in many profilers).

While technically just a form of call tree statistics, flame graphs can be noted as a particularly expressive visual form.

A flame graph is a visualization technique that represents the call stack of a program as a stack of colored rectangles. The width of each rectangle corresponds to the proportion of total execution time spent in that function or code path, while the vertical stacking shows the call hierarchy. Wider sections indicate hotter code paths. Flame graphs are interactive in SVG format, allowing users to zoom into specific branches for detailed inspection:

.. raw:: html

<object data="../_static/flamegraph_example.svg"
type="image/svg+xml"
width="100%"
style="max-width: 100%; height: auto;">
</object>

## Python profilers

- **[cProfile](https://docs.python.org/3/library/profile.html)** (built-in)\
  Deterministic instrumentation profiler included in the Python standard library. It records exact call counts and cumulative times for every function.

- **[line_profiler](https://github.com/pyutils/line_profiler)**\
  Line-by-line profiler that measures execution time for individual lines within decorated functions.

- **[py-spy](https://github.com/benfred/py-spy)**\
  Low-overhead sampling profiler that can attach to running processes and generate flame graphs directly.

- **[memory_profiler](https://github.com/pythonprofilers/memory_profiler)**\
  Line-by-line memory usage profiler that tracks memory consumption per line.

- **[memray](https://github.com/bloomberg/memray)**\
  High-performance memory profiler capable of generating flame graphs, tables, and interactive reports for both Python and native allocations.

- **[tracemalloc](https://docs.python.org/3/library/tracemalloc.html)** (built-in)\
  Tracks memory allocations and allows comparison of snapshots to detect leaks or unexpected growth.

- **[fil-profiler](https://github.com/pythonspeed/filprofiler)** (now part of [Scalene](https://github.com/plasma-umass/scalene))\
  Memory profiler focused on identifying peak memory usage and allocation hotspots.

- **[Scalene](https://github.com/plasma-umass/scalene)**\
  High-precision CPU + memory + GPU profiler with line-level granularity and low overhead.

- **[torch.profiler](https://pytorch.org/docs/stable/profiler.html)** (PyTorch-specific)\
  Specialized profiler for PyTorch models, capturing tensor operations, GPU kernels, and CPU activities.

Additionally, usual profiler outputs can be converted to visual forms:

- **[SnakeViz](https://jiffyclub.github.io/snakeviz/)**\
  Visualization tool that turns `cProfile` output into interactive sunburst and call graphs.
- [flameprof](https://github.com/baverman/flameprof)
  Visualization tool that turns `cProfile` output into a flame graph.
- [gprof2dot](https://github.com/jrfonseca/gprof2dot)
  Visualization tool that turns `cProfile` output into a dot graphs.

## Suggested profilers

`py-spy` can be the great starting point, while `Scalene` is the tool that satisfies most needs
