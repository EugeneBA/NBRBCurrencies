import json
import io
import matplotlib.pyplot as plt

from datetime import datetime

eurFilename = ".\\EUR-2000-2023.json"
usdFilename = ".\\USD-2000-2023.json"

with open(eurFilename, 'r') as f:
    eurRawData = json.load(f)

with open(usdFilename, 'r') as f:
    usdRawData = json.load(f)

eurDates = [datetime.fromisoformat(i['Date']) for i in eurRawData]
eurVals = [i['Cur_OfficialRate'] for i in eurRawData]
eurDenomVals = [val if val<7 else val*0.0001 for val in eurVals]

usdDates = [datetime.fromisoformat(i['Date']) for i in usdRawData]
usdVals = [i['Cur_OfficialRate'] for i in usdRawData]
usdDenomVals = [val if val<7 else val*0.0001 for val in usdVals]

plt.plot(eurDates, eurDenomVals)
plt.title("1 EUR")
plt.ylabel("BYN")
plt.grid(True)

plt.figure()
plt.plot(usdDates[0:], usdDenomVals[0:])
plt.title("1 USD")
plt.ylabel("BYN")
plt.grid(True)

plt.show()