import pandapower as pp
import csv


buses_data = 'buses.csv'
lines_data = 'lines.csv'
tranfomers_data = 'transformers.csv'


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




def main():
    net = create_net("network1")
    add_bus(buses_data, net)
    add_line(lines_data,net)
    add_trans(tranfomers_data,net)
    print(net)
    print(net.bus)
    print(net.trafo)
    print(net.line)
    pp.plotting.simple_plot(net)

if __name__ == "__main__":
    main()