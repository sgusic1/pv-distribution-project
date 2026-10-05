import pandas as pd
import pandapower as pp
from network_model import create_network

net = create_network()

# Load and run the network simulation
pp.runpp(net)

# !. Busbar results
print("\n=== BUSBAR VOLTAGES ===")
bus_results = pd.concat([net.bus[["name", "vn_kv"]], net.res_bus[["vm_pu", "va_degree"]]], axis=1)
bus_results["vm_kv"] = bus_results["vm_pu"] * bus_results["vn_kv"]
print(bus_results[["name", "vn_kv", "vm_pu", "vm_kv", "va_degree"]])

# 2. Line (Feeder) Results
print("\n=== LINE RESULTS ===")
line_results = pd.concat([net.line[["name", "length_km"]], net.res_line[["loading_percent", "p_from_mw", "q_from_mvar", "p_to_mw", "q_to_mvar", "pl_mw"]]], axis=1)
print(line_results)

# 3. Transformer results
print("\nTRANSFORMER RESULTS:")
trafo_results = pd.concat([net.trafo[["name", "sn_mva"]], net.res_trafo[["loading_percent", "p_hv_mw", "q_hv_mvar",  "p_lv_mw", "q_lv_mvar","pl_mw"]]], axis=1)
print(trafo_results[["name", "sn_mva", "loading_percent", "p_hv_mw", "q_hv_mvar", "p_lv_mw", "q_lv_mvar","pl_mw"]])

# 4. Power from external grid
print("\nPOWER IMPORT FROM 110 kV EXTERNAL GRID:")
print(net.res_ext_grid[["p_mw", "q_mvar"]])