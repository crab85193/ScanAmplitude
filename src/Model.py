class Model(object):
    def __init__(self):
        self.__ai_plot_title = 'Analog Input'
        self.__ao_plot_title = 'Analog Output'
        self.__do1_checkbox_label = 'DO1'
        self.__do2_checkbox_label = 'DO2'
        self.__do_manual_title = 'Digital output manual Controller'
        self.__scan_button_default_label = 'SCAN'
        self.__scan_button_update_label = 'STOP'
        self.__conditioning_label = 'Conditioning'
        self.__ai_channel_label = 'AI Channel'
        self.__ao_channel_label = 'AO Channel'
        self.__do1_port_and_line_label = 'DO1 Port & Line'
        self.__do2_port_and_line_label = 'DO2 Port & Line'
        self.__threshold_label = 'Threshold Voltage'
        self.__vmax_label = 'Max Voltage'
        self.__vmin_label = 'Min Voltage'
        self.__vinc_label = 'Incremental Voltage'
        self.__threshold_default_value = '10.0'
        self.__vmax_default_value = '5.0'
        self.__vmin_default_value = '-5.0'
        self.__vinc_default_value = '0.01'
        self.__do_conditioning_label = 'DO when conditioning'
        self.__init_button_default_label = 'Initialize'
        self.__line = '----------------------------------------'
        self.__ai_channels = ['ai0','ai1','ai2','ai3','ai4','ai5','ai6','ai7']
        self.__ao_channels = ['ao0',"ao1"]
        self.__do_ports = ['port0','port1','port2']
        self.__do_lines = ['line0','line1','line2','line3','line4','line5','line6','line7']
        self.__do_conditioning_items = ['DO1','DO2','Both']
        self.__ai_channels_default_index = 0
        self.__ao_channels_default_index = 0
        self.__do1_ports_default_index = 1
        self.__do1_lines_default_index = 0
        self.__do2_ports_default_index = 1
        self.__do2_lines_default_index = 1
        
    def getAIPlotTitle(self) -> str:
        return self.__ai_plot_title
    
    def getAOPlotTitle(self) -> str:
        return self.__ao_plot_title
    
    def getDO1CheckboxLabel(self) -> str:
        return self.__do1_checkbox_label
    
    def getDO2CheckboxLabel(self) -> str:
        return self.__do2_checkbox_label
    
    def getDOManualTitle(self) -> str:
        return self.__do_manual_title
    
    def getScanButtonLabel(self, update: bool) -> str:
        if update:
            return self.__scan_button_update_label
        else:
            return self.__scan_button_default_label
        
    def getConditioningLabel(self) -> str:
        return self.__conditioning_label
    
    def getAIChannelLabel(self) -> str:
        return self.__ai_channel_label
    
    def getAOChannelLabel(self) -> str:
        return self.__ao_channel_label
    
    def getDO1PortAndLineLabel(self) -> str:
        return self.__do1_port_and_line_label
    
    def getDO2PortAndLineLabel(self) -> str:
        return self.__do2_port_and_line_label
    
    def getThresholdLabel(self) -> str:
        return self.__threshold_label
    
    def getVmaxLabel(self) -> str:
        return self.__vmax_label
    
    def getVminLabel(self) -> str:
        return self.__vmin_label
    
    def getVincLabel(self) -> str:
        return self.__vinc_label
    
    def getThresholdDefaultValue(self) -> str:
        return self.__threshold_default_value
    
    def getVmaxDefaultValue(self) -> str:
        return self.__vmax_default_value
    
    def getVminDefaultValue(self) -> str:
        return self.__vmin_default_value
    
    def getVincDefaultValue(self) -> str:
        return self.__vinc_default_value
    
    def getDOConditioningLabel(self) -> str:
        return self.__do_conditioning_label
    
    def getInitButtonLabel(self) -> str:
        return self.__init_button_default_label
    
    def getLine(self) -> str:
        return self.__line
    
    def getAIChannels(self) -> list:
        return self.__ai_channels
    
    def getAOChannels(self) -> list:
        return self.__ao_channels
    
    def getDOPorts(self) -> list:
        return self.__do_ports
    
    def getDOLines(self) -> list:
        return self.__do_lines
    
    def getDOConditioningItems(self) -> list:
        return self.__do_conditioning_items
    
    def getAIChannelsDefaultIndex(self) -> int:
        return self.__ai_channels_default_index
    
    def getAOChannelsDefaultIndex(self) -> int:
        return self.__ao_channels_default_index
    
    def getDO1PortsDefaultIndex(self) -> int:
        return self.__do1_ports_default_index
    
    def getDO1LinesDefaultIndex(self) -> int:
        return self.__do1_lines_default_index
    
    def getDO2PortsDefaultIndex(self) -> int:
        return self.__do2_ports_default_index
    
    def getDO2LinesDefaultIndex(self) -> int:
        return self.__do2_lines_default_index