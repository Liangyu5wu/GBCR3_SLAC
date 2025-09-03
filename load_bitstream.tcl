open_hw
connect_hw_server
open_hw_target

set BITFILE_PATH "firmware/GBCR2_SEU_Test.bit"
#set BITFILE_PATH "firmware/GBCR2_SEU_Test_dataReset.bit"

set current_device [lindex [get_hw_devices] 0]
refresh_hw_device -update_hw_probes false $current_device
set_property PROGRAM.FILE $BITFILE_PATH $current_device

# Program the device and check the result
if {[catch {program_hw_devices $current_device} result]} {
    puts "Programming failed! Error: $result"
} else {
    puts "Programming successful!"
}

close_hw_target
disconnect_hw_server
close_hw
