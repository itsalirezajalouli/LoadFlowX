# Imports
import csv
import pandapower as pp

# Methods of load flow calculations 
def runLoadFlow(projectPth: str, busCsv: str, lineCsv: str, trafoCsv: str, 
                genCsv: str, loadCsv: str, slacksCsv: str, method: str, maxIter) -> bool:

    # Create empty network from scratch
    net = pp.create_empty_network()

    # Load and add buses
    with open(busCsv) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            pp.create_bus(
                net, vn_kv = float(row['vMag']), name = row['name'], index = int(row['id'])
            )
    
    # Load and add lines
    with open(lineCsv) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['bus1id'] != row['bus2id']:
                fromBus, toBus = int(row['bus1id']), int(row['bus2id'])
                pp.create_line(
                    net, from_bus = fromBus, to_bus = toBus, length_km = float(row['len']),
                    name = row['name'], std_type = 'NAYY 4x50 SE'
                )

    # Load and add generators
    with open(genCsv) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            pp.create_gen(
                net, bus = int(row['bus']), name = row['name'], p_mw = float(row['pMW']),
                vm_pu = 1.0, min_q_mvar = -50.0, max_q_mvar = 50.0
            )

    # Load and add transformers
    with open(trafoCsv) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            pp.create_transformer(
                net, hv_bus = int(row['hvBus']), lv_bus = int(row['lvBus']),
                name = row['name'], std_type = '0.4 MVA 20/0.4 kV'
            )
    
    # Load and add loads
    with open(loadCsv) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            pp.create_load(net, bus = int(row['bus']), p_mw = float(row['pMW']), q_mvar = float(row['qMW']))

    # Load and add slacks
    with open(slacksCsv) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            pp.create_ext_grid(net, bus = int(row['bus']), vm_pu = float(row['vmPU']))

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
    pp.runpp(
        net, algorithm = method, init = 'flat', enforce_q_lims = True, numba = True,
        max_iteration = maxIter
    )

    # Check for convergence
    if not net.converged:
        return False

    # Save results
    elif net.converged:
        resultPath = f'{projectPth}/results'
        net.res_bus.to_csv(f'{resultPath}_buses.csv', index=True)
        net.res_line.to_csv(f'{resultPath}_lines.csv', index=True)
        net.res_trafo.to_csv(f'{resultPath}_trafos.csv', index=True)
        net.res_load.to_csv(f'{resultPath}_loads.csv', index=True)
        return True
