#!/bin/bash

# GBCR3 Quality Control (QC) Comprehensive Testing Script
# This script performs a full QC testing cycle including:
# - Environment setup
# - Basic functionality check
# - Random channel disabling test
# - Random retiming mode test  
# - Random MF vs HF amplification scanning test

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Log file for all output
LOG_FILE="QC_Test_$(date +%Y%m%d_%H%M%S).log"

log() {
    echo -e "$1" | tee -a "$LOG_FILE"
}

log_section() {
    log "\n${BLUE}========================================${NC}"
    log "${BLUE}$1${NC}"
    log "${BLUE}========================================${NC}"
}

log_step() {
    log "${YELLOW}>>> $1${NC}"
}

log_success() {
    log "${GREEN}✓ $1${NC}"
}

log_error() {
    log "${RED}✗ $1${NC}"
}

# Function to generate random number within range
random_in_range() {
    local min=$1
    local max=$2
    echo $(( RANDOM % (max - min + 1) + min ))
}

# Function to convert number to hex
to_hex() {
    printf "0x%x" $1
}

# Main execution starts here
log_section "GBCR3 QC Test Suite Started - $(date)"

# Save current directory
ORIGINAL_DIR=$(pwd)
SCRIPT_DIR=$(dirname "$0")
cd "$SCRIPT_DIR/.."

log_section "Phase 1: Environment Setup"

log_step "Loading FPGA bitstream..."
if ./load_bitstream.sh >> "$LOG_FILE" 2>&1; then
    log_success "FPGA bitstream loaded successfully"
else
    log_error "Failed to load FPGA bitstream"
    exit 1
fi

log_step "Setting up software environment..."
cd GBCR3_SLAC/software
if source setup.sh >> "$LOG_FILE" 2>&1; then
    log_success "Software environment setup completed"
else
    log_error "Failed to setup software environment"
    exit 1
fi

# Return to software_v2 directory
cd ../software_v2

log_section "Phase 2: Basic Functionality Check"

log_step "Performing basic functionality test with default register values..."
if python main_v2.py 10 1 >> "$LOG_FILE" 2>&1; then
    log_success "Basic functionality test completed successfully"
else
    log_error "Basic functionality test failed"
    exit 1
fi

log_section "Phase 3: Random Channel Disabling Test"

# Generate 2 random RX channels to disable (from rx1-rx6)
RX_CHANNELS=(rx1 rx2 rx3 rx4 rx5 rx6)
DISABLE_CHANNELS=()

# Select 2 random channels
for i in {1..2}; do
    while true; do
        RANDOM_INDEX=$(random_in_range 0 5)
        CHANNEL="${RX_CHANNELS[$RANDOM_INDEX]}"
        
        # Check if channel not already selected
        if [[ ! " ${DISABLE_CHANNELS[@]} " =~ " ${CHANNEL} " ]]; then
            DISABLE_CHANNELS+=("$CHANNEL")
            break
        fi
    done
done

log_step "Randomly selected channels to disable: ${DISABLE_CHANNELS[0]}, ${DISABLE_CHANNELS[1]}"

# Run test with disabled channels
DISABLE_CMD="python main_v2.py 10 1 --disable ${DISABLE_CHANNELS[0]} --disable ${DISABLE_CHANNELS[1]}"
log_step "Executing: $DISABLE_CMD"

if $DISABLE_CMD >> "$LOG_FILE" 2>&1; then
    log_success "Channel disabling functionality test completed successfully"
else
    log_error "Channel disabling functionality test failed"
    exit 1
fi

log_section "Phase 4: Random Retiming Mode Test"

# Select 1 random RX channel for retiming test
RETIMED_CHANNEL_INDEX=$(random_in_range 0 5)
RETIMED_CHANNEL="${RX_CHANNELS[$RETIMED_CHANNEL_INDEX]}"

# Generate random delay value (0x0-0xf)
RANDOM_DELAY=$(random_in_range 0 15)
HEX_DELAY=$(to_hex $RANDOM_DELAY)

log_step "Randomly selected channel for retiming mode: $RETIMED_CHANNEL with delay $HEX_DELAY"

# Run retiming mode test
RETIMED_CMD="python main_v2.py 10 1 --retimed ${RETIMED_CHANNEL}:${HEX_DELAY}"
log_step "Executing: $RETIMED_CMD"

if $RETIMED_CMD >> "$LOG_FILE" 2>&1; then
    log_success "Retiming mode test completed successfully"
else
    log_error "Retiming mode test failed"
    exit 1
fi

log_section "Phase 5: MF vs HF Amplification Scanning Test"

# Select 1 random RX channel for amplification scanning
AMPL_CHANNEL_INDEX=$(random_in_range 0 5)
AMPL_CHANNEL="${RX_CHANNELS[$AMPL_CHANNEL_INDEX]}"

log_step "Randomly selected channel for MF/HF amplification scanning: $AMPL_CHANNEL"
log_step "Performing 2D scan with step size of 4 (HF: 0x0,0x4,0x8,0xc; MF: 0x0,0x4,0x8,0xc)"

# Scan with step size of 4: 0x0, 0x4, 0x8, 0xc
HF_VALUES=(0 4 8 12)
MF_VALUES=(0 4 8 12)

SCAN_COUNT=0
for hf_val in "${HF_VALUES[@]}"; do
    for mf_val in "${MF_VALUES[@]}"; do
        HEX_HF=$(to_hex $hf_val)
        HEX_MF=$(to_hex $mf_val)
        
        SCAN_COUNT=$((SCAN_COUNT + 1))
        log_step "Scan $SCAN_COUNT/16: HF=$HEX_HF, MF=$HEX_MF on channel $AMPL_CHANNEL"
        
        AMPL_CMD="python main_v2.py 5 0 --rx-config \"${AMPL_CHANNEL}:eq_hf1=${HEX_HF},eq_hf2=${HEX_HF},eq_hf3=${HEX_HF},eq_mf=${HEX_MF}\""
        log_step "Executing: $AMPL_CMD"
        
        if eval $AMPL_CMD >> "$LOG_FILE" 2>&1; then
            log "  ✓ Scan point completed successfully"
        else
            log_error "Amplification scan failed at HF=$HEX_HF, MF=$HEX_MF"
            exit 1
        fi
    done
done

log_success "MF vs HF amplification scanning test completed successfully"

log_section "QC Test Suite Completed Successfully"

log_success "All QC tests passed!"
log "Total test duration: $(date)"
log "Complete test log saved to: $LOG_FILE"

# Return to original directory
cd "$ORIGINAL_DIR"

log_section "Test Summary"
log "✓ Environment Setup: PASSED"
log "✓ Basic Functionality Check: PASSED"
log "✓ Channel Disabling Test: PASSED (disabled: ${DISABLE_CHANNELS[0]}, ${DISABLE_CHANNELS[1]})"
log "✓ Retiming Mode Test: PASSED (channel: $RETIMED_CHANNEL, delay: $HEX_DELAY)"  
log "✓ MF/HF Amplification Scan: PASSED (channel: $AMPL_CHANNEL, 16 scan points)"

log "\n${GREEN}🎉 GBCR3 QC Test Suite: ALL TESTS PASSED! 🎉${NC}"