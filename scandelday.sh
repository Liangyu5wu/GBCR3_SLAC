#!/bin/bash

start=0x0
end=0xf

main_script="main.py"
output_file="summary_delay_output.txt"

> $output_file

start_dec=$((start))
end_dec=$((end))

for ((i=$start_dec; i<=$end_dec; i++))
do
    hex_val=$(printf "0x%x" $i)

    sed -i "203s/.*/iic_write_val = GBCR3_Reg1.configure_rx_channels(iic_write_val, ch=4, MUX_bias=0xf, fdllClkDelay=$hex_val)/" $main_script

    for run in {1..10}
    do
        temp_output=$(python $main_script 2>&1)

        summary=$(echo "$temp_output" | awk '/End Run Summary/,0')

        echo "Running RX4 in retimed mode with delay : $hex_val, Run: $run / 10" >> $output_file
        echo "$summary" >> $output_file
        echo "----------------------------------------" >> $output_file
    done
done

echo "All runs completed. Output saved to $output_file"
