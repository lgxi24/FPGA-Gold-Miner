# FPGA-Gold-Miner
### Introduction
This is the github repository for the ELEC50009 - Information module coursework. FPGA Gold Miner is an FPGA-based multiplayer interactive game. Utilizing the DE10-Lite FPGA board and NIOS II softcore, along with server-client communication based on AWS, it enables two players, using DE10 as gamepads, to enjoy the classic Gold Miner game.

### Structure
```shell
FPGA-Gold_Miner/
│
├── src/ # game release
|   ├── picture/  # pictures used in game
|   ├── coursework_v1.elf # software project
|   ├── DE10_LITE_Golden_Top.sof # NIOS hardware bit-stream file
|   ├── gamebox.py # gamebox library
|   ├── Gold-MinerBasicClient.py # Game file and Client script
|   ├── host.py # UART communication with FPGA
|   └── tcpserver.py # Server script
│
├── Golden_Top/ # FPGA project
│   ├── ... 
│   ├── software/
|   │   ├── coursework_v1
|   |   │   ├── coursework_v1.elf # software project
|   |   │   ├── hello_world_small.c # software program of NIOS
|   |   │   └── ... 
|   |   └── coursework_v1_bsp # board support package for the project
│   ├── ... 
│   ├── coursework.qsys # QSYS HDL file
|   ├── coursework.qsys # SOPC Builder information file of the hardware
│   ├── DE10_LITE_Golden_Top.qpf # Quartus Project
|   ├── DE10_LITE_Golden_Top.sof # NIOS hardware bit-stream file
│   └── DE10_LITE_Golden_Top.v # Top level Verilog file
│
├── .gitignore
|
└── README.md
```

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
