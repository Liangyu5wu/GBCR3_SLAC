#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import copy

class GBCR3_Config(object):
    ## @var _defaultRegMap default register values
    _defaultRegMap = {
        #Using Evan's Default Value for '_Dis_MUX_BIAS'
        #Name: RX_CH6 / regOut00-03
        'Dis_Ch_BIAS_CH6'       :  0,       'Dis_LPF_BIAS_CH6'       :  0,       'CH6_Dis_MUX_BIAS'        :  0x17,
        'CH6_EQ_HF1'            :  0xb,     'CH6_EQ_HF2'             :  0xb,   
        'CH6_EQ_HF3'            :  0xb,     'CH6_EQ_MF'              :  0xb,  
        'Dis_EQ_LF_CH6'         :  0,       'CH6_CML_AmplSel'        :  0x7,     'CH6_CLK_Delay'           :  0x5,
        
        #Name: RX_CH5 / regOut04-07
        'Dis_Ch_BIAS_CH5'       :  0,       'Dis_LPF_BIAS_CH5'       :  0,       'CH5_Dis_MUX_BIAS'        :  0x17,
        'CH5_EQ_HF1'            :  0xb,     'CH5_EQ_HF2'             :  0xb,   
        'CH5_EQ_HF3'            :  0xb,     'CH5_EQ_MF'              :  0xb,  
        'Dis_EQ_LF_CH5'         :  0,       'CH5_CML_AmplSel'        :  0x7,     'CH5_CLK_Delay'           :  0x5,
        
        #Name: RX_CH4 / regOut08-0B
        'Dis_Ch_BIAS_CH4'       :  0,       'Dis_LPF_BIAS_CH4'       :  0,       'CH4_Dis_MUX_BIAS'        :  0x17,
        'CH4_EQ_HF1'            :  0xb,     'CH4_EQ_HF2'             :  0xb,   
        'CH4_EQ_HF3'            :  0xb,     'CH4_EQ_MF'              :  0xb,  
        'Dis_EQ_LF_CH4'         :  0,       'CH4_CML_AmplSel'        :  0x7,     'CH4_CLK_Delay'           :  0x5,
        
        #Name: RX_CH3 / regOut0C-0F
        'Dis_Ch_BIAS_CH3'       :  0,       'Dis_LPF_BIAS_CH3'       :  0,       'CH3_Dis_MUX_BIAS'        :  0x17,
        'CH3_EQ_HF1'            :  0xb,     'CH3_EQ_HF2'             :  0xb,   
        'CH3_EQ_HF3'            :  0xb,     'CH3_EQ_MF'              :  0xb,  
        'Dis_EQ_LF_CH3'         :  0,       'CH3_CML_AmplSel'        :  0x7,     'CH3_CLK_Delay'           :  0x5,
        
        #Name: RX_CH2 / regOut10-13
        'Dis_Ch_BIAS_CH2'       :  0,       'Dis_LPF_BIAS_CH2'       :  0,       'CH2_Dis_MUX_BIAS'        :  0x17,
        'CH2_EQ_HF1'            :  0xb,     'CH2_EQ_HF2'             :  0xb,   
        'CH2_EQ_HF3'            :  0xb,     'CH2_EQ_MF'              :  0xb,  
        'Dis_EQ_LF_CH2'         :  0,       'CH2_CML_AmplSel'        :  0x7,     'CH2_CLK_Delay'           :  0x5,

        #Name: RX_CH1 / regOut14-17
        'Dis_Ch_BIAS_CH1'       :  0,       'Dis_LPF_BIAS_CH1'       :  0,       'CH1_Dis_MUX_BIAS'        :  0x17,
        'CH1_EQ_HF1'            :  0xb,     'CH1_EQ_HF2'             :  0xb,   
        'CH1_EQ_HF3'            :  0xb,     'CH1_EQ_MF'              :  0xb,  
        'Dis_EQ_LF_CH1'         :  0,       'CH1_CML_AmplSel'        :  0x7,     'CH1_CLK_Delay'           :  0x5,
        
        #Using Evan's Default Values
        #Name: TX_CH1 / regOut18-1A
        'Tx_Ch1_SC2'            :  0xf,     'Tx_Ch1_SC1'             :  0xf,
        'Tx_Ch1_AmplSel'        :  0x7,     'Tx_Ch1_SR1'             :  0x4,
        'Tx_Ch1_SR2'            :  0x10,    'Dis_Ch1_PreEmph'        :  0,       'Dis_Ch1_TxBIAS'          :  0,   

        #Name: TX_CH2 / regOut1B-1D
        'Tx_Ch2_SC2'            :  0xf,     'Tx_Ch2_SC1'             :  0xf,
        'Tx_Ch2_AmplSel'        :  0x7,     'Tx_Ch2_SR1'             :  0x4,
        'Tx_Ch2_SR2'            :  0x10,    'Dis_Ch2_PreEmph'        :  0,       'Dis_Ch2_TxBIAS'          :  0,   

        #Name: Phaseshift / regOut1E-1F
        #The next line should be checked later!!!
        'CLK_Rx_en'             :  1,     'CLK_Tx_Delay'             :  0xc,     'Dis_CLK_Tx'              :  1,   
        'Dll_CPCurrent'         :  0x2,   'Dll_ForceDown'            :  1,       'Dll_Enable'              :  1,    'Dll_CapReset'              :  1,   
    }

    _regMap = {}

    def __init__(self):
        self._regMap = copy.deepcopy(self._defaultRegMap)

    ## get I2C register value - same as original configure_all method
    def generate_i2c_values(self):
        reg_value = []
        # RX channels CH6-CH1 (registers 0-23)
        rx_channels = [6, 5, 4, 3, 2, 1]  # Order from original code
        for ch in rx_channels:
            reg_value += [self._regMap[f'Dis_Ch_BIAS_CH{ch}'] << 6 | self._regMap[f'Dis_LPF_BIAS_CH{ch}'] << 5 | self._regMap[f'CH{ch}_Dis_MUX_BIAS']]
            reg_value += [self._regMap[f'CH{ch}_EQ_HF1'] << 4 | self._regMap[f'CH{ch}_EQ_HF2']]
            reg_value += [self._regMap[f'CH{ch}_EQ_HF3'] << 4 | self._regMap[f'CH{ch}_EQ_MF']]
            reg_value += [self._regMap[f'Dis_EQ_LF_CH{ch}'] << 7 | self._regMap[f'CH{ch}_CML_AmplSel'] << 4 | self._regMap[f'CH{ch}_CLK_Delay']]
        
        # TX channels CH1-CH2 (registers 24-29)
        for ch in [1, 2]:
            reg_value += [self._regMap[f'Tx_Ch{ch}_SC2'] << 4 | self._regMap[f'Tx_Ch{ch}_SC1']]
            reg_value += [self._regMap[f'Tx_Ch{ch}_AmplSel'] << 5 | self._regMap[f'Tx_Ch{ch}_SR1']]
            reg_value += [self._regMap[f'Tx_Ch{ch}_SR2'] << 2 | self._regMap[f'Dis_Ch{ch}_PreEmph'] << 1 | self._regMap[f'Dis_Ch{ch}_TxBIAS']]
        
        # Clock/DLL (registers 30-31)
        reg_value += [self._regMap['CLK_Rx_en'] << 5 | self._regMap['CLK_Tx_Delay'] << 1 | self._regMap['Dis_CLK_Tx']]
        reg_value += [self._regMap['Dll_CPCurrent'] << 3 | self._regMap['Dll_ForceDown'] << 2 | self._regMap['Dll_Enable'] << 1 | self._regMap['Dll_CapReset']]
        
        return reg_value

    ## Configure RX channels with original logic but simplified interface
    def configure_rx_channel(self, channel, **kwargs):
        """Configure a single RX channel with parameters"""
        if channel not in range(1, 7):
            raise ValueError(f"Invalid RX channel {channel}. Valid: 1-6")
        
        # Parameter name mapping for simplified interface
        param_mapping = {
            'dis_chan': f'Dis_Ch_BIAS_CH{channel}',
            'dis_lpf': f'Dis_LPF_BIAS_CH{channel}',
            'mux_bias': f'CH{channel}_Dis_MUX_BIAS',
            'eq_hf1': f'CH{channel}_EQ_HF1',
            'eq_hf2': f'CH{channel}_EQ_HF2', 
            'eq_hf3': f'CH{channel}_EQ_HF3',
            'eq_mf': f'CH{channel}_EQ_MF',
            'dis_eq_lf': f'Dis_EQ_LF_CH{channel}',
            'cml_ampl': f'CH{channel}_CML_AmplSel',
            'clk_delay': f'CH{channel}_CLK_Delay',
            # Alternative names for compatibility
            'dllClkDelay': f'CH{channel}_CLK_Delay',
            'MUX_bias': f'CH{channel}_Dis_MUX_BIAS',
            'CML_AmplSel': f'CH{channel}_CML_AmplSel'
        }
        
        for param, value in kwargs.items():
            if param in param_mapping:
                reg_name = param_mapping[param]
                if reg_name in self._regMap:
                    self._regMap[reg_name] = value
                else:
                    raise ValueError(f"Invalid register name: {reg_name}")
            else:
                raise ValueError(f"Invalid RX parameter: {param}")

    ## Configure TX channels 
    def configure_tx_channel(self, channel, **kwargs):
        """Configure a single TX channel with parameters"""
        if channel not in range(1, 3):
            raise ValueError(f"Invalid TX channel {channel}. Valid: 1-2")
            
        param_mapping = {
            'sc1': f'Tx_Ch{channel}_SC1',
            'sc2': f'Tx_Ch{channel}_SC2',
            'ampl': f'Tx_Ch{channel}_AmplSel',
            'sr1': f'Tx_Ch{channel}_SR1',
            'sr2': f'Tx_Ch{channel}_SR2',
            'dis_preemph': f'Dis_Ch{channel}_PreEmph',
            'dis_bias': f'Dis_Ch{channel}_TxBIAS'
        }
        
        for param, value in kwargs.items():
            if param in param_mapping:
                reg_name = param_mapping[param]
                if reg_name in self._regMap:
                    self._regMap[reg_name] = value
                else:
                    raise ValueError(f"Invalid register name: {reg_name}")
            else:
                raise ValueError(f"Invalid TX parameter: {param}")

    ## Configure clock/DLL parameters
    def configure_clock(self, **kwargs):
        """Configure clock/DLL parameters"""
        param_mapping = {
            'rx_en': 'CLK_Rx_en',
            'tx_delay': 'CLK_Tx_Delay', 
            'dis_tx': 'Dis_CLK_Tx',
            'dll_current': 'Dll_CPCurrent',
            'dll_force_down': 'Dll_ForceDown',
            'dll_enable': 'Dll_Enable',
            'dll_cap_reset': 'Dll_CapReset'
        }
        
        for param, value in kwargs.items():
            if param in param_mapping:
                reg_name = param_mapping[param]
                if reg_name in self._regMap:
                    self._regMap[reg_name] = value
                else:
                    raise ValueError(f"Invalid register name: {reg_name}")
            else:
                raise ValueError(f"Invalid clock parameter: {param}")

    ## Batch configure multiple channels - new functionality
    def configure_multiple_rx(self, channel_configs):
        """Configure multiple RX channels at once
        channel_configs: dict like {4: {'mux_bias': 0xf, 'clk_delay': 0x8}, 6: {'mux_bias': 0x17}}
        """
        for channel, params in channel_configs.items():
            self.configure_rx_channel(channel, **params)

    ## Get current configuration for debugging - new functionality
    def get_channel_config(self, channel_type, channel):
        """Get current configuration for a channel"""
        if channel_type == 'rx' and channel in range(1, 7):
            return {
                'dis_chan': self._regMap[f'Dis_Ch_BIAS_CH{channel}'],
                'dis_lpf': self._regMap[f'Dis_LPF_BIAS_CH{channel}'],
                'mux_bias': self._regMap[f'CH{channel}_Dis_MUX_BIAS'],
                'eq_hf1': self._regMap[f'CH{channel}_EQ_HF1'],
                'eq_hf2': self._regMap[f'CH{channel}_EQ_HF2'],
                'eq_hf3': self._regMap[f'CH{channel}_EQ_HF3'],
                'eq_mf': self._regMap[f'CH{channel}_EQ_MF'],
                'dis_eq_lf': self._regMap[f'Dis_EQ_LF_CH{channel}'],
                'cml_ampl': self._regMap[f'CH{channel}_CML_AmplSel'],
                'clk_delay': self._regMap[f'CH{channel}_CLK_Delay']
            }
        elif channel_type == 'tx' and channel in range(1, 3):
            return {
                'sc1': self._regMap[f'Tx_Ch{channel}_SC1'],
                'sc2': self._regMap[f'Tx_Ch{channel}_SC2'],
                'ampl': self._regMap[f'Tx_Ch{channel}_AmplSel'],
                'sr1': self._regMap[f'Tx_Ch{channel}_SR1'],
                'sr2': self._regMap[f'Tx_Ch{channel}_SR2'],
                'dis_preemph': self._regMap[f'Dis_Ch{channel}_PreEmph'],
                'dis_bias': self._regMap[f'Dis_Ch{channel}_TxBIAS']
            }
        else:
            raise ValueError(f"Invalid channel type/number: {channel_type} {channel}")


def parse_channel_config(config_str):
    """Parse channel configuration from string format
    Format: 'rx4:mux_bias=0xf,clk_delay=0x8' or 'ch1:ampl=0x7' (tx channels still use ch)
    """
    if ':' not in config_str:
        raise ValueError("Invalid format. Use 'rx4:param=value,param2=value2' or 'ch1:param=value'")
    
    ch_part, params_part = config_str.split(':', 1)
    
    # Parse channel - support both rx (RX channels) and ch (TX channels or legacy)
    if ch_part.startswith('rx'):
        channel = int(ch_part[2:])
    elif ch_part.startswith('ch'):
        channel = int(ch_part[2:])
    else:
        raise ValueError("Channel must start with 'rx' (e.g., 'rx4') or 'ch' (e.g., 'ch1')")
    
    # Parse parameters
    params = {}
    for param_pair in params_part.split(','):
        if '=' not in param_pair:
            continue
        key, value = param_pair.strip().split('=', 1)
        
        # Convert hex values
        if value.startswith('0x'):
            params[key] = int(value, 16)
        else:
            params[key] = int(value)
    
    return channel, params