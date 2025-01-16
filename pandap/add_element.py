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
    with open(buses_data,"r") as file:
        reader = csv.DictReader(file, fieldnames=['vn_kv', 'name', 'index'])
        
        for bus in reader:
            pp.create_bus(net,vn_kv = float(bus['vn_kv']),name = bus['name'], index = int(bus['index']))


def add_trans(transes_data,net):
    with open(transes_data,"r") as file:
        reader = csv.DictReader(file,fieldnames=['hv_bus', 'lv_bus', 'name', 'std_type', 'index']) 

        for trans in reader:
            pp.create_transformer(net,hv_bus= int(trans['hv_bus']), lv_bus=int(trans['lv_bus']), name=trans['name'], std_type= trans['std_type'],index=int(trans['index']))


def add_trans_from_param(transes_data,net):
    with open(transes_data,"r") as file:
        reader = csv.DictReader(file,fieldnames=['hv_bus', 'lv_bus','sn_mva','vn_hv_kv','vn_lv_kv','vkr_percent','vk_percent','pfe_kw','i0_percent'])

        for trans in reader:
            pp.create_transformer_from_parameters(net,hv_bus=int(trans['hv_bus']),lv_bus=int(trans['lv_bus']),sn_mva=float(trans['sn_mva']),vn_hv_kv=float(trans['vn_hv_kv']),vn_lv_kv=float(trans['vn_lv_kv']),vkr_percent=float(trans['vkr_percent']),vk_percent=float(trans['vk_percent']),pfe_kw=float(trans['pfe_kw']),i0_percent=float(trans['i0_percent']))

        
def add_line(lines_data, net):
    with open(lines_data,"r") as file:
        reader = csv.DictReader(file, fieldnames=['from_bus', 'to_bus', 'length_km', 'name', 'std_type', 'index'])

        for line in reader:
            pp.create_line(net,from_bus=int(line['from_bus']), to_bus=int(line['to_bus']), length_km= float(line['length_km']), name= line['name'],std_type= line['std_type'], index=int(line['index']))


def add_line_from_param(lines_data, net):
    with open(lines_data,"r") as file:
        reader = csv.DictReader(file, fieldnames=['from_bus','to_bus','length_km','r_ohm_per_km','x_ohm_per_km', 'c_nf_per_km','max_i_ka'])

        for line in reader:
            pp.create_line_from_parameters(net,from_bus=int(line['from_bus']), to_bus=int(line['to_bus']), length_km= float(line['length_km']), r_ohm_per_km= float(line['r_ohm_per_km']),x_ohm_per_km= float(line['x_ohm_per_km']), c_nf_per_km=float(line['c_nf_per_km']), max_i_ka=float(line['max_i_ka']))



def add_gen(gens_data, net):
    with open(gens_data,"r") as file:
        reader = csv.DictReader(file, fieldnames=['bus', 'p_mw', 'vm_pu', 'sn_mva', 'name', 'index','slack'])
        
        for gen in reader:
            pp.create.create_gen(net,bus=int(gen['bus']),p_mw=float(gen['p_mw']),vm_pu=float(gen['vm_pu']),sn_mva = float(gen['sn_mva']),name = gen['name'],index = int(gen['index']), slack = gen['slack'])


def add_load(loads_data, net):
    with open(loads_data,"r") as file:
        reader = csv.DictReader(file,fieldnames=['bus','p_mw','q_mvar','index'])

        for load in reader:
            pp.create_load(net,bus=int(load['bus']),p_mw=float(load['p_mw']),q_mvar=float(load['q_mvar']),index=int(load['index']))

def lf(net):
    pp.runpp(net)

def lf_res(net):
    return dict(net.res_bus)

def line_loss(lines_data,net):
    with open(lines_data) as file:
        reader = csv.DictReader(file,fieldnames=['from_bus','to_bus','length_km','r_ohm_per_km','x_ohm_per_km', 'c_nf_per_km','max_i_ka'])


def impedance_pu(Z_pu:float,Z_base:float)->float:
    return Z_pu*Z_base


def voltage_pu(V_pu:float,V_base:float)->float:
    return V_pu*V_base


def power_pu(P_pu:float,S_base:float)->float:
    return P_pu*S_base

# this function can do everything that is written above so all are ok:)
def pu(pu:float,base:float)->float:
    return pu*base


def main():
    # net = create_net("network1")
    # add_bus(buses_data, net)
    # add_line(lines_data,net)
    # add_trans(tranfomers_data,net)
    # add_gen(gens_data,net)
    # add_load(loads_data,net)
    # print(net.bus)
    # print(net.bus)
    # print(net.trafo)
    # print(net.line)
    # pp.plotting.simple_plot(net)
    # pp.runpp(net)
    # print(net.res_bus)
    # print(colored('the program runned succesfully!','green'))
    # lf(net)
    # print(lf_res)

    q = float(input('q: '))
    sbase = float(input('Sb: '))
    print(pu(q,sbase))

if __name__ == "__main__":
    main()