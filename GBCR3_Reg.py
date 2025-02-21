#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy

class GBCR3_Reg(object):
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
        'Tx_Ch1_AmplSel'        :  0xe,     'Tx_Ch1_SR1'             :  0x4,
        'Tx_Ch1_SR2'            :  0xb,     'Dis_Ch1_PreEmph'        :  0,       'Dis_Ch1_TxBIAS'          :  0,   

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

    # ----------------------- Set methods -----------------------

    #Name: RX_CH6 / regOut00-03
    def set_Dis_Ch_BIAS_CH6(self, val):           self._regMap['Dis_Ch_BIAS_CH6'] = val & 0x1
    def set_Dis_LPF_BIAS_CH6(self, val):          self._regMap['Dis_LPF_BIAS_CH6'] = val & 0x1
    def set_CH6_Dis_MUX_BIAS(self, val):          self._regMap['CH6_Dis_MUX_BIAS'] = val & 0x1f
    def set_CH6_EQ_HF1(self, val):                self._regMap['CH6_EQ_HF1'] = val & 0xf
    def set_CH6_EQ_HF2(self, val):                self._regMap['CH6_EQ_HF2'] = val & 0xf
    def set_CH6_EQ_HF3(self, val):                self._regMap['CH6_EQ_HF3'] = val & 0xf
    def set_CH6_EQ_MF(self, val):                 self._regMap['CH6_EQ_MF'] = val & 0xf
    def set_Dis_EQ_LF_CH6(self, val):             self._regMap['Dis_EQ_LF_CH6'] = val & 0x1
    def set_CH6_CML_AmplSel(self, val):           self._regMap['CH6_CML_AmplSel'] = val & 0x7
    def set_CH6_CLK_Delay(self, val):             self._regMap['CH6_CLK_Delay'] = val & 0xf

    #Name: RX_CH5 / regOut04-07
    def set_Dis_Ch_BIAS_CH5(self, val):           self._regMap['Dis_Ch_BIAS_CH5'] = val & 0x1
    def set_Dis_LPF_BIAS_CH5(self, val):          self._regMap['Dis_LPF_BIAS_CH5'] = val & 0x1
    def set_CH5_Dis_MUX_BIAS(self, val):          self._regMap['CH5_Dis_MUX_BIAS'] = val & 0x1f
    def set_CH5_EQ_HF1(self, val):                self._regMap['CH5_EQ_HF1'] = val & 0xf
    def set_CH5_EQ_HF2(self, val):                self._regMap['CH5_EQ_HF2'] = val & 0xf
    def set_CH5_EQ_HF3(self, val):                self._regMap['CH5_EQ_HF3'] = val & 0xf
    def set_CH5_EQ_MF(self, val):                 self._regMap['CH5_EQ_MF'] = val & 0xf
    def set_Dis_EQ_LF_CH5(self, val):             self._regMap['Dis_EQ_LF_CH5'] = val & 0x1
    def set_CH5_CML_AmplSel(self, val):           self._regMap['CH5_CML_AmplSel'] = val & 0x7
    def set_CH5_CLK_Delay(self, val):             self._regMap['CH5_CLK_Delay'] = val & 0xf

    #Name: RX_CH4 / regOut08-0B
    def set_Dis_Ch_BIAS_CH4(self, val):           self._regMap['Dis_Ch_BIAS_CH4'] = val & 0x1
    def set_Dis_LPF_BIAS_CH4(self, val):          self._regMap['Dis_LPF_BIAS_CH4'] = val & 0x1
    def set_CH4_Dis_MUX_BIAS(self, val):          self._regMap['CH4_Dis_MUX_BIAS'] = val & 0x1f
    def set_CH4_EQ_HF1(self, val):                self._regMap['CH4_EQ_HF1'] = val & 0xf
    def set_CH4_EQ_HF2(self, val):                self._regMap['CH4_EQ_HF2'] = val & 0xf
    def set_CH4_EQ_HF3(self, val):                self._regMap['CH4_EQ_HF3'] = val & 0xf
    def set_CH4_EQ_MF(self, val):                 self._regMap['CH4_EQ_MF'] = val & 0xf
    def set_Dis_EQ_LF_CH4(self, val):             self._regMap['Dis_EQ_LF_CH4'] = val & 0x1
    def set_CH4_CML_AmplSel(self, val):           self._regMap['CH4_CML_AmplSel'] = val & 0x7
    def set_CH4_CLK_Delay(self, val):             self._regMap['CH4_CLK_Delay'] = val & 0xf
    
    #Name: RX_CH3 / regOut0C-0F
    def set_Dis_Ch_BIAS_CH3(self, val):           self._regMap['Dis_Ch_BIAS_CH3'] = val & 0x1
    def set_Dis_LPF_BIAS_CH3(self, val):          self._regMap['Dis_LPF_BIAS_CH3'] = val & 0x1
    def set_CH3_Dis_MUX_BIAS(self, val):          self._regMap['CH3_Dis_MUX_BIAS'] = val & 0x1f
    def set_CH3_EQ_HF1(self, val):                self._regMap['CH3_EQ_HF1'] = val & 0xf
    def set_CH3_EQ_HF2(self, val):                self._regMap['CH3_EQ_HF2'] = val & 0xf
    def set_CH3_EQ_HF3(self, val):                self._regMap['CH3_EQ_HF3'] = val & 0xf
    def set_CH3_EQ_MF(self, val):                 self._regMap['CH3_EQ_MF'] = val & 0xf
    def set_Dis_EQ_LF_CH3(self, val):             self._regMap['Dis_EQ_LF_CH3'] = val & 0x1
    def set_CH3_CML_AmplSel(self, val):           self._regMap['CH3_CML_AmplSel'] = val & 0x7
    def set_CH3_CLK_Delay(self, val):             self._regMap['CH3_CLK_Delay'] = val & 0xf
        
    #Name: RX_CH2 / regOut10-13
    def set_Dis_Ch_BIAS_CH2(self, val):           self._regMap['Dis_Ch_BIAS_CH2'] = val & 0x1
    def set_Dis_LPF_BIAS_CH2(self, val):          self._regMap['Dis_LPF_BIAS_CH2'] = val & 0x1
    def set_CH2_Dis_MUX_BIAS(self, val):          self._regMap['CH2_Dis_MUX_BIAS'] = val & 0x1f
    def set_CH2_EQ_HF1(self, val):                self._regMap['CH2_EQ_HF1'] = val & 0xf
    def set_CH2_EQ_HF2(self, val):                self._regMap['CH2_EQ_HF2'] = val & 0xf
    def set_CH2_EQ_HF3(self, val):                self._regMap['CH2_EQ_HF3'] = val & 0xf
    def set_CH2_EQ_MF(self, val):                 self._regMap['CH2_EQ_MF'] = val & 0xf
    def set_Dis_EQ_LF_CH2(self, val):             self._regMap['Dis_EQ_LF_CH2'] = val & 0x1
    def set_CH2_CML_AmplSel(self, val):           self._regMap['CH2_CML_AmplSel'] = val & 0x7
    def set_CH2_CLK_Delay(self, val):             self._regMap['CH2_CLK_Delay'] = val & 0xf
        
    #Name: RX_CH1 / regOut14-17
    def set_Dis_Ch_BIAS_CH1(self, val):           self._regMap['Dis_Ch_BIAS_CH1'] = val & 0x1
    def set_Dis_LPF_BIAS_CH1(self, val):          self._regMap['Dis_LPF_BIAS_CH1'] = val & 0x1
    def set_CH1_Dis_MUX_BIAS(self, val):          self._regMap['CH1_Dis_MUX_BIAS'] = val & 0x1f
    def set_CH1_EQ_HF1(self, val):                self._regMap['CH1_EQ_HF1'] = val & 0xf
    def set_CH1_EQ_HF2(self, val):                self._regMap['CH1_EQ_HF2'] = val & 0xf
    def set_CH1_EQ_HF3(self, val):                self._regMap['CH1_EQ_HF3'] = val & 0xf
    def set_CH1_EQ_MF(self, val):                 self._regMap['CH1_EQ_MF'] = val & 0xf
    def set_Dis_EQ_LF_CH1(self, val):             self._regMap['Dis_EQ_LF_CH1'] = val & 0x1
    def set_CH1_CML_AmplSel(self, val):           self._regMap['CH1_CML_AmplSel'] = val & 0x7
    def set_CH1_CLK_Delay(self, val):             self._regMap['CH1_CLK_Delay'] = val & 0xf

    #Name: TX_CH1 / regOut18-1A 
    def set_Tx_Ch1_SC2(self, val):                self._regMap['Tx_Ch1_SC2'] = val & 0xf
    def set_Tx_Ch1_SC1(self, val):                self._regMap['Tx_Ch1_SC1'] = val & 0xf
    def set_Tx_Ch1_AmplSel(self, val):            self._regMap['Tx_Ch1_AmplSel'] = val & 0x7
    def set_Tx_Ch1_SR1(self, val):                self._regMap['Tx_Ch1_SR1'] = val & 0x1f
    def set_Tx_Ch1_SR2(self, val):                self._regMap['Tx_Ch1_SR2'] = val & 0x1f
    def set_Dis_Ch1_PreEmph(self, val):           self._regMap['Dis_Ch1_PreEmph'] = val & 0x1
    def set_Dis_Ch1_TxBIAS(self, val):            self._regMap['Dis_Ch1_TxBIAS'] = val & 0x1

    #Name: TX_CH2 / regOut1B-1D
    def set_Tx_Ch2_SC2(self, val):                self._regMap['Tx_Ch2_SC2'] = val & 0xf
    def set_Tx_Ch2_SC1(self, val):                self._regMap['Tx_Ch2_SC1'] = val & 0xf
    def set_Tx_Ch2_AmplSel(self, val):            self._regMap['Tx_Ch2_AmplSel'] = val & 0x7
    def set_Tx_Ch2_SR1(self, val):                self._regMap['Tx_Ch2_SR1'] = val & 0x1f
    def set_Tx_Ch2_SR2(self, val):                self._regMap['Tx_Ch2_SR2'] = val & 0x1f
    def set_Dis_Ch2_PreEmph(self, val):           self._regMap['Dis_Ch2_PreEmph'] = val & 0x1
    def set_Dis_Ch2_TxBIAS(self, val):            self._regMap['Dis_Ch2_TxBIAS'] = val & 0x1

    #Name: Phaseshift / regOut1E-1F
    #The next line should be checked later!!!
    def set_CLK_Rx_en(self, val):                 self._regMap['CLK_Rx_en'] = val & 0x1
    def set_CLK_Tx_Delay(self, val):              self._regMap['CLK_Tx_Delay'] = val & 0xf
    def set_Dis_CLK_Tx(self, val):                self._regMap['Dis_CLK_Tx'] = val & 0x1
    def set_Dll_CPCurrent(self, val):             self._regMap['Dll_CPCurrent'] = val & 0xf
    def set_Dll_ForceDown(self, val):             self._regMap['Dll_ForceDown'] = val & 0x1
    def set_Dll_Enable(self, val):                self._regMap['Dll_Enable'] = val & 0x1
    def set_Dll_CapReset(self, val):              self._regMap['Dll_CapReset'] = val & 0x1
        

    ## get I2C register value
    def get_config_vector(self):
        reg_value = []
        reg_value += [self._regMap['CH1_Dis_EQ_LF'] << 5 | self._regMap['CH1_EQ_ATT'] << 3 | self._regMap['CH1_CML_AmplSel']]
        reg_value += [self._regMap['CH1_CTLE_HFSR'] << 4 | self._regMap['CH1_CTLE_MFSR']]
        reg_value += [self._regMap['CH1_Disable'] << 2 | self._regMap['CH1_Dis_DFF'] << 1 | self._regMap['CH1_Dis_LPF']]
        reg_value += [self._regMap['CH2_Dis_EQ_LF'] << 5 | self._regMap['CH2_EQ_ATT'] << 3 | self._regMap['CH2_CML_AmplSel']]
        reg_value += [self._regMap['CH2_CTLE_HFSR'] << 4 | self._regMap['CH2_CTLE_MFSR']]
        reg_value += [self._regMap['CH2_Disable'] << 2 | self._regMap['CH2_Dis_DFF'] << 1 | self._regMap['CH2_Dis_LPF']]
        reg_value += [self._regMap['CH3_Dis_EQ_LF'] << 5 | self._regMap['CH3_EQ_ATT'] << 3 | self._regMap['CH3_CML_AmplSel']]
        reg_value += [self._regMap['CH3_CTLE_HFSR'] << 4 | self._regMap['CH3_CTLE_MFSR']]
        reg_value += [self._regMap['CH3_Disable'] << 2 | self._regMap['CH3_Dis_DFF'] << 1 | self._regMap['CH3_Dis_LPF']]
        reg_value += [self._regMap['CH4_Dis_EQ_LF'] << 5 | self._regMap['CH4_EQ_ATT'] << 3 | self._regMap['CH4_CML_AmplSel']]
        reg_value += [self._regMap['CH4_CTLE_HFSR'] << 4 | self._regMap['CH4_CTLE_MFSR']]
        reg_value += [self._regMap['CH4_Disable'] << 2 | self._regMap['CH4_Dis_DFF'] << 1 | self._regMap['CH4_Dis_LPF']]
        reg_value += [self._regMap['CH5_Dis_EQ_LF'] << 5 | self._regMap['CH5_EQ_ATT'] << 3 | self._regMap['CH5_CML_AmplSel']]
        reg_value += [self._regMap['CH5_CTLE_HFSR'] << 4 | self._regMap['CH5_CTLE_MFSR']]
        reg_value += [self._regMap['CH5_Disable'] << 2 | self._regMap['CH5_Dis_DFF'] << 1 | self._regMap['CH5_Dis_LPF']]
        reg_value += [self._regMap['CH6_Dis_EQ_LF'] << 5 | self._regMap['CH6_EQ_ATT'] << 3 | self._regMap['CH6_CML_AmplSel']]
        reg_value += [self._regMap['CH6_CTLE_HFSR'] << 4 | self._regMap['CH6_CTLE_MFSR']]
        reg_value += [self._regMap['CH6_Disable'] << 2 | self._regMap['CH6_Dis_DFF'] << 1 | self._regMap['CH6_Dis_LPF']]
        reg_value += [self._regMap['CH7_Dis_EQ_LF'] << 5 | self._regMap['CH7_EQ_ATT'] << 3 | self._regMap['CH7_CML_AmplSel']]
        reg_value += [self._regMap['CH7_CTLE_HFSR'] << 4 | self._regMap['CH7_CTLE_MFSR']]
        reg_value += [self._regMap['CH7_Disable'] << 2 | self._regMap['CH7_Dis_DFF'] << 1 | self._regMap['CH7_Dis_LPF']]
        reg_value += [self._regMap['dllEnable'] << 1 | self._regMap['dllCapReset']]
        reg_value += [self._regMap['dllForceDown'] << 4 | self._regMap['dllChargePumpCurrent']]
        reg_value += [self._regMap['dllClockDelay_CH7'] << 4 | self._regMap['dllClockDelay_CH6']]
        reg_value += [self._regMap['dllClockDelay_CH5'] << 4 | self._regMap['dllClockDelay_CH4']]
        reg_value += [self._regMap['dllClockDelay_CH3'] << 4 | self._regMap['dllClockDelay_CH2']]
        reg_value += [self._regMap['dllClockDelay_CH1'] << 4 | self._regMap['dllClockDelay_CH0']]
        reg_value += [self._regMap['Rx_Enable'] << 6 | self._regMap['Rx_setCM'] << 5 | self._regMap['Rx_enTermination'] << 4 \
                      | self._regMap['Rx_invData'] << 3 | self._regMap['Rx_Equa'] << 1 | self._regMap['Dis_Tx']]
        reg_value += [self._regMap['Tx1_DL_ATT'] << 4 | self._regMap['Tx1_Dis_DL_Emp'] << 3 | self._regMap['Tx1_DL_SR']]
        reg_value += [self._regMap['Tx1_Dis_DL_BIAS'] << 1 | self._regMap['Tx1_Dis_DL_LPF_BIAS']]
        reg_value += [self._regMap['Tx2_DL_ATT'] << 4 | self._regMap['Tx2_Dis_DL_Emp'] << 3 | self._regMap['Tx2_DL_SR']]
        reg_value += [self._regMap['Tx2_Dis_DL_BIAS'] << 1 | self._regMap['Tx2_Dis_DL_LPF_BIAS']]
        return reg_value
    

    def configure_rx_channels(self, iic_write_val):
        dis_chan = 0
        disLPF = 0
        MUX_bias = 0x17
        CTLE_MFSR = 0x8
        CTLE_HFSR = 0x8
        dis_EQ_LF = 0
        CML_AmplSel = 0x7
        dllClkDelay = 0x5

        for i in range(6):
            iic_write_val[4 * i] = (dis_chan << 6) | (disLPF << 5) | MUX_bias
            iic_write_val[4 * i + 1] = (CTLE_HFSR << 4) | CTLE_HFSR
            iic_write_val[4 * i + 2] = (CTLE_HFSR << 4) | CTLE_MFSR
            iic_write_val[4 * i + 3] = (dis_EQ_LF << 7) | (CML_AmplSel << 4) | dllClkDelay
        return iic_write_val

    def configure_tx(self, iic_write_val):
        txSC1 = 0xF
        txSC2 = 0xF
        txSR1 = 0x4
        txSR2 = 0x10
        txAmp = 0x7
        disPreEmp = 0
        disTXbias = 0
        for i in range(2):
            iic_write_val[3 * i + 24] = (txSC2 << 4) | txSC1
            iic_write_val[3 * i + 25] = (txAmp << 5) | txSR1
            iic_write_val[3 * i + 26] = (txSR2 << 2) | (disPreEmp << 1) | disTXbias
        return iic_write_val

    def configure_external_clock(self, iic_write_val):
        clk_Rx_En = 1
        dis_clk_Tx = 1
        clk_Tx_Delay = 0
        iic_write_val[30] = (clk_Rx_En << 5) | (clk_Tx_Delay << 1) | dis_clk_Tx
        return iic_write_val

    def configure_dll(self, iic_write_val):
        dllCapReset = 0
        dllEnable = 1
        dllForceDown = 0
        dllChargePumpCurrent = 0x8
        iic_write_val[31] = (dllChargePumpCurrent << 3) | (dllForceDown << 2) | (dllEnable << 1) | dllCapReset
        return iic_write_val

    def configure_all(self, iic_write_val):
        iic_write_val = self.configure_rx_channels(iic_write_val)
        iic_write_val = self.configure_tx(iic_write_val)
        iic_write_val = self.configure_external_clock(iic_write_val)
        iic_write_val = self.configure_dll(iic_write_val)
        return iic_write_val
