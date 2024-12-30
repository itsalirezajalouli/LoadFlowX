import pandapower as pp
import csv
from termcolor import colored


buses_data = 'buses.csv'
lines_data = 'lines.csv'
tranfomers_data = 'transformers.csv'
gens_data = 'gens.csv'
loads_data = 'loads.csv'


def create_net(network,f:float = 50, s:float = 100):
    net = pp.create.create_empty_network(name=network, f_hz= f, sn_mva= s, add_stdtypes=True)
    return net


def add_bus(buses_data, net):
    buses = []
    with open(buses_data,"r") as file:
        reader = csv.DictReader(file, fieldnames=['vn_kv', 'name', 'index'])
        for _ in reader:
            buses.append(_)
        
        for bus in buses:
            pp.create_bus(net,vn_kv = float(bus['vn_kv']),name = bus['name'], index = int(bus['index']))


def add_trans(transes_data,net):
    transes = []
    with open(transes_data,"r") as file:
        reader = csv.DictReader(file,fieldnames=['hv_bus', 'lv_bus', 'name', 'std_type', 'index'])
        for _ in reader:
            transes.append(_)   

        for trans in transes:
            pp.create_transformer(net,hv_bus= int(trans['hv_bus']), lv_bus=int(trans['lv_bus']), name=trans['name'], std_type= trans['std_type'],index=int(trans['index']))

        
def add_line(lines_data, net):
    lines = []
    with open(lines_data,"r") as file:
        reader = csv.DictReader(file, fieldnames=['from_bus', 'to_bus', 'length_km', 'name', 'std_type', 'index'])
        for _ in reader:
            lines.append(_)

        for line in lines:
            pp.create_line(net,from_bus=int(line['from_bus']), to_bus=int(line['to_bus']), length_km= float(line['length_km']), name= line['name'],std_type= line['std_type'], index=int(line['index']))


def add_gen(gens_data, net):
    gens = []
    with open(gens_data,"r") as file:
        reader = csv.DictReader(file, fieldnames=['bus', 'p_mw', 'vm_pu', 'sn_mva', 'name', 'index','slack'])
        for _ in reader :
            gens.append(_)
        
        for gen in gens:
            pp.create.create_gen(net,bus=int(gen['bus']),p_mw=float(gen['p_mw']),vm_pu=float(gen['vm_pu']),sn_mva = float(gen['sn_mva']),name = gen['name'],index = int(gen['index']), slack = gen['slack'])


def add_load(loads_data, net):
    loads = []
    with open(loads_data,"r") as file:
        reader = csv.DictReader(file,fieldnames=['bus','p_mw','q_mvar','index'])
        for _ in reader:
            loads.append(_)

        for load in loads:
            pp.create_load(net,bus=int(load['bus']),p_mw=float(load['p_mw']),q_mvar=float(load['q_mvar']),index=int(load['index']))


def main():
    net = create_net("network1")
    add_bus(buses_data, net)
    add_line(lines_data,net)
    add_trans(tranfomers_data,net)
    add_gen(gens_data,net)
    add_load(loads_data,net)
    print(net)
    # print(net.bus)
    # print(net.trafo)
    # print(net.line)
    # pp.plotting.simple_plot(net)
    # pp.runpp(net)
    # print(net.res_bus)
    print(colored('the program runned succesfully!','green'))

if __name__ == "__main__":
    main()