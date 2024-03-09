# FPGA-Gold-Miner
Create connection between `test.py` script and DE10-Lite
```powershell
# Open NIOS II command shell
& 'path\intelFPGA_lite\18.1\nios2eds\Nios II Command Shell.bat'
# Locate the folder
cd path/Info_Proc_CW/FPGA-Gold-Miner
# Download .elf project 
nios2-download -g coursework_v1.elf

run the python script test.py
```