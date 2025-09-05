# GBCR3 Data Acquisition System v2

Enhanced GBCR3 data acquisition system that maintains identical calculation and statistical methods as the original code, with added command-line parameter support for register configuration without code modification.

## Key Features

- **Full Compatibility**: Maintains identical data processing logic and statistical calculations as original
- **Command-line Parameters**: Configure RX/TX channel parameters directly via command line
- **Debug Mode**: Preserves original debug mode functionality
- **Streamlined Configuration**: Refactored register configuration class, eliminating duplicate code
- **Quick Presets**: Built-in retimed/voted mode switching

## Basic Usage

### Same Interface as Original Version

```bash
# Basic data acquisition (100 files, normal mode)
python main_v2.py 100

# Explicitly specify debug mode
python main_v2.py 100 0   # Normal mode
python main_v2.py 100 1   # Debug mode
```

### New Command-line Configuration Features

```bash
# Configure any RX channel for retimed mode (mux_bias=0xf)
python main_v2.py 100 1 --retimed rx4
python main_v2.py 100 1 --retimed rx6

# Configure RX channel for retimed mode with specific delay
python main_v2.py 100 1 --retimed rx4:0x8
python main_v2.py 100 1 --retimed rx4 --delay 0x8

# Disable specific RX channel
python main_v2.py 100 1 --disable rx4

# Manual RX channel parameter configuration
python main_v2.py 100 1 --rx-config "rx4:mux_bias=0xf,clk_delay=0x8"

# Configure multiple RX channels
python main_v2.py 100 1 \
    --rx-config "rx4:mux_bias=0xf,clk_delay=0x8" \
    --rx-config "rx6:mux_bias=0x17,clk_delay=0x5"

# Configure TX channel (still uses ch format as TX channels are different)
python main_v2.py 100 1 --tx-config "ch1:ampl=0x7,sr1=0x4"

# Configure clock parameters
python main_v2.py 100 1 --clock-config "rx_en=1,tx_delay=0xc"

# Configure MF & HF equalizer amplification parameters
# Set all HF equalizers (HF1, HF2, HF3) to same value, MF to different value
python main_v2.py 100 1 --rx-config "rx4:eq_hf1=0x8,eq_hf2=0x8,eq_hf3=0x8,eq_mf=0x4"
python main_v2.py 100 1 --rx-config "rx6:eq_hf1=0xc,eq_hf2=0xc,eq_hf3=0xc,eq_mf=0x2"
```

## Parameter Reference

### RX Channel Parameters
- `dis_chan`: Channel bias disable (0/1)
- `dis_lpf`: LPF bias disable (0/1)
- `mux_bias`: MUX bias setting (0x0-0x1f)
  - `0xf`: Retimed mode
  - `0x17`: Voted mode (default)
- `eq_hf1/hf2/hf3`: High frequency equalizer settings (0x0-0xf)
- `eq_mf`: Mid frequency equalizer setting (0x0-0xf)  
- `dis_eq_lf`: Low frequency equalizer disable (0/1)
- `cml_ampl`: CML amplitude selection (0x0-0x7)
- `clk_delay`: Clock delay (0x0-0xf)

### TX Channel Parameters
- `sc1/sc2`: Source current control (0x0-0xf)
- `ampl`: Amplitude selection (0x0-0x7)
- `sr1/sr2`: Slew rate control (0x0-0x1f)
- `dis_preemph`: Pre-emphasis disable (0/1)
- `dis_bias`: TX bias disable (0/1)

### Clock Parameters
- `rx_en`: RX clock enable (0/1)
- `tx_delay`: TX clock delay (0x0-0xf)
- `dis_tx`: TX clock disable (0/1)
- `dll_current`: DLL current (0x0-0xf)
- `dll_force_down`: DLL force down (0/1)
- `dll_enable`: DLL enable (0/1)
- `dll_cap_reset`: DLL capacitor reset (0/1)

## Debug Mode

Debug mode (`debug_mode=1`) provides detailed runtime information:

- I2C register read/write verification
- Current monitoring data
- Detailed data processing information
- Detailed error frame output
- Alignment status changes

```bash
# Enable debug mode
python main_v2.py 100 1
```

