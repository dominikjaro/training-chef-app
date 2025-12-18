
import subprocess
import sys

try:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "fastapi", '"uvicorn[standard]"'])
    print("Packages installed successfully.")
except subprocess.CalledProcessError as e:
    print(f"Error installing packages: {e}")
    sys.exit(1)
