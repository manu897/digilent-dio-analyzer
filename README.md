# Digilent DIO Analyzer

A professional tool for monitoring Digital I/O pins on Digilent devices and analyzing signal patterns in correlation with system memory usage. This analyzer is particularly useful for debugging hardware/software interactions, detecting rapid signal sequences, and diagnosing potential system issues.

## 🚀 Features

- **Real-time DIO monitoring** using Digilent WaveForms SDK
- **Rapid toggle sequence detection** (configurable patterns)
- **System memory monitoring** with spike detection
- **Comprehensive logging** with timestamps and analysis
- **Pattern analysis** with frequency calculations
- **Graceful error handling** and simulation mode
- **Cross-platform support** (Windows, macOS, Linux)

## 📁 Project Structure

```
digilent-dio-analyzer/
├── src/
│   ├── main.py          # Main analyzer application
│   ├── dio_reader.py    # Digilent DIO interface
│   ├── heap_monitor.py  # System memory monitoring
│   └── utils.py         # Utility functions and analysis
├── tests/               # Unit tests
├── requirements.txt     # Python dependencies
├── setup.py            # Installation script
├── test_installation.py # Verification script
└── README.md           # This file
```

## 🛠️ Quick Setup

### Prerequisites
1. **Digilent WaveForms Software** - Download from [Digilent's website](https://digilent.com/reference/software/waveforms/waveforms-3/start)
2. **Python 3.7+**

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/manu897/digilent-dio-analyzer.git
   cd digilent-dio-analyzer
   ```

2. **Run the setup script:**
   ```bash
   python setup.py
   ```

3. **Verify installation:**
   ```bash
   python test_installation.py
   ```

### Manual Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Test the installation
python test_installation.py
```

## 🎯 Usage

### Basic Usage
```bash
cd src
python main.py
```

### Configuration Options
The analyzer can be configured by modifying the `DIOAnalyzer` parameters in `main.py`:

```python
analyzer = DIOAnalyzer(
    pin=0,                    # DIO pin number (0-15)
    rapid_toggle_count=6,     # Number of toggles for rapid sequence
    rapid_window_ms=60        # Time window in milliseconds
)
```

### Example Output
```
[2025-07-28 10:30:15.123] Starting DIO analysis...
[2025-07-28 10:30:15.124] Configuration: 6 toggles within 60ms
Memory: RSS=45MB, VMS=120MB, Usage=2.1%
[2025-07-28 10:30:16.200] Toggle #1 detected at 1722150616.200000
[2025-07-28 10:30:16.215] Toggle #2 detected at 1722150616.215000
...
[2025-07-28 10:30:16.250] 🚨 RAPID SEQUENCE #1 DETECTED!
[2025-07-28 10:30:16.250]    6 toggles in 50.0ms
[2025-07-28 10:30:16.250]    Frequency: 120.0 Hz
[2025-07-28 10:30:16.250]    Memory at event: 45MB RSS, 2.1% usage
```

## 🔧 Hardware Setup

### Digilent Device Connection
1. Connect your Digilent device (Analog Discovery 2, Digital Discovery, etc.)
2. Ensure WaveForms software recognizes the device
3. Connect your signal to the desired DIO pin (default: DIO 0)

### Simulation Mode
If no hardware is connected, the analyzer runs in simulation mode with:
- Random toggle generation for testing
- Mock memory monitoring
- Full logging and analysis capabilities

## 📊 Analysis Features

### Toggle Pattern Analysis
- **Frequency calculation** from toggle sequences
- **Interval timing** between consecutive toggles
- **Rapid sequence detection** within configurable windows
- **Statistical analysis** of toggle patterns

### Memory Monitoring
- **Real-time memory usage** (RSS, VMS, percentage)
- **Memory spike detection** with configurable thresholds
- **Correlation analysis** between toggles and memory usage
- **Memory usage statistics** over time

### Logging and Output
- **Timestamped events** with microsecond precision
- **Console output** for real-time monitoring
- **File logging** to `event_log.txt`
- **Final statistics** summary on shutdown

## 🧪 Testing

Run the test suite to verify functionality:

```bash
# Run all tests
python test_installation.py

# Run specific unit tests
pytest tests/
```

## 📝 Log Files

The analyzer creates detailed logs:
- **`event_log.txt`** - All events with timestamps
- Console output for real-time monitoring
- Memory usage statistics
- Toggle pattern analysis results

## ⚡ Performance

- **Low latency**: 1ms sampling rate
- **Efficient memory usage**: Rate-limited logging
- **Graceful shutdown**: Ctrl+C handling with statistics
- **Resource monitoring**: Built-in memory spike detection

## 🛡️ Error Handling

- **Hardware disconnection** - Automatic fallback to simulation
- **Missing dependencies** - Clear error messages
- **Memory issues** - Spike detection and logging
- **Graceful shutdown** - Signal handling and cleanup

## 🤝 Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

1. **"pydwf not found"**
   - Install: `pip install pydwf`
   - Ensure WaveForms software is installed

2. **"No device found"**
   - Check USB connection
   - Verify device in WaveForms software
   - Try different USB port

3. **"Permission denied"**
   - On Linux: Add user to dialout group
   - On macOS: Check system permissions

### Support

For issues and questions:
- Check the [troubleshooting guide](https://github.com/manu897/digilent-dio-analyzer/wiki)
- Open an [issue](https://github.com/manu897/digilent-dio-analyzer/issues)
- Review Digilent's [documentation](https://digilent.com/reference/software/waveforms/waveforms-3/start)