## Output Files

Program creates timestamped folders in `QAResults_v2/` directory containing:

- `ChAll.TXT`: All channel error data with timestamps
- `Ch{N}.TXT`: Individual channel detailed error data
- `summary.txt`: Run summary with per-channel statistics
- `Filesummary.TXT`: Per-file statistical summary and channel statistics
- `I2C.TXT`: I2C register verification records
- `IDD.TXT`: Current monitoring records

## MF & HF Amplification Parameter Adjustment

The system supports fine-tuning of equalizer amplification parameters for optimal signal conditioning:

### High Frequency (HF) and Mid Frequency (MF) Equalizers

- **eq_hf1, eq_hf2, eq_hf3**: High frequency equalizer settings (0x0-0xf)
- **eq_mf**: Mid frequency equalizer setting (0x0-0xf)

### Usage Examples

```bash
# Example 1: Configure RX4 with HF equalizers at 0x8, MF equalizer at 0x4
python main_v2.py 100 1 --rx-config "rx4:eq_hf1=0x8,eq_hf2=0x8,eq_hf3=0x8,eq_mf=0x4"

# Example 2: Configure RX6 with HF equalizers at 0xc, MF equalizer at 0x2  
python main_v2.py 100 1 --rx-config "rx6:eq_hf1=0xc,eq_hf2=0xc,eq_hf3=0xc,eq_mf=0x2"

# Example 3: Configure multiple channels with different equalizer settings
python main_v2.py 100 1 \
    --rx-config "rx4:eq_hf1=0x8,eq_hf2=0x8,eq_hf3=0x8,eq_mf=0x4" \
    --rx-config "rx5:eq_hf1=0xa,eq_hf2=0xa,eq_hf3=0xa,eq_mf=0x6"
```

### Parameter Scanning for Equalizer Optimization

```bash
#!/bin/bash
# Scan HF/MF equalizer settings for optimal performance
for hf_val in 0x4 0x8 0xc; do
    for mf_val in 0x2 0x4 0x6 0x8; do
        python main_v2.py 50 0 --rx-config "rx4:eq_hf1=$hf_val,eq_hf2=$hf_val,eq_hf3=$hf_val,eq_mf=$mf_val"
    done
done
```

## Hardware Requirements

- FPGA connection at 192.168.2.6:1024
- I2C slave address: 0x23
- Current monitor: LTC2991 (I2C address 0x4F)

## Dependencies

- `GBCR3_Config.py`: Register configuration management
- `command_interpret.py`: FPGA communication interface
- `crc32_8.py`: CRC32 calculations
- `binhex.py`: Data conversion utilities

## Recent Improvements

### Code Quality Enhancements
- **Standardized formatting**: All string formatting unified to f-strings for consistency
- **Eliminated magic numbers**: Introduced constants (NUM_CHANNELS, MAX_CHANNEL_ID) for better maintainability  
- **Reduced code duplication**: Created helper functions to eliminate repetitive file writing operations
- **Improved time processing**: Enhanced cross-month/year time calculations using datetime objects
- **Optimized statistics collection**: Streamlined channel statistics gathering with list comprehensions

### Enhanced Reliability
- **Better error handling**: Improved boundary checks for channel IDs to prevent array index errors
- **Consistent file operations**: Unified file path formatting across all operations
- **Cleaner code structure**: Removed outdated comments and improved function documentation

## Quality Control (QC) Testing

The `GBCR3_QC_Test.sh` script provides a comprehensive automated testing suite for validating system functionality:

```bash
# Run complete QC test suite
./GBCR3_QC_Test.sh
```

### QC Test Components

1. **Environment Setup**: Loads FPGA bitstream and configures software environment
2. **Basic Functionality**: Tests default register configuration 
3. **Channel Disabling Test**: Randomly disables 2 RX channels to verify disable functionality
4. **Retiming Mode Test**: Tests random RX channel in retiming mode with random delay
5. **MF/HF Amplification Scan**: 2D parameter scan (step size 4) for equalizer optimization

All test output is saved to timestamped log files for analysis and debugging.

## Command Line Help

```bash
python main_v2.py --help
```

Shows complete parameter documentation and usage examples.