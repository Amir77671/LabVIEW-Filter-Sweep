import pyvisa
import math
import matplotlib.pyplot as plt

rm = pyvisa.ResourceManager()

oscyloskop = rm.open_resource('GPIB0::1::INSTR')
generator = rm.open_resource('GPIB8::2::INSTR')

oscyloskop.timeout = 1000
generator.timeout = 1000

generator.write('SOUR1:VOLT:AMPLITUDE 1')
generator.write('SOUR1:FREQ:CW 1000')
generator.write('OUTP ON')
generator.query('*OPC?')

oscyloskop.write('*RST"')
oscyloskop.query('*OPC?')
oscyloskop.write('CHANNEL1:RANGE 2')
oscyloskop.write('CHANNEL1:COUPLING DC')
oscyloskop.write('CHANNEL2:RANGE 2')
oscyloskop.write('CHANNEL2:COUPLING DC')
oscyloskop.write('TIMEBASE:RANGE 1')


freq = []
att = []


for i in range(100):
    freq.append(i)
    generator.write(f'SOUR1:FREQ:CW {1000*i}')
    generator.query('*OPC?')
    oscyloskop.write('CHAN1:INPU')
    oscyloskop.write('AUT')
    oscyloskop.write('*TRG')
    oscyloskop.query('*OPC?')
    ampCH1 = oscyloskop.query(float('MEASURE:VRMS?'))
    oscyloskop.write('CHAN2:INPU')
    oscyloskop.write('*TRG')
    oscyloskop.query('*OPC?')
    ampCH2 = oscyloskop.query(float('MEASURE:VRMS?'))
    att.append(20*math.log(ampCH2/ampCH1))
    print(freq[-1], att[-1])


print(freq)
print(att)
generator.write('OUTP OFF')

plt.plot(freq, att)
plt.ylabel('Tlumienie [dB]')
plt.ylabel('Częstotliwość [kHz]')
plt.show()