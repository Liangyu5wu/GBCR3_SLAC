# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a GBCR3 (GigaBit Cosmic Ray) test setup at SLAC for SEU (Single Event Upset) testing. The system tests data transmission through GBCR3 chips using FPGA-based hardware with Ethernet communication.

## Architecture

### Software Structure
The repository contains two main versions:

#### Original Version (`software/`)
- **main.py**: Original data acquisition script with hardcoded I2C configuration
- **GBCR3_Reg.py**: Original register configuration class with repetitive code
- **command_interpret.py**: Low-level Ethernet communication with FPGA
- **crc32_8.py** and **binhex.py**: Utility modules for data processing

#### Enhanced Version (`software_v2/`) - RECOMMENDED
- **main_v2.py**: Enhanced main script with command-line parameter support
- **GBCR3_Config.py**: Streamlined register configuration class following original logic
- **README.md**: Comprehensive documentation for the enhanced version
- Same utility modules copied from original version

### Hardware Components
- **firmware/**: Contains FPGA bitstream files (.bit) for different test configurations
- **load_bitstream.sh/.tcl**: Scripts for loading firmware onto FPGA using Vivado Lab

## Common Development Commands

### Enhanced Version (software_v2/) - Primary Development

```bash
# Basic data acquisition (identical to original)
python main_v2.py 100          # 100 files, normal mode
python main_v2.py 100 1        # 100 files, debug mode

# Configure specific channels without code modification
python main_v2.py 100 1 --retimed ch4:0x8
python main_v2.py 100 1 --disable ch6
python main_v2.py 100 1 --rx-config "ch4:mux_bias=0xf,clk_delay=0x8"

# Multiple channel configuration
python main_v2.py 100 1 \
    --retimed ch4:0x8 \
    --rx-config "ch6:mux_bias=0x17,clk_delay=0x5"

# Get help on all parameters
python main_v2.py --help
```

### Original Version (software/) - Legacy Support

```bash
# Requires manual code modification in main.py around line 208
python main.py 100             # 100 files, normal mode  
python main.py 100 1           # 100 files, debug mode
```

### FPGA Operations
```bash
# Load bitstream to FPGA
bash load_bitstream.sh

# Alternative bitstream files available:
# firmware/GBCR2_SEU_Test.bit (default)
# firmware/GBCR2_SEU_Test_dataReset.bit
# firmware/GBCR2_SEU_Test_newreset.bit
```

### Parameter Scanning Scripts

Enhanced version greatly simplifies automation:

```bash
#!/bin/bash
# Example: Test retimed mode across different channels and delay range
for channel in ch4 ch5 ch6; do
    for delay in {0..15}; do
        hex_delay=$(printf "0x%x" $delay)
        python main_v2.py 50 0 --retimed $channel:$hex_delay
    done
done
```

## Key Configuration

- **FPGA IP**: 192.168.2.6:1024 (hardcoded in main.py:25-26)
- **I2C Slave Address**: 0x23
- **Current Monitor**: LTC2991 at I2C address 0x4F  
- **Default Data Collection**: 50,000 words per file
- **Channel Configuration**: 9 channels (8 data + 1 filler)
- **Test Modes**: 
  - Retimed mode: `mux_bias=0xf`
  - Voted mode: `mux_bias=0x17` (default)

## Data Output Structure

Both versions generate timestamped directories:
- Original: `QAResults/YYYY-MM-DD_HH-MM-SS/`
- Enhanced: `QAResults_v2/YYYY-MM-DD_HH-MM-SS/`

### Output Files:
- **ChAll.TXT**: All channel error data with timestamps
- **Ch{N}.TXT**: Individual channel error logs (N=0-8)
- **summary.txt**: Run summary with channel statistics and timing
- **Filesummary.TXT**: Per-file statistics and channel performance
- **I2C.TXT**: I2C register verification logs (every 10 files)
- **IDD.TXT**: Current consumption monitoring

## Development Guidelines

### Working with Enhanced Version (Recommended)

1. **Parameter Configuration**: Use command-line parameters instead of modifying code
2. **Debugging**: Enable debug mode with `debug_mode=1` for detailed output
3. **Register Access**: Use `GBCR3_Config` class methods for register manipulation
4. **Batch Operations**: Use `configure_multiple_rx()` for complex setups

### Working with Original Version (Legacy)

1. **Manual Configuration**: Edit `main.py` lines 205-212 to change register settings
2. **Scan Scripts**: Use `sed` to dynamically modify Python source code
3. **Testing**: Always verify I2C register read-back matches written values

## Important Implementation Details

- **Frame Alignment**: System detects alignment using filler pattern `0x3c5c7c5c...`
- **CRC Validation**: 32-bit CRC calculated for each frame to ensure data integrity
- **Error Classification**: Distinguishes between aligned/not-aligned and error/OK frames
- **Channel Mapping**: Physical channels mapped to logical DAQ lanes via `rxchan` array
- **Current Monitoring**: LTC2991 provides real-time power consumption data
- **I2C Verification**: Registers re-read every 10 files for stability verification

## Register Configuration Details

### RX Channels (CH1-CH6)
- **MUX_bias**: Critical parameter distinguishing retimed (0xf) vs voted (0x17) modes
- **CLK_Delay**: Clock delay compensation (0x0-0xf)
- **Equalizers**: HF1/HF2/HF3 (high freq) and MF (mid freq) settings
- **CML_AmplSel**: Output amplitude control

### TX Channels (CH1-CH2)  
- **SC1/SC2**: Source current control
- **AmplSel**: Output amplitude selection
- **SR1/SR2**: Slew rate control

### Clock/DLL Settings
- **CLK_Rx_en**: RX clock enable
- **CLK_Tx_Delay**: TX clock phase delay
- **DLL settings**: Phase-locked loop configuration

## Error Handling and Debugging

- **I2C Failures**: Check register read-back verification in I2C.TXT
- **Alignment Issues**: Monitor alignment loss statistics in debug mode
- **Current Anomalies**: Track power consumption in IDD.TXT
- **Frame Errors**: Individual channel error logs provide detailed diagnostics
- **FPGA Communication**: Socket connection failures indicate hardware issues

## Testing and Validation

- **Register Verification**: I2C read-back comparison ensures configuration integrity  
- **Statistical Validation**: Compare channel statistics between runs for consistency
- **Performance Metrics**: Monitor error rates across different parameter settings
- **Long-term Stability**: Use extended runs to verify system reliability

## Recent Code Improvements (software_v2/)

### Code Quality and Maintainability
- **Eliminated Magic Numbers**: Replaced hardcoded values with meaningful constants (NUM_CHANNELS, MAX_CHANNEL_ID, CHANNEL_STATS_SIZE)
- **Unified String Formatting**: Converted all % formatting to f-strings for consistency and modern Python practices
- **Reduced Code Duplication**: Created helper function `write_error_data()` to eliminate repetitive file writing operations
- **Optimized Data Structures**: Streamlined channel statistics collection with list comprehensions instead of nested loops

### Enhanced Reliability and Bug Fixes  
- **Improved Time Processing**: Fixed cross-month/year time calculations using proper datetime arithmetic
- **Better Boundary Checks**: Enhanced channel ID validation to prevent array index errors
- **Consistent File Operations**: Unified file path formatting across all I/O operations
- **Cleaner Error Handling**: Improved debug output formatting and error message consistency

### Performance Optimizations
- **Reduced Function Calls**: Combined duplicate loops for better execution efficiency  
- **Streamlined File I/O**: Consolidated error data writing to minimize file operations
- **Optimized String Operations**: Eliminated redundant string formatting and concatenations

These improvements maintain full functional compatibility while significantly enhancing code maintainability, readability, and reliability. All statistical calculations and output formats remain identical to preserve data consistency.

This architecture enables comprehensive SEU testing with flexible parameter control and detailed data analysis capabilities.