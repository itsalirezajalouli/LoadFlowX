import pandapower as pp
import pandapower.networks as pn
import pandas as pd

def run_and_save_results(network_name, filename):
    # Load network
    if network_name == "case9":
        net = pn.case9()
    elif network_name == "case39":
        net = pn.case39()
    else:
        raise ValueError("Unsupported network name")
    
    # Run power flow
    pp.runpp(net)
    
    # Save results to CSV
    bus_results = net.res_bus
    line_results = net.res_line
    gen_results = net.res_gen
    
    bus_results.to_csv(f"{filename}_bus.csv")
    line_results.to_csv(f"{filename}_line.csv")
    gen_results.to_csv(f"{filename}_gen.csv")
    
    print(f"Results saved for {network_name}")

# Run and save for IEEE 9-bus and 39-bus systems
run_and_save_results("case9", "case9_results")
run_and_save_results("case39", "case39_results")

