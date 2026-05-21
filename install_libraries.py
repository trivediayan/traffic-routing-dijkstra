import os
import sys
import subprocess

packages = ["networkx", "pandas", "matplotlib"]

def install(package):
    """Install a Python package using pip"""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

for package in packages:
    try:
        __import__(package)
        print(f"✅ {package} is already installed.")
    except ImportError:
        print(f"📦 Installing {package}...")
        install(package)
        print(f"✅ {package} installed successfully!")

print("\n🎉 All required libraries are ready to use!")
