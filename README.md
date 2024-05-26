# FPGA-Gold-Miner
### Introduction
This is the github repository for the ELEC50009 - Information module coursework. FPGA Gold Miner is an FPGA-based multiplayer interactive game. Utilizing the DE10-Lite FPGA board and NIOS II softcore, along with server-client communication based on AWS, it enables two players, using DE10 as gamepads, to enjoy the classic Gold Miner game.

### Structure
```bash
FPGA-Gold_Miner/
│
├──coursework_v1.elf # software project
├──DE10_LITE_Golden_Top.sof # NIOS hardware bit-stream file
├──gamebox.py # gamebox library
├──Gold-MinerBasicClient.py # Game file and Client script
├──host.py # UART communication with FPGA
├──tcpserver.py # Server script
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
├── picture/  # pictures used in game 
├── images/
├── input.txt # temporary file for game 
├── output.txt # temporary file for game 
├── .gitignore
└── README.md
```

### Tutorial

1. Initialise FPGA
```bash
Goto Quartus -> Tools -> Programmer -> Add file...
Open <path>\FPGA-Gold-Miner\src\DE10_LITE_Golden_Top.sof
Click Start
```

2. Create UARTconnection between `host.py` script and DE10-Lite
```bash
# Open NIOS II command shell
& '<path>\intelFPGA_lite\18.1\nios2eds\Nios II Command Shell.bat'
# Locate the folder
cd <path>/FPGA-Gold-Miner/src
# Download .elf project 
nios2-download -g coursework_v1.elf

run host.py
```

3. Set Up server
```bash
Set up AWS server (refer to https://github.com/Aaron-Zhao123/ELEC50009/blob/main/lab5/lab5.pdf)
# Open server file
python3 tcpserver.py
```

4. Start the game
```bash
run Gold-MinerBasicClient.py
```

![Game Interface](./images/game_interface.png)

### Demo

https://github.com/lgxi24/FPGA-Gold-Miner/assets/115477676/4af19abd-b736-4b01-b00d-a21ac7633fd7




