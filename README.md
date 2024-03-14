# FPGA-Gold-Miner
### Introduction
This is the github repository for the ELEC50009 - Information module coursework. FPGA Gold Miner is an FPGA-based multiplayer interactive game. Utilizing the DE10-Lite FPGA board and NIOS II softcore, along with server-client communication based on AWS, it enables two players, using DE10 as gamepads, to enjoy the classic Gold Miner game.

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
