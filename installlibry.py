script_content = """
import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# List of required libraries
required_libraries = [
    "schedule",
    "tk"
]

for library in required_libraries:
    install(library)

print("All required libraries have been installed.")
"""

with open("install_libraries.py", "w") as file:
    file.write(script_content)