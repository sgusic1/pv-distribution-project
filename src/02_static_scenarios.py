import os
import pandas as pd
import pandapower as pp
import matplotlib.pyplot as plt

from network_model import create_network


RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)

def run_scenario(scenario_name, pv_mw, load_p_mw, load_q_mvar):
    """
    Runs a single static scenario.

    pv_mw: PV power plant output in MW
    load_p_mw: active power of the consumer in MW
    load_q_mvar: reactive power of the consumer in Mvar
    """
    
    net = create_network()
    
    # Adjust load for the given scenario
    net.load.loc[0, "p_mw"] = load_p_mw
    net.load.loc[0, "q_mvar"] = load_q_mvar
    
    # Find the 0.4 kV busbar
    lv_bus = net.bus.index[net.bus["name"] == "B4 - 0.4 kV consumer and PV"][0]
    
    # Add PV power plant
    if pv_mw > 0:
        pp.create_sgen(
            net,
            bus=lv_bus,
            p_mw=pv_mw,
            q_mvar=0.0,
            name=f"PV Power Plant {pv_mw * 1000:.0f} kW"
        )
        
    # Load flow analysis
    pp.runpp(net, numba=False)
        
    # Calculate power losses across the network
    total_line_losses_mw = net.res_line["pl_mw"].sum()
    total_trafo_losses_mw = net.res_trafo["pl_mw"].sum()
    total_losses_mw = total_line_losses_mw + total_trafo_losses_mw

    # Compile the final scenario report dictionary
    result = {
        "scenario": scenario_name,
        "pv_kw": pv_mw * 1000,
        "load_kw": load_p_mw * 1000,
        "voltage_04_bus_pu": net.res_bus.loc[lv_bus, "vm_pu"],
        "min_voltage_pu": net.res_bus["vm_pu"].min(),
        "max_voltage_pu": net.res_bus["vm_pu"].max(),
        "grid_import_mw": net.res_ext_grid["p_mw"].sum(),
        "total_losses_mw": total_losses_mw,
        "max_line_loading_percent": net.res_line["loading_percent"].max(),
        "max_trafo_loading_percent": net.res_trafo["loading_percent"].max(),
    }
    
    
    voltage_rows = []

    for bus_idx, bus in net.bus.iterrows():
        voltage_rows.append({
            "scenario": scenario_name,
            "bus": bus["name"],
            "voltage_pu": net.res_bus.loc[bus_idx, "vm_pu"]
        })

    return result, voltage_rows



def main():
    scenarios = [
        {
            "name": "S0_without_PV",
            "pv_mw": 0.00,
            "load_p_mw": 0.35,
            "load_q_mvar": 0.12,
        },
        {
            "name": "S1_PV_100kW",
            "pv_mw": 0.10,
            "load_p_mw": 0.35,
            "load_q_mvar": 0.12,
        },
        {
            "name": "S2_PV_300kW",
            "pv_mw": 0.30,
            "load_p_mw": 0.35,
            "load_q_mvar": 0.12,
        },
        {
            "name": "S3_PV_500kW",
            "pv_mw": 0.50,
            "load_p_mw": 0.35,
            "load_q_mvar": 0.12,
        },
        {
            "name": "S4_PV_500kW_low_load",
            "pv_mw": 0.50,
            "load_p_mw": 0.15,
            "load_q_mvar": 0.05,
        },
        {
            "name": "S5_PV_500kW_high_load",
            "pv_mw": 0.50,
            "load_p_mw": 0.55,
            "load_q_mvar": 0.18,
        },
    ]
        
    summary_rows = []
    all_voltage_rows = []
        
        
    for scenario in scenarios:
        result, voltage_rows = run_scenario(
            scenario_name=scenario["name"],
            pv_mw=scenario["pv_mw"],
            load_p_mw=scenario["load_p_mw"],
            load_q_mvar=scenario["load_q_mvar"],
        )

        summary_rows.append(result)
        all_voltage_rows.extend(voltage_rows)
        
    summary_df = pd.DataFrame(summary_rows)
    voltage_df = pd.DataFrame(all_voltage_rows)

    summary_df.to_csv(f"{RESULTS_DIR}/static_scenario_summary.csv", index=False)
    voltage_df.to_csv(f"{RESULTS_DIR}/static_bus_voltages.csv", index=False)

    print("\nSTATIC SCENARIO SUMMARY: ")
    print(summary_df)
    
    # Graph 1: 0.4 kV busbar voltage
    plt.figure()
    plt.bar(summary_df["scenario"], summary_df["voltage_04_bus_pu"])
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("0.4 kV Busbar Voltage [p.u.]")
    plt.title("Impact of PV Power on Connection Point Voltage")
    plt.tight_layout()
    plt.savefig(f"{RESULTS_DIR}/static_voltage_04_bus.png", dpi=200)

    # Graph 2: Grid import
    plt.figure()
    plt.bar(summary_df["scenario"], summary_df["grid_import_mw"])
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Import from 110 kV Grid [MW]")
    plt.title("Active Power Import from Grid for Different PV Scenarios")
    plt.tight_layout()
    plt.savefig(f"{RESULTS_DIR}/static_grid_import.png", dpi=200)

    # Graph 3: Losses
    plt.figure()
    plt.bar(summary_df["scenario"], summary_df["total_losses_mw"])
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Total Losses [MW]")
    plt.title("Network Losses for Different PV Scenarios")
    plt.tight_layout()
    plt.savefig(f"{RESULTS_DIR}/static_losses.png", dpi=200)

    # Graph 4: Transformer loading
    plt.figure()
    plt.bar(summary_df["scenario"], summary_df["max_trafo_loading_percent"])
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Max Transformer Loading [%]")
    plt.title("Transformer Loading for Different Scenarios")
    plt.tight_layout()
    plt.savefig(f"{RESULTS_DIR}/static_trafo_loading.png", dpi=200)

        
        
        
if __name__ == "__main__":
    main()