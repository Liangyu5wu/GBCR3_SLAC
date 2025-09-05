#!/bin/bash

# GBCR3 Quality Control (QC) Comprehensive Testing Script
# This script performs a full QC testing cycle including:
# - Environment setup
# - Basic functionality check
# - Random channel disabling test
# - Random retiming mode test  
# - Random MF vs HF amplification scanning test

set -e  # Exit on any error

# Log file for all output
LOG_FILE="QC_Test_$(date +%Y%m%d_%H%M%S).log"

log() {
    echo "$1" | tee -a "$LOG_FILE"
}

# Function to generate random number within range
random_in_range() {
    echo $(( RANDOM % ($2 - $1 + 1) + $1 ))
}

# Function to convert number to hex
to_hex() {
    printf "0x%x" $1
}

# Main execution starts here
log "========================================"
log "GBCR3 QC Test Suite Started - $(date)"
log "========================================"

# Save current directory and navigate to project root
ORIGINAL_DIR=$(pwd)
cd "$(dirname "$0")/.."

log ""
log "Phase 1: Environment Setup"
log ">>> Loading FPGA bitstream..."
if ./load_bitstream.sh >> "$LOG_FILE" 2>&1; then
    log "✓ FPGA bitstream loaded successfully"
else
    log "✗ Failed to load FPGA bitstream"
    exit 1
fi

log ">>> Setting up software environment..."
cd GBCR3_SLAC/software
if source setup.sh >> "$LOG_FILE" 2>&1; then
    log "✓ Software environment setup completed"
else
    log "✗ Failed to setup software environment"
    exit 1
fi

cd ../software_v2

log ""
log "Phase 2: Basic Functionality Check"
log ">>> Performing basic functionality test with default register values..."
if python main_v2.py 10 1 >> "$LOG_FILE" 2>&1; then
    log "✓ Basic functionality test completed successfully"
else
    log "✗ Basic functionality test failed"
    exit 1
fi

log ""
log "Phase 3: Random Channel Disabling Test"

# Generate 2 random RX channels to disable (from rx1-rx6)
RX_CHANNELS=(rx1 rx2 rx3 rx4 rx5 rx6)
DISABLE_CHANNELS=()

# Select 2 random channels
for i in {1..2}; do
    while true; do
        RANDOM_INDEX=$(random_in_range 0 5)
        CHANNEL="${RX_CHANNELS[$RANDOM_INDEX]}"
        
        if [[ ! " ${DISABLE_CHANNELS[@]} " =~ " ${CHANNEL} " ]]; then
            DISABLE_CHANNELS+=("$CHANNEL")
            break
        fi
    done
done

log ">>> Randomly selected channels to disable: ${DISABLE_CHANNELS[0]}, ${DISABLE_CHANNELS[1]}"
DISABLE_CMD="python main_v2.py 10 1 --disable ${DISABLE_CHANNELS[0]} --disable ${DISABLE_CHANNELS[1]}"
log ">>> Executing: $DISABLE_CMD"

if $DISABLE_CMD >> "$LOG_FILE" 2>&1; then
    log "✓ Channel disabling functionality test completed successfully"
else
    log "✗ Channel disabling functionality test failed"
    exit 1
fi

log ""
log "Phase 4: Random Retiming Mode Test"

# Select 1 random RX channel for retiming test
RETIMED_CHANNEL_INDEX=$(random_in_range 0 5)
RETIMED_CHANNEL="${RX_CHANNELS[$RETIMED_CHANNEL_INDEX]}"
RANDOM_DELAY=$(random_in_range 0 15)
HEX_DELAY=$(to_hex $RANDOM_DELAY)

log ">>> Randomly selected channel for retiming mode: $RETIMED_CHANNEL with delay $HEX_DELAY"
RETIMED_CMD="python main_v2.py 10 1 --retimed ${RETIMED_CHANNEL}:${HEX_DELAY}"
log ">>> Executing: $RETIMED_CMD"

if $RETIMED_CMD >> "$LOG_FILE" 2>&1; then
    log "✓ Retiming mode test completed successfully"
else
    log "✗ Retiming mode test failed"
    exit 1
fi

log ""
log "Phase 5: MF vs HF Amplification Scanning Test"

# Select 1 random RX channel for amplification scanning
AMPL_CHANNEL_INDEX=$(random_in_range 0 5)
AMPL_CHANNEL="${RX_CHANNELS[$AMPL_CHANNEL_INDEX]}"

log ">>> Randomly selected channel for MF/HF amplification scanning: $AMPL_CHANNEL"
log ">>> Performing 2D scan with step size of 4 (HF: 0x0,0x4,0x8,0xc; MF: 0x0,0x4,0x8,0xc)"

# Scan with step size of 4: 0x0, 0x4, 0x8, 0xc
HF_VALUES=(0 4 8 12)
MF_VALUES=(0 4 8 12)

SCAN_COUNT=0
for hf_val in "${HF_VALUES[@]}"; do
    for mf_val in "${MF_VALUES[@]}"; do
        HEX_HF=$(to_hex $hf_val)
        HEX_MF=$(to_hex $mf_val)
        
        SCAN_COUNT=$((SCAN_COUNT + 1))
        log ">>> Scan $SCAN_COUNT/16: HF=$HEX_HF, MF=$HEX_MF on channel $AMPL_CHANNEL"
        
        AMPL_CMD="python main_v2.py 5 0 --rx-config \"${AMPL_CHANNEL}:eq_hf1=${HEX_HF},eq_hf2=${HEX_HF},eq_hf3=${HEX_HF},eq_mf=${HEX_MF}\""
        
        if eval $AMPL_CMD >> "$LOG_FILE" 2>&1; then
            log "    ✓ Scan point completed successfully"
        else
            log "    ✗ Amplification scan failed at HF=$HEX_HF, MF=$HEX_MF"
            exit 1
        fi
    done
done

log "✓ MF vs HF amplification scanning test completed successfully"

log ""
log "========================================"
log "QC Test Suite Completed Successfully"
log "========================================"
log "✓ All QC tests passed!"
log "✓ Test completed: $(date)"
log "✓ Complete test log saved to: $LOG_FILE"

# Return to original directory
cd "$ORIGINAL_DIR"

log ""
log "Test Summary:"
log "✓ Environment Setup: PASSED"
log "✓ Basic Functionality Check: PASSED"
log "✓ Channel Disabling Test: PASSED (disabled: ${DISABLE_CHANNELS[0]}, ${DISABLE_CHANNELS[1]})"
log "✓ Retiming Mode Test: PASSED (channel: $RETIMED_CHANNEL, delay: $HEX_DELAY)"  
log "✓ MF/HF Amplification Scan: PASSED (channel: $AMPL_CHANNEL, 16 scan points)"
log ""
log "GBCR3 QC Test Suite: ALL TESTS PASSED!"