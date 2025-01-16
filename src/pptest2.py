import pandapower as pp
import numpy as np
import pandas as pd

def create_ieee39():
    """
    Create IEEE 39-bus (New England) test system in pandapower
    Returns: pandapower network
    """
    # Create empty network with 100 MVA base power
    net = pp.create_empty_network(name="IEEE 39-bus", sn_mva=100.0)
    
    # Create buses (nominal voltage in kV)
    for i in range(1, 40):
        if i <= 29:  # Buses 1-29 are 345kV
            pp.create_bus(net, vn_kv=345, name=f"Bus {i}", index=i-1)
        else:  # Buses 30-39 are generator buses at 345kV
            pp.create_bus(net, vn_kv=345, name=f"Bus {i}", index=i-1)
    
    # Create lines
    line_data = [
        (1, 2, 0.0035, 0.0411, 0.6987), (1, 39, 0.001, 0.025, 0.75),
        (2, 3, 0.0013, 0.0151, 0.2572), (2, 25, 0.007, 0.0086, 0.146),
        (3, 4, 0.0013, 0.0213, 0.2214), (3, 18, 0.0011, 0.0133, 0.2138),
        (4, 5, 0.0008, 0.0128, 0.1342), (4, 14, 0.0008, 0.0129, 0.1382),
        (5, 6, 0.0002, 0.0026, 0.0434), (5, 8, 0.0008, 0.0112, 0.1476),
        (6, 7, 0.0006, 0.0092, 0.113), (6, 11, 0.0007, 0.0082, 0.1389),
        (7, 8, 0.0004, 0.0046, 0.078), (8, 9, 0.0023, 0.0363, 0.3804),
        (9, 39, 0.001, 0.025, 1.2), (10, 11, 0.0004, 0.0043, 0.0729),
        (10, 13, 0.0004, 0.0043, 0.0729), (13, 14, 0.0009, 0.0101, 0.1723),
        (14, 15, 0.0018, 0.0217, 0.366), (15, 16, 0.0009, 0.0094, 0.171),
        (16, 17, 0.0007, 0.0089, 0.1342), (16, 19, 0.0016, 0.0195, 0.304),
        (16, 21, 0.0008, 0.0135, 0.2548), (16, 24, 0.0003, 0.0059, 0.068),
        (17, 18, 0.0007, 0.0082, 0.1319), (17, 27, 0.0013, 0.0173, 0.3216),
        (21, 22, 0.0008, 0.014, 0.2565), (22, 23, 0.0006, 0.0096, 0.1846),
        (23, 24, 0.0022, 0.035, 0.361), (25, 26, 0.0032, 0.0323, 0.513),
        (26, 27, 0.0014, 0.0147, 0.2396), (26, 28, 0.0043, 0.0474, 0.7802),
        (26, 29, 0.0057, 0.0625, 1.029), (28, 29, 0.0014, 0.0151, 0.249)
    ]
    
    for from_bus, to_bus, r_pu, x_pu, b_pu in line_data:
        pp.create_line_from_parameters(
            net,
            from_bus=from_bus-1,
            to_bus=to_bus-1,
            length_km=1,
            r_ohm_per_km=r_pu * 345**2 / 100,
            x_ohm_per_km=x_pu * 345**2 / 100,
            c_nf_per_km=b_pu * 100 / 345**2,
            max_i_ka=2
        )
    
    # Create loads first
    load_data = [
        (3, 322, 2.4), (4, 500, 184), (7, 233.8, 84),
        (8, 522, 176), (12, 8.5, 88), (15, 320, 153),
        (16, 329, 32.3), (18, 158, 30), (20, 680, 103),
        (21, 274, 115), (23, 247.5, 84.6), (24, 308.6, -92.2),
        (25, 224, 47.2), (26, 139, 17), (27, 281, 75.5),
        (28, 206, 27.6), (29, 283.5, 26.9), (31, 9.2, 4.6),
        (39, 1104, 250)
    ]
    
    for bus, p_mw, q_mvar in load_data:
        pp.create_load(
            net,
            bus=bus-1,
            p_mw=p_mw,
            q_mvar=q_mvar
        )
    
    # Create generators with correct initial P values
    gen_data = [
        (30, 250, 1.0475), (31, 573.2, 0.9820), (32, 650, 0.9831),
        (33, 632, 0.9972), (34, 508, 1.0123), (35, 650, 1.0493),
        (36, 560, 1.0635), (37, 540, 1.0278), (38, 830, 1.0265),
        (39, 1000, 1.0300)
    ]
    
    # Set bus 31 as slack, others as PV
    for i, (bus, p_mw, vm_pu) in enumerate(gen_data):
        pp.create_gen(
            net,
            bus=bus-1,
            p_mw=p_mw,
            vm_pu=vm_pu,
            slack=True if bus == 31 else False,
            min_q_mvar=-999,
            max_q_mvar=999
        )
    
    return net

def run_and_print_results(net):
    """
    Run power flow and print formatted results
    """
    # Run power flow with increased max iterations
    pp.runpp(net, enforce_q_lims=True, max_iteration=100)
    
    # Format bus results
    bus_results = pd.DataFrame({
        'Bus': net.bus.index + 1,
        'Voltage (pu)': net.res_bus.vm_pu.values,
        'Angle (deg)': net.res_bus.va_degree.values,
        'P Load (MW)': net.res_bus.p_mw.values,
        'Q Load (MVar)': net.res_bus.q_mvar.values
    }).round(4)
    
    # Format generator results
    gen_results = pd.DataFrame({
        'Bus': net.gen.bus.values + 1,
        'P Gen (MW)': net.res_gen.p_mw.values,
        'Q Gen (MVar)': net.res_gen.q_mvar.values,
        'Voltage Setpoint (pu)': net.gen.vm_pu.values
    }).round(4)
    
    # Format line loading results
    line_results = pd.DataFrame({
        'From Bus': net.line.from_bus.values + 1,
        'To Bus': net.line.to_bus.values + 1,
        'Loading (%)': net.res_line.loading_percent.values,
        'P From (MW)': net.res_line.p_from_mw.values,
        'Q From (MVar)': net.res_line.q_from_mvar.values,
        'P Losses (MW)': net.res_line.pl_mw.values
    }).round(4)
    
    print("\n=== Bus Results ===")
    print(bus_results.to_string(index=False))
    
    print("\n=== Generator Results ===")
    print(gen_results.to_string(index=False))
    
    print("\n=== Line Results ===")
    print(line_results.to_string(index=False))
    
    # Print total losses
    total_losses = net.res_line.pl_mw.sum()
    print(f"\nTotal System Losses: {total_losses:.2f} MW")

# Create network and run power flow
net = create_ieee39()
run_and_print_results(net)
