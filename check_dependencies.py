import subprocess
import sys

def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

required_packages = [
    'plotly==5.18.0',
    'plotly-express==0.4.1',
    'pandas',
    'numpy'
]

for package in required_packages:
    try:
        __import__(package.split('==')[0])
        print(f"{package} is already installed")
    except ImportError:
        print(f"Installing {package}...")
        install_package(package) 