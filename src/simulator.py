# Imports
from csv import DictReader
import pandapower as pp

# Methods of load flow calculations 
def runLoadFlow(projectPth: str, busCsv: str, lineCsv: str, trafoCsv: str, 
                genCsv: str, loadCsv: str, slacksCsv: str, method: str, maxIter,
                freq: float, sBase) -> tuple[bool, str]:

    try:
        # Create empty network from scratch
        print('sBase:', sBase, 'freq:', freq)
        net = pp.create_empty_network(sn_mva = sBase, f_hz = freq)

        # Load and add buses
        with open(busCsv) as csvfile:
            reader = DictReader(csvfile)
            for row in reader:
                pp.create_bus(
                    net, vn_kv = float(row['vMag']), zone = int(row['zone']),
                    name = row['name'], index = int(row['id']), in_service = True,
                    type = 'b', max_vm_pu = float(row['maxVm']), min_vm_pu = float(row['minVm']),
                )
        
        # Load and add lines
        # First create the standard type with the actual parameters you want
        with open(lineCsv) as csvfile:
            reader = DictReader(csvfile)
            for row in reader:
                if row['bus1id'] != row['bus2id']:
                    # Create a unique std_type for each line
                    stdTypeName = f'custom_type_{row['name']}'
                    if row['R'] == 'None':
                        stdTypeName = 'NAYY 4x50 SE'
                    else:
                        pp.create_std_type(
                            net,
                            {
                                'r_ohm_per_km': float(row['R']),
                                'x_ohm_per_km': float(row['X']),
                                'c_nf_per_km': float(row['c_nf_per_km']),
                                'max_i_ka': float(row['max_i_ka']),
                                'type': 'ol',
                                'g_us_per_km': float(0)
                            },
                            name=stdTypeName,
                            element='line'
                        )
                    # if not given the std_type params set it to default

                    fromBus, toBus = int(row['bus1id']), int(row['bus2id'])
                    pp.create_line(
                        net, 
                        from_bus=int(fromBus),
                        to_bus=int(toBus), 
                        length_km=float(row['len']),
                        name=str(row['name']), 
                        std_type=stdTypeName,  # Use the custom type we just created
                        in_service=bool(True),
                        max_loading_percent=float(100), 
                        df=int(1), 
                        parallel=int(1),
                    )

        # Load and add generators
        with open(genCsv) as csvfile:
            reader = DictReader(csvfile)
            for row in reader:
                pp.create_gen(
                    net,
                    bus=int(row['bus']),
                    name=row['name'],
                    p_mw=float(row['pMW']),
                    vm_pu=float(row.get('vmPU', 1.0)),  # Default vm_pu to 1.0 if not present
                    min_q_mvar=float(row.get('minQMvar', -1e6)),  # Default to a large negative value if not present
                    max_q_mvar=float(row.get('maxQMvar', 1e6)),   # Default to a large positive value if not present
                    min_p_mw=float(row.get('minPMW', 0.0)),       # Default to 0.0 if not present
                    max_p_mw=float(row.get('maxPMW', 1e6)),       # Default to a large positive value if not present
                    controllable=True,  # Hardcoded to True
                    slack=False,        # Hardcoded to False
                    slack_weight=0,     # Hardcoded to 0
                    index = int(row['id'])
                )

        # Load and add transformers
        with open(trafoCsv) as csvfile:
            reader = DictReader(csvfile)
            for row in reader:
                # Extract parameters
                hv_bus = int(row["hvBus"])
                lv_bus = int(row["lvBus"])
                sn_mva = float(row["sn_mva"])
                vk_percent = float(row["vk_percent"])
                vkr_percent = float(row["vkr_percent"])
                tap_step_percent = float(row["tap_step_percent"])

                # Create a custom transformer standard type
                std_type = createTransformerStdType(
                    net,
                    hv_kv=net.bus.vn_kv[hv_bus],
                    lv_kv=net.bus.vn_kv[lv_bus],
                    sn_mva=sn_mva,
                    vk_percent=vk_percent,
                    vkr_percent=vkr_percent,
                    tap_step_percent=tap_step_percent,
                )

                # Add transformer to the network
                pp.create_transformer(
                    net,
                    hv_bus=hv_bus,
                    lv_bus=lv_bus,
                    name=row["name"],
                    std_type=std_type,
                    index = int(row['id'])
                )
                print(f"Transformer {row['name']} added to the network.")
        
        # Load and add loads
        with open(loadCsv) as csvfile:
            reader = DictReader(csvfile)
            counter = 0
            for row in reader:
                counter += 1
                pp.create_load(net,
                               name = counter,
                               bus = int(row['bus']),
                               p_mw = float(row['pMW']),
                               q_mvar = float(row['qMW']),
                               scaling = 1,
                               type = None,
                               in_service = True,
                               index = int(row['id']),
                               controllable = False)

        # Load and add slacks
        with open(slacksCsv) as csvfile:
            reader = DictReader(csvfile)
            for row in reader:
                pp.create_ext_grid(net, bus = int(row['bus']), vm_pu = float(row['vmPU']),
                                   va_degree = float(row['vaD']), slack_weight = 1,
                                   in_service = True, max_p_mw = float(row['maxP']), min_p_mw = float(row['minP']),
                                   max_q_mvar = float(row['maxQ']), min_q_mvar = float(row['minQ']),
                                   index = int(row['id']))

        # Run power flow
        print('bus', 30 * '-')
        print(net.bus)
        print('line', 30 * '-')
        print(net.line)
        print('trafo', 30 * '-')
        print(net.trafo)
        print('load', 30 * '-')
        print(net.load)
        print('gen', 30 * '-')
        print(net.gen)
        print('slack', 30 * '-')
        print(net.ext_grid)

        try:
            pp.runpp(
                net, algorithm = method, init = 'flat', enforce_q_lims = True, numba = True,
                max_iteration = maxIter
            )

        # Check for convergence
        except pp.LoadflowNotConverged:
            return False, 'Load flow did not converge'

        # Save network's data
        dataPath = f'{projectPth}/data'
        net.bus.to_csv(f'{dataPath}_buses.csv', index=True)
        net.line.to_csv(f'{dataPath}_lines.csv', index=True)
        net.trafo.to_csv(f'{dataPath}_trafos.csv', index=True)
        net.load.to_csv(f'{dataPath}_loads.csv', index=True)
        net.gen.to_csv(f'{dataPath}_gens.csv', index=True)
        net.ext_grid.to_csv(f'{dataPath}_slacks.csv', index=True)

        # Save results
        resultPath = f'{projectPth}/results'
        net.res_bus.to_csv(f'{resultPath}_buses.csv', index=True)
        net.res_line.to_csv(f'{resultPath}_lines.csv', index=True)
        net.res_trafo.to_csv(f'{resultPath}_trafos.csv', index=True)
        net.res_load.to_csv(f'{resultPath}_loads.csv', index=True)
        net.res_gen.to_csv(f'{resultPath}_gens.csv', index=True)
        net.res_ext_grid.to_csv(f'{resultPath}_slacks.csv', index=True)
        return True, ''

    except Exception as e:
        return False, str(e)

def createTransformerStdType(net, hv_kv, lv_kv, sn_mva, vk_percent, vkr_percent, tap_step_percent):
    # Create a transformer standard type in the pandapower network.
    std_type_name = f"custom_std_type_{hv_kv}_{lv_kv}"
    pp.create_std_type(
        net,
        {
            "sn_mva": sn_mva,
            "vn_hv_kv": hv_kv,
            "vn_lv_kv": lv_kv,
            "vk_percent": vk_percent,
            "vkr_percent": vkr_percent,
            "pfe_kw": 0,  # Default value for iron losses
            "i0_percent": 0,  # Default value for no-load current
            "shift_degree": 0,  # Default phase shift
            "tap_side": "hv",  # Default tap side
            "tap_neutral": 0,
            "tap_max": 0,
            "tap_min": 0,
            "tap_step_percent": tap_step_percent,
        },
        name=std_type_name,
        element="trafo",
    )
    return std_type_name
