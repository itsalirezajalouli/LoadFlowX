import csv


def Bus_csvMkr(data:dict,file_name):
    with open(file_name,"a",newline='') as file:
        writer = csv.DictWriter(file,fieldnames=['id','name','pos','bType','vMag','vAng','P','Q'])
        # if int(data[id]) == 1:
        #     writer.writeheader()
        writer.writerow(data)

def Trans_csvMkr(data:dict,file_name):
    with open(file_name,"a",newline="") as file:
        writer = csv.DictWriter(file,fieldnames=['id','name','pos','R','X','a','winding'])
        # if int(data[id]) == 1:
        #     writer.writeheader()
        writer.writerow(data)

def Line_csvMkr(data:dict,file_name):
    with open(file_name,"a",newline="") as file:
        writer = csv.DictWriter(file,fieldnames=['bus1id','bus2id','R','X','Length','vBase'])
        writer.writerow(data)



def bus_data_getter():
    data_inputs = ['id','name','pos','bType','vMag','vAng','P','Q']
    Data = {}
    for data in data_inputs:
        user_input = input(f'{data}: ')
        Data[data] = user_input
    return Data

def trans_data_getter():
    data_inputs = ['id','name','pos','R','X','a','winding']
    Data = {}
    for data in data_inputs:
        user_input = input(f'{data}: ')
        Data[data] = user_input
    return Data

def line_data_getter():
    data_inputs = ['bus1id','bus2id','R','X','Length','vBase']
    Data = {}
    for data in data_inputs:
        user_input = input(f'{data}: ')
        Data[data] = user_input
    return Data


def main():
    obj = input('What you want to add?(b for bus/t for trans/l for line): ')
    if obj == 'b':
        Data = bus_data_getter()
        file_name = input('Ok i wanna save this data choose a name: ')
        Bus_csvMkr(Data,file_name)

    elif obj == 't':
        Data = trans_data_getter()
        file_name = input('Ok i wanna save this data choose a name: ')
        Trans_csvMkr(Data,file_name)
        
    elif obj == 'l':
        Data = line_data_getter()
        file_name = input('Ok i wanna save this data choose a name: ')
        Line_csvMkr(Data,file_name)
        

if __name__ == "__main__":
    main()