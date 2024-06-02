# Importing necessary modules
import os
import platform
import subprocess
import torch

# Program description
# This program was used to print the hadware information which was used for the research project

def getCudaVersion():
    # Returns the CUDA version used by PyTorch or a message if CUDA is not available
    try:
        return torch.version.cuda
    except AttributeError:
        return "CUDA not available"

def getPytorchVersion():
    # Returns the version of PyTorch installed
    return torch.__version__

def getOsInfo():
    # Returns the operating system type and version
    return platform.system(), platform.release()

def getCpuInfo():
    # Retrieves the CPU information based on the operating system
    if platform.system() == "Windows":
        return platform.processor()
    elif platform.system() == "Darwin":
        return subprocess.run(['sysctl', '-n', 'machdep.cpu.brand_string'], capture_output=True, text=True).stdout.strip()
    else:
        return subprocess.run(['cat', '/proc/cpuinfo'], capture_output=True, text=True).stdout.split('\n')[4].split(':')[1].strip()

def getGpuInfo():
    # Attempts to get the GPU name using PyTorch; returns an error message if unsuccessful
    try:
        from torch.cuda import get_device_name
        return get_device_name(0)
    except Exception as e:
        return str(e)

def getRamInfo():
    # Retrieves RAM information based on the operating system
    if platform.system() == "Windows":
        import psutil
        return f"{psutil.virtual_memory().total / (1024**3):.2f} GB"
    else:
        mem_info = subprocess.run(['grep', 'MemTotal', '/proc/meminfo'], capture_output=True, text=True).stdout
        return f"{int(mem_info.split()[1]) / 1024:.2f} MB"

def main():
    # Main function to display the system information
    print(f"CUDA Version: {getCudaVersion()}")
    print(f"PyTorch Version: {getPytorchVersion()}")
    osType, osVersion = getOsInfo()
    print(f"Operating System: {osType} {osVersion}")
    print(f"CPU: {getCpuInfo()}")
    print(f"GPU: {getGpuInfo()}")
    print(f"RAM: {getRamInfo()}")

if __name__ == "__main__":
    main()
