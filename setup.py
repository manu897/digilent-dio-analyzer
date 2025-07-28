#!/usr/bin/env python3
"""
Setup script for Digilent DIO Analyzer
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    try:
        print("Installing required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def check_digilent_software():
    """Check if Digilent WaveForms software is installed"""
    print("\n📋 Checking for Digilent WaveForms software...")
    
    # Common installation paths
    possible_paths = [
        "/Applications/WaveForms.app",  # macOS
        "C:\\Program Files (x86)\\Digilent\\WaveFormsSDK",  # Windows
        "/usr/share/digilent/waveforms"  # Linux
    ]
    
    found = False
    for path in possible_paths:
        if os.path.exists(path):
            print(f"✅ Found WaveForms at: {path}")
            found = True
            break
    
    if not found:
        print("⚠️  Digilent WaveForms software not found!")
        print("   Please download and install from: https://digilent.com/reference/software/waveforms/waveforms-3/start")
        print("   The software is required for hardware communication.")
    
    return found

def main():
    """Main setup function"""
    print("🔧 Setting up Digilent DIO Analyzer")
    print("=" * 40)
    
    # Install Python packages
    if not install_requirements():
        sys.exit(1)
    
    # Check for Digilent software
    check_digilent_software()
    
    print("\n🎉 Setup complete!")
    print("\nTo run the analyzer:")
    print("  cd src")
    print("  python main.py")
    
    print("\nNote: If you don't have Digilent hardware connected,")
    print("      the software will run in simulation mode.")

if __name__ == "__main__":
    main()
