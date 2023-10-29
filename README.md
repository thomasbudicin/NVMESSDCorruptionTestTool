# NVMe SSD Corruption Test Tool

## Introduction
The NVMe SSD Corruption Test Tool is a Python-based utility designed for checking the integrity and reliability of NVMe SSDs. It performs read and write tests and verifies data integrity using MD5 checksums.

## Features
- User-friendly GUI.
- RAM and SSD testing options.
- Customizable test size.
- Progress display.
- Time and data statistics.
- Abort functionality.
- No installation required.

## Requirements
- Windows 7/10/11.
- NVMe SSD.
- Minimum 1 GB RAM.
- Python 3.x

## Installation
### Python Installation
1. Download Python from [Python's official website](https://www.python.org/downloads/windows/).
2. Follow the installation instructions. Make sure to check the "Add Python to PATH" option during installation.

### Dependencies Installation
After installing Python, open a command prompt or terminal and run the following command to install necessary dependencies:
```bash
pip install tk hashlib threading
```

## Usage

- Download the Script: Download NVMe_SSD_Corruption_Test_Tool_v1.py.
- Run the Script: Open a command prompt or terminal, navigate to the script's directory, and execute:
```bash
- python NVMe_SSD_Corruption_Test_Tool_v1.py
```
- Start the Test: In the application, click "Start Test" and select the size in GB for the test.
- Choose Test Mode: Decide between RAM or SSD testing.
- Monitor Progress: Watch the progress and statistics during the test.
- Abort if Necessary: Use the "Abort Test" button to stop the test early if needed.
- Review Results: Check the final results after the test completes.

## Disclaimer
Intensive read/write operations are involved. Back up data before use. No liability for data loss or hardware damage.

![nvme0](https://github.com/thomasbudicin/NVMESSDCorruptionTestTool/assets/149277877/d439a021-1163-4605-87dd-21e59146be46)
![nvme1](https://github.com/thomasbudicin/NVMESSDCorruptionTestTool/assets/149277877/1c61d3c7-1fc4-4266-9b63-6d5426cd071a)
![nvme2](https://github.com/thomasbudicin/NVMESSDCorruptionTestTool/assets/149277877/beff9d2b-743c-4bf3-a7ef-d303aee19b8d)
