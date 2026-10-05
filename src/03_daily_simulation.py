import os
import pandas as pd
import pandapower as pp
import matplotlib.pyplot as plt

from network_model import create_network


RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)


def load_multiplier(hour):
    """
    Simplified 24-hour load profile with morning and evening peaks.
    """
    
    profile = {
        0: 0.45,
        1: 0.40,
        2: 0.38,
        3: 0.38,
        4: 0.40,
        5: 0.45,
        6: 0.60,
        7: 0.75,
        8: 0.85,
        9: 0.90,
        10: 0.95,
        11: 1.00,
        12: 1.00,
        13: 0.95,
        14: 0.90,
        15: 0.90,
        16: 0.95,
        17: 1.05,
        18: 1.10,
        19: 1.15,
        20: 1.05,
        21: 0.90,
        22: 0.70,
        23: 0.55,
    }
    
    return profile[hour]


def pv_multiplier(hour):
    """
    Simplified daily PV generation profile.
    No generation at night, maximum output around noon.
    """
    
    profile = {
        0: 0.00,
        1: 0.00,
        2: 0.00,
        3: 0.00,
        4: 0.00,
        5: 0.00,
        6: 0.05,
        7: 0.15,
        8: 0.35,
        9: 0.55,
        10: 0.75,
        11: 0.90,
        12: 1.00,
        13: 0.95,
        14: 0.80,
        15: 0.60,
        16: 0.35,
        17: 0.15,
        18: 0.03,
        19: 0.00,
        20: 0.00,
        21: 0.00,
        22: 0.00,
        23: 0.00,
    }
    
    return profile[hour]


def run_hour(hour, pv_installed_mw, base_load_mw, base_load_q_mvar):
    net = create_network()
    load_p_mw = base_load_mw * load_multiplier(hour)
    load_q_mvar = base_load_q_mvar * load_multiplier(hour)
    pv_p_mw = pv_installed_mw * pv_multiplier(hour)

    net.load.loc[0, "p_mw"] = load_p_mw
    net.load.loc[0, "q_mvar"] = load_q_mvar
    
    lv_bus = net.bus.index[net.bus["name"] == "B4 - 0.4 kV consumer and PV"][0]

    if pv_p_mw > 0:
        pp.create_sgen(
            net,
            bus=lv_bus,
            p_mw=pv_p_mw,
            q_mvar=0.0,
            name="PV elektrana"
        )
        
    pp.runpp(net, numba=False)

    total_losses_mw = net.res_line["pl_mw"].sum() + net.res_trafo["pl_mw"].sum()

    return {
        "hour": hour,
        "load_mw": load_p_mw,
        "pv_generation_mw": pv_p_mw,
        "voltage_04_bus_pu": net.res_bus.loc[lv_bus, "vm_pu"],
        "grid_import_mw": net.res_ext_grid["p_mw"].sum(),
        "total_losses_mw": total_losses_mw,
        "max_trafo_loading_percent": net.res_trafo["loading_percent"].max(),
    }
    
    
def main():
    rows = []

    pv_installed_mw = 0.30
    base_load_mw = 0.35
    base_load_q_mvar = 0.12

    for hour in range(24):
        row = run_hour(
            hour=hour,
            pv_installed_mw=pv_installed_mw,
            base_load_mw=base_load_mw,
            base_load_q_mvar=base_load_q_mvar,
        )
        rows.append(row)

    df = pd.DataFrame(rows)

    df.to_csv(f"{RESULTS_DIR}/daily_simulation_300kw_pv.csv", index=False)

    print("\n24-HOUR SIMULATION FOR 300 kW PV:")
    print(df.to_string(index=False))

    # Graph 1: Demand and PV Generation
    plt.figure(figsize=(10, 5)) # Wider figure looks much better with 24 tick marks
    plt.plot(df["hour"], df["load_mw"], marker="o", label="Demand (Load)")
    plt.plot(df["hour"], df["pv_generation_mw"], marker="o", label="PV Generation")
    plt.xticks(range(24)) # Forces grid lines for all hours
    plt.xlabel("Hour of Day")
    plt.ylabel("Power [MW]")
    plt.title("Daily Demand and PV Generation Profiles")
    plt.legend()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5) # Clean dashed lines
    plt.tight_layout()
    plt.savefig(f"{RESULTS_DIR}/daily_load_pv_profile.png", dpi=200)

    # Graph 2: Voltage Profile
    plt.figure(figsize=(10, 5))
    plt.plot(df["hour"], df["voltage_04_bus_pu"], marker="o", color="g")
    plt.xticks(range(24))
    plt.xlabel("Hour of Day")
    plt.ylabel("0.4 kV Busbar Voltage [p.u.]")
    plt.title("Daily Voltage Profile at PV Connection Point")
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.savefig(f"{RESULTS_DIR}/daily_voltage_profile.png", dpi=200)

    # Graph 3: Grid Import
    plt.figure(figsize=(10, 5))
    plt.plot(df["hour"], df["grid_import_mw"], marker="o", color="r")
    plt.xticks(range(24))
    plt.xlabel("Hour of Day")
    plt.ylabel("Import from 110 kV Grid [MW]")
    plt.title("Daily Active Power Import from Grid")
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.savefig(f"{RESULTS_DIR}/daily_grid_import.png", dpi=200)

    # Graph 4: Network Losses
    plt.figure(figsize=(10, 5))
    plt.plot(df["hour"], df["total_losses_mw"], marker="o", color="m")
    plt.xticks(range(24))
    plt.xlabel("Hour of Day")
    plt.ylabel("Total Losses [MW]")
    plt.title("Daily Network Power Losses")
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.savefig(f"{RESULTS_DIR}/daily_losses.png", dpi=200)

    # Graph 5: Transformer Loading
    plt.figure(figsize=(10, 5))
    plt.plot(df["hour"], df["max_trafo_loading_percent"], marker="o", color="b")
    plt.xticks(range(24))
    plt.xlabel("Hour of Day")
    plt.ylabel("Max Transformer Loading [%]")
    plt.title("Daily Maximum Transformer Loading Profile")
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.savefig(f"{RESULTS_DIR}/daily_trafo_loading.png", dpi=200)


if __name__ == "__main__":
    main()
