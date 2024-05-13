import os
import platform
import subprocess
import torch

def get_cuda_version():
    try:
        return torch.version.cuda
    except AttributeError:
        return "CUDA not available"

def get_pytorch_version():
    return torch.__version__

def get_os_info():
    return platform.system(), platform.release()

def get_cpu_info():
    if platform.system() == "Windows":
        return platform.processor()
    elif platform.system() == "Darwin":
        return subprocess.run(['sysctl', '-n', 'machdep.cpu.brand_string'], capture_output=True, text=True).stdout.strip()
    else:
        return subprocess.run(['cat', '/proc/cpuinfo'], capture_output=True, text=True).stdout.split('\n')[4].split(':')[1].strip()

def get_gpu_info():
    try:
        from torch.cuda import get_device_name
        return get_device_name(0)
    except Exception as e:
        return str(e)

def get_ram_info():
    if platform.system() == "Windows":
        import psutil
        return f"{psutil.virtual_memory().total / (1024**3):.2f} GB"
    else:
        mem_info = subprocess.run(['grep', 'MemTotal', '/proc/meminfo'], capture_output=True, text=True).stdout
        return f"{int(mem_info.split()[1]) / 1024:.2f} MB"

def main():
    print(f"CUDA Version: {get_cuda_version()}")
    print(f"PyTorch Version: {get_pytorch_version()}")
    os_type, os_version = get_os_info()
    print(f"Operating System: {os_type} {os_version}")
    print(f"CPU: {get_cpu_info()}")
    print(f"GPU: {get_gpu_info()}")
    print(f"RAM: {get_ram_info()}")

if __name__ == "__main__":
    main()