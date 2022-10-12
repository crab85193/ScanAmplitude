import nidaqmx
from nidaqmx.constants import LineGrouping

class NIDAQ_task(object):
    def __init__(self):
        """
        Constructor.

        Create a task
        """
        try:
            self.dev_name = self.getDeviceNames()[0]
            self.task = nidaqmx.Task()
        except (nidaqmx._lib.DaqNotFoundError,AttributeError):
            pass

    def start(self):
        try:
            self.task.start()
        except (nidaqmx._lib.DaqNotFoundError,AttributeError):
            pass

    def stop(self):
        try:
            self.task.stop()
        except (nidaqmx._lib.DaqNotFoundError,AttributeError):
            pass

    def close(self):
        try:
            self.task.close()
        except (nidaqmx._lib.DaqNotFoundError,AttributeError):
            pass

    def getDeviceNames(self) -> list:
        try:
            sys = nidaqmx.system.System()
            return sys.devices.device_names
        except (nidaqmx._lib.DaqNotFoundError,AttributeError):
            return ['None']


class NIDAQ_ai_task(NIDAQ_task):
    def __init__(self, port : str):
        """
        Constructor.

        Create an AI task
        """
        try:
            super().__init__()
            self.task.ai_channels.add_ai_voltage_chan(self.dev_name + "/" + port)
        except (nidaqmx._lib.DaqNotFoundError,AttributeError):
            pass

    def getAIData_single(self) -> list:
        """
        Obtain an analog input value.

        Returns:
            list: Analog input values.
        """
        try:
            return self.task.read(number_of_samples_per_channel=1)
        except (nidaqmx._lib.DaqNotFoundError,AttributeError):
            return [0.0]

    def getAIData_multi(self, num) -> list:
        """
        Obtain an analog input value.

        Returns:
            list: Analog input values.
        """
        try:
            return self.task.read(number_of_samples_per_channel=num)
        except (nidaqmx._lib.DaqNotFoundError,AttributeError):
            return [0.0]


class NIDAQ_ao_task(NIDAQ_task):
    def __init__(self, port : str):
        """
        Constructor.

        Create an AO task
        """
        try:
            super().__init__()
            self.task.ao_channels.add_ao_voltage_chan(self.dev_name + "/" + port)
        except (nidaqmx._lib.DaqNotFoundError,AttributeError):
            pass

    def setAOData(self, data : float) -> None:
        """
        Set an analog output value.

        """
        try:
            return self.task.write(data, auto_start=False)
        except (nidaqmx._lib.DaqNotFoundError,AttributeError):
            return False


class NIDAQ_do_task(NIDAQ_task):
    def __init__(self, port : str, line : str):
        """
        Constructor.

        Create a DO task
        """
        try:
            super().__init__()
            self.task.do_channels.add_do_chan(self.dev_name + "/" + port + "/" + line, line_grouping=LineGrouping.CHAN_PER_LINE)
        except (nidaqmx._lib.DaqNotFoundError,AttributeError):
            pass

    def setDOData(self, data : bool) -> None:
        """
        Set a digital output value.

        """
        try:
            return self.task.write(data, auto_start=False)
        except (nidaqmx._lib.DaqNotFoundError,AttributeError):
            return False