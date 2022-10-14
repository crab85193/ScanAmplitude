import nidaqmx

sys = nidaqmx.system.System()
dev = sys.devices.device_names

task = nidaqmx.Task()

task.ai_channels.add_ai_voltage_chan(dev[0] + '/' + 'ai0')

task.start()

print(task.read(number_of_samples_per_channel=1))

task.stop()
# task.close()

# task = nidaqmx.Task()

task.close()

task = nidaqmx.Task()

task.ai_channels.add_ai_voltage_chan(dev[0] + '/' + 'ai0')

task.start()

print(task.read(number_of_samples_per_channel=1))

task.stop()
task.close()

task = nidaqmx.Task()

task.ai_channels.add_ai_voltage_chan(dev[0] + '/' + 'ai1')

task.start()

print(task.read(number_of_samples_per_channel=1))

task.stop()
task.close()

task = nidaqmx.Task()
task.ai_channels.add_ai_voltage_chan(dev[0] + '/' + 'ai0')

task2 = nidaqmx.Task()
task2.ao_channels.add_ao_voltage_chan(dev[0] + '/' + 'ao0')

task.start()
task2.start()

print(task.read(number_of_samples_per_channel=1))
task2.write(1.0)

task.stop()
task2.stop()
task.close()
task2.close()
