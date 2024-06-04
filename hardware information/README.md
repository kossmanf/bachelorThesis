
# Hardware Information Tool

## Description
This program is designed to provide detailed information about the hardware configuration of the system where it is run. This is done for documenting the computing environment used for the research project.

## Features
- **CUDA Version**: Displays the CUDA version available to PyTorch, if applicable.
- **PyTorch Version**: Shows the installed PyTorch version.
- **Operating System Info**: Reports the operating system type and version.
- **CPU Info**: Outputs detailed CPU specifications.
- **GPU Info**: Lists the GPU model being used if available.
- **RAM Info**: Provides total RAM available in the system.

### Requirements
- Python 3.x
- PyTorch
- For Linux and MacOS systems, certain commands might require sudo privileges for installation.

## Usage
Run the script from the command line:

```bash
python hardwareInformation.py
```