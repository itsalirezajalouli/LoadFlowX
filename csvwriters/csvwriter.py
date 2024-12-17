import csv


def Bus_csvMkr(data:dict,file_name):
    with open(file_name,"a",newline='') as file:
        writer = csv.DictWriter(file,fieldnames=['id','name','pos','bType','vMag','vAng','P','Q'])
        writer.writeheader()
        writer.writerow(data)

def main():
    data_inputs = ['id','name','pos','bType','vMag','vAng','P','Q']
    Data = {}
    for data in data_inputs:
        user_input = input(f'{data}: ')
        Data[data] = user_input

    file_name = input('Ok i wanna save this data choose a name: ')

    Bus_csvMkr(Data,file_name)

if __name__ == "__main__":
    main()