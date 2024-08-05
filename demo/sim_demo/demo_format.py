import sys, getopt, os
import json


file_name = None
out_name = None
base_ts = 1719309600
data = {}

try:
    opts, args = getopt.getopt(sys.argv[1:],"f:o:",["file=", "out="])
except getopt.GetoptError as err:
    print(err)
    print('HINT: main.py -t <arq topologia>')
    print('MORE INFO: main.py --help')
    sys.exit(1)
for opt, arg in opts:
    if opt in ("-f", "--file"):
        file_name = arg
    elif opt in ("-o", "--out"):
        out_name = arg

if(file_name == None):
    print("Error: Missing Argument")
    print('HINT: main.py -f <fcd-output file>')
    print("  O parâmetro -f é obrigatório!!!")
    sys.exit(1)


if(out_name == None):
    print("Error: Missing Argument")
    print('HINT: main.py -o <output file>')
    print("  O parâmetro -o é obrigatório!!!")
    sys.exit(1)

with open(file_name) as data_file:
    data = json.load(data_file)
    f = open(out_name, "w")

    for ts in data:
        if float(ts) < 300:
            if float(ts)%60 == 42:
                sch_ts = base_ts + int(float(ts))
                
                for msg in data[ts]:
                    for i in range(len(msg['gp200'])):
                        msg['gp200'][i] = "\""+msg['gp200'][i]+"\""
                    line = '{\"bus_id\": \"'+ msg['bus_id']+ '\", \"trip_id\": \"'+ msg['bus_id']+ ';1\", \"lat\": '+ str(msg['lat'])+', \"lon\": '+ str(msg['lon'])+', \"spd\": '+str(msg['spd'])+', \"ts\": '+str(sch_ts)+ ', \"links\": ['+", ".join(msg['gp200'])+']}\n'
                    f.write(line)
            
    f.close()
