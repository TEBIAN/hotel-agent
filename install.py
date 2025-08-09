#!/usr/bin/env python3
"""
Installation script for Hotel Agent dependencies.
This script handles PyTorch installation properly to avoid wheel building issues.
"""

import subprocess
import sys
import platform

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("🚀 Starting Hotel Agent installation...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version} detected")
    
    # Upgrade pip
    if not run_command(f"{sys.executable} -m pip install --upgrade pip", "Upgrading pip"):
        sys.exit(1)
    
    # Install PyTorch first (this is the key fix)
    pytorch_command = f"{sys.executable} -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu"
    if not run_command(pytorch_command, "Installing PyTorch"):
        print("⚠️  PyTorch installation failed. Trying alternative method...")
        # Fallback to regular torch installation
        if not run_command(f"{sys.executable} -m pip install torch", "Installing PyTorch (fallback)"):
            sys.exit(1)
    
    # Install other dependencies
    dependencies = [
        "streamlit>=1.28.0",
        "pandas>=2.0.0", 
        "scikit-learn>=1.3.0",
        "transformers>=4.30.0",
        "plotly>=5.15.0",
        "numpy>=1.21.0"
    ]
    
    for dep in dependencies:
        if not run_command(f"{sys.executable} -m pip install {dep}", f"Installing {dep}"):
            sys.exit(1)
    
    print("\n🎉 Installation completed successfully!")
    print("\nTo run the application:")
    print("  streamlit run app/main.py")
    print("\nTo generate sample data:")
    print("  python data_generator.py")
    print("\nOr use Docker:")
    print("  docker build -t hotel-agent .")
    print("  docker run -p 8501:8501 hotel-agent")

if __name__ == "__main__":
    main()


