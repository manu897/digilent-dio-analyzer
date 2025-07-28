import time
try:
    from pydwf import DwfLibrary, DwfEnumConfigInfo
    from pydwf.core import api as dwf
    PYDWF_AVAILABLE = True
except ImportError:
    print("Warning: pydwf not available. Install with: pip install pydwf")
    PYDWF_AVAILABLE = False

class DIOReader:
    def __init__(self, pin=0):
        self.pin = pin
        self.device = None
        self.last_state = None
        self.is_reading = False
        
        if PYDWF_AVAILABLE:
            try:
                # Initialize Digilent device
                dwf_library = DwfLibrary()
                self.device = dwf_library.device.open()
                print(f"Successfully connected to Digilent device")
            except Exception as e:
                print(f"Failed to connect to Digilent device: {e}")
                print("Running in simulation mode...")
                self.device = None
        else:
            print("Running in simulation mode (pydwf not installed)")

    def start_reading(self):
        """Initialize the DIO pin for reading"""
        self.is_reading = True
        if self.device:
            try:
                # Configure the DIO pin as input
                self.device.digital_io.output_enable_set(1 << self.pin, 0)  # Set as input
                # Read initial state
                self.last_state = self._read_pin_state()
                print(f"DIO pin {self.pin} initialized for reading")
            except Exception as e:
                print(f"Error initializing DIO pin: {e}")
                self.device = None

    def stop_reading(self):
        """Stop reading and close the device"""
        self.is_reading = False
        if self.device:
            try:
                self.device.close()
                print("Digilent device connection closed")
            except Exception as e:
                print(f"Error closing device: {e}")

    def _read_pin_state(self):
        """Read the current state of the DIO pin"""
        if self.device:
            try:
                # Read the digital input state
                state = self.device.digital_io.input_status()
                return bool(state & (1 << self.pin))
            except Exception as e:
                print(f"Error reading DIO pin: {e}")
                return None
        else:
            # Simulation mode - generate random toggles occasionally
            import random
            if random.random() < 0.1:  # 10% chance of toggle
                return not self.last_state if self.last_state is not None else True
            return self.last_state

    def check_toggle(self):
        """Check if a toggle occurred on the DIO pin"""
        if not self.is_reading:
            return False
            
        current_state = self._read_pin_state()
        
        if current_state is None:
            return False
            
        # Check for state change (toggle)
        if self.last_state is not None and current_state != self.last_state:
            self.last_state = current_state
            return True
            
        self.last_state = current_state
        return False

    def get_pin_state(self):
        """Get the current state of the DIO pin"""
        return self._read_pin_state()