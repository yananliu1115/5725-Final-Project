import os
import time
import pandas as pd

localtime = time.localtime(time.time())
day = localtime.tm_mday
month = localtime.tm_mon
hour = 0
hour = int(hour)
filename = "2021"+"-"+str(month)+"-"+str(day)+"-"+str(hour)+".csv"
folderPath = "/Users/yananliu/Documents/5725/FinalProject/"
filepath = folderPath+filename
#turns
df = pd.read_csv(filepath)
df.values
data = df.values
data = list(map(list, zip(*data)))
data = pd.DataFrame(data)
newfilepath = folderPath +"2021"+"-"+str(month)+"-"+str(day)+"-"+str(hour)+"new"+".csv"
data.to_csv(newfilepath, header=0, index=0)
mycsv=pd.read_csv(newfilepath)
#print (mycsv)
#column_headers = list(mycsv.columns.values)
#print(column_headers)

ca = mycsv['California ']
ny = mycsv['New York ']
texas = mycsv['Texas ']
Florida = mycsv['Florida ']
Illinois = mycsv['Illinois ']

def to_dict(ca):
    ca_dict = {}

    ca_dict['infected_total'] = ca[0]
    ca_dict['infected_today'] = ca[1]
    ca_dict['death_total'] = ca[2]
    ca_dict['death_today'] = ca[3]
    ca_dict['recovered_total'] = ca[4]
    ca_dict['active case'] = ca[5]
    ca_dict['state'] = str(ca)

    return ca_dict

ca_dict = to_dict(ca)
ny_dict = to_dict(ny)
texas_dict = to_dict(texas)
Florida_dict = to_dict(Florida)
Illinois_dict = to_dict(Illinois)

print (ca_dict)
print (ny_dict)
print (texas_dict)
print (Illinois_dict)








