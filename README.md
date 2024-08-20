# Rational Monitor Script

This repository contains the `Rational Monitor` script, a Python tool designed for monitoring Linear Temporal Logic (LTL) formulas over a sequence of events. The script supports compositional monitoring with the ability to optimize the evaluation process using resource constraints.

## Features

- **Compositional Monitoring**: Supports `AND`, `OR`, and `NOT` compositional monitors.
- **Temporal Monitoring**: Handles LTL formulas with temporal operators.
- **Resource-Bound Optimization**: Utilizes a knapsack approach to select the most relevant indistinguishability relation to break under resource constraints.
- **Dynamic Formula Revision**: Revises the monitoring process based on a time window and resource availability.

## Requirements

- Python >=3.6 (tested on 3.10.12)
- Required Python libraries:
  - `spot` (https://spot.lre.epita.fr/)
  - `importlib` (https://pypi.org/project/importlib/)
  
## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/AngeloFerrando/RationalMonitor.git
   ```

## Usage

### Command-Line Usage

The `Rational Monitor` script can be run from the command line using the following format:

```bash
python script.py <ltl> <ap> <sim> <costs> <resource_bound> <time_window> <filename> <metric_module>
```

#### Arguments:

- `ltl`: The LTL formula to monitor (e.g., `!G!(x && Xi) || F(Xg || (Fj U o))`).
- `ap`: A comma-separated list of atomic propositions enclosed in brackets (e.g., `[a,b,c,d]`).
- `sim`: A semicolon-separated list of equivalence classes, where each trace is a list of atomic propositions enclosed in brackets (e.g., `[a,b];[c,d]`).
- `costs`: Costs associated with each atomic proposition, formatted as `prop:cost` pairs separated by semicolons (e.g., `[a,b]:10;[c,d]:10`).
- `resource_bound`: A floating-point number representing the resource bound for the knapsack problem (e.g., `10`).
- `time_window`: An integer representing the time window for monitoring (e.g., `1`).
- `filename`: The name of the file containing the events to monitor (e.g., `test.txt`).
- `metric_module`: The name of the Python module that contains the metric function for calculating payoffs (e.g., `metrics.metric_1`).

#### Example:

```bash
python rational_monitor.py '!G!(x && Xi) || F(Xg || (Fj U o))' '[a,b,c,d]' '[a,b];[c,d]' '[a,b]:10;[c,d]:10' 10 1 'test.txt' 'metrics.metric_1'
```

### To test case study

```bash
python case_study/test.py
```

### To run experiments

To generate N random LTL formulas in the `props.txt` file:

```bash
python ltl_generator.py <N>
```

To generate N random event traces of maximum length L into the folder `traces/`:

```bash
python trace_generator.py <N> <L>
```

To run experiments on the so generated LTL formulas and event traces:

```bash
python experiments.py 
```

The results of the experiments can be found in the `res.txt` file.

### Programmatic Usage

You can also use the script within another Python program by simulating command-line arguments with a list:

```python
import argparse
from script import main  # Assuming the script is named 'script.py'

args = [
    "!G!(x && Xi) || F(Xg || (Fj U o))",
    "[a,b,c,d]",
    "[a,b];[c,d]",
    "[a,b]:10;[c,d]:10",
    "10",
    "1",
    "test.txt",
    "metric_1"
]

parser = argparse.ArgumentParser(description='Rational Monitor for LTL formulas.')
# Define your arguments as done in the script...
parsed_args = parser.parse_args(args)
main(parsed_args)
```

### Metric Module

The `metric_module` is a Python module that contains a `metric` function, which is used to calculate payoffs for the atomic propositions. Ensure that the module is in your Python path or is accessible by the script.

### Event File Format

The event file should contain a sequence of events, each on a new line. Each event is a comma-separated list of atomic propositions that are true at that time step. Example:

```txt
a,b
c
a,c,d
b
```

## Output

The script will output the final verdict after processing all events in the provided file:

```
Verdict: True
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an issue.