import pandapower as pp

# Create an empty pandapower network
net = pp.create_empty_network()

# Add buses
buses = {}
for i in range(1, 40):  # IEEE 39-bus system has buses numbered from 1 to 39
    buses[i] = pp.create_bus(net, vn_kv=345 if i <= 29 else 138)  # 345kV or 138kV levels

# Add generators
pp.create_gen(net, buses[30], p_mw=520, vm_pu=1.03, slack=True)  # Slack bus generator
generators = [
    (31, 650), (32, 632), (33, 508), (34, 650), (35, 560),
    (36, 540), (37, 830), (38, 800), (39, 1000)
]
for bus, p_mw in generators:
    pp.create_gen(net, buses[bus], p_mw=p_mw, vm_pu=1.02)

# Add loads
loads = [
    (3, 97), (4, 180), (7, 74), (8, 71), (11, 38), (12, 35),
    (14, 124), (15, 90), (16, 91), (18, 333), (20, 181),
    (21, 128), (23, 64), (24, 95), (25, 93), (26, 102), (29, 120)
]
for bus, p_mw in loads:
    pp.create_load(net, buses[bus], p_mw=p_mw, q_mvar=p_mw * 0.3)  # Assuming 0.3 power factor for reactive power

# Add transmission lines
lines = [
    (1, 2, 0.0035, 0.0411, 0.6987),
    (1, 39, 0.001, 0.025, 0.75),
    (2, 3, 0.0013, 0.0151, 0.2572),
    (2, 25, 0.007, 0.0086, 0.146),
    (3, 4, 0.0013, 0.0213, 0.2214),
    # Add remaining transmission lines
]
for from_bus, to_bus, r, x, c in lines:
    pp.create_line_from_parameters(net, buses[from_bus], buses[to_bus], length_km=1.0,
                                   r_ohm_per_km=r, x_ohm_per_km=x, c_nf_per_km=c * 1e9, max_i_ka=1.0)

# Add transformers (example data)
transformers = [
    (30, 2, 100, 345, 138, 0.01, 0.05),
    (30, 3, 100, 345, 138, 0.01, 0.05),
]
for hv_bus, lv_bus, sn_mva, vn_hv_kv, vn_lv_kv, vk_percent, vkr_percent in transformers:
    pp.create_transformer_from_parameters(net, buses[hv_bus], buses[lv_bus],
                                          sn_mva=sn_mva, vn_hv_kv=vn_hv_kv, vn_lv_kv=vn_lv_kv,
                                          vk_percent=vk_percent, vkr_percent=vkr_percent)

# Run power flow
pp.runpp(net)

# Display results
print("Power Flow Results:")
print(net.res_bus)
print(net.res_line)
print(net.res_trafo)
