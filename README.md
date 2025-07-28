# Digilent DIO Analyzer

This project is designed to monitor the DIO 0 pin of a Digilent device, detect toggles, and record the timestamps of each toggle. It also analyzes the correlation between these toggles and heap memory size, which can help in diagnosing potential crashes or memory issues.

## Project Structure

```
digilent-dio-analyzer
├── src
│   ├── main.py          # Entry point of the application
│   ├── dio_reader.py    # DIOReader class for interfacing with DIO 0 pin
│   ├── heap_monitor.py   # HeapMonitor class for monitoring heap memory
│   └── utils.py         # Utility functions for time formatting and logging
├── requirements.txt     # Project dependencies
├── README.md            # Project documentation
└── tests
    ├── test_dio_reader.py  # Unit tests for DIOReader class
    ├── test_heap_monitor.py  # Unit tests for HeapMonitor class
    └── test_utils.py       # Unit tests for utility functions
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/digilent-dio-analyzer.git
   cd digilent-dio-analyzer
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:
```
python src/main.py
```

The application will start monitoring the DIO 0 pin and will log the timestamps of each toggle detected within a 20 millisecond gap.

## Purpose

The Digilent DIO Analyzer aims to provide insights into the behavior of the DIO 0 pin and its correlation with heap memory usage. This can be particularly useful for developers and engineers working with embedded systems to ensure stability and performance.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.