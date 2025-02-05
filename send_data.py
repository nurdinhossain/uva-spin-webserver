import u3
import requests
import time

# METHODS
def update_dac(device: u3.U3, input_volts: float) -> None:
    dac_value = device.voltageToDACBits(volts=input_volts, dacNumber=0, is16Bits=False)
    device.getFeedback(u3.DAC0_8(dac_value))

def send_data(device: u3.U3, timestamp: float):
    # read AIN0 data
    ain0bits, = device.getFeedback(u3.AIN(PositiveChannel=0, NegativeChannel=31, LongSettling=False, QuickSample=False))
    ainValue = device.binaryToCalibratedAnalogVoltage(bits=ain0bits, isLowVoltage=False, isSingleEnded=True, isSpecialSetting=False, channelNumber=0)

    # send AIN0 data in POST reqest
    payload = {str(timestamp): str(ainValue)}
    res = requests.post('http://172.28.36.9:5000/receive-data', json=payload)
    print("Response:", res.text)

if __name__ == "__main__":
    # get code start time
    start = time.time()

    # grab LabJack device
    d = u3.U3()

    # variable for storing current voltage
    dac_voltage = 0
    
    # update starting dac
    update_dac(d, dac_voltage)

    while True:
        # send data
        send_data(d, time.time() - start)

        # increment voltage
        dac_voltage = (dac_voltage + 0.5) % 5
        update_dac(d, dac_voltage)

        # restrict data send to every 5 seconds
        time.sleep(5)
    

    print(voltage)
