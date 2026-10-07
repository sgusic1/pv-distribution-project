import os
import pandas as pd


RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)


def main():
    """
    Simplified Economic Analysis of a Solar PV System.
    Note:
    This is not an investment study.
    The goal is to roughly estimate annual production,
    annual savings, and the simple payback period.
    """
    
    pv_installed_kw = 300
    
    # Assumed annual production per 1 kW of installed capacity.
    # The value is simplified for the portfolio project.
    specific_yield_kwh_per_kw_year = 1200
    
    # Assumed electricity price.
    electricity_price_km_per_kwh = 0.18
    
    # Assumed investment cost per kW.
    investment_cost_km_per_kw = 1400
    
    # Assumption that 75% of PV energy is consumed locally.
    self_consumption_ratio = 0.75
    
    annual_generation_kwh = pv_installed_kw * specific_yield_kwh_per_kw_year
    self_consumed_energy_kwh = annual_generation_kwh * self_consumption_ratio
    annual_savings_km = self_consumed_energy_kwh * electricity_price_km_per_kwh
    investment_cost_km = pv_installed_kw * investment_cost_km_per_kw
    simple_payback_years = investment_cost_km / annual_savings_km
    
    df = pd.DataFrame([
        {
            "pv_installed_kw": pv_installed_kw,
            "specific_yield_kwh_per_kw_year": specific_yield_kwh_per_kw_year,
            "annual_generation_kwh": annual_generation_kwh,
            "self_consumption_ratio": self_consumption_ratio,
            "self_consumed_energy_kwh": self_consumed_energy_kwh,
            "electricity_price_km_per_kwh": electricity_price_km_per_kwh,
            "investment_cost_km": investment_cost_km,
            "annual_savings_km": annual_savings_km,
            "simple_payback_years": simple_payback_years,
        }
    ])
    
    
    df.to_csv(f"{RESULTS_DIR}/economic_summary.csv", index=False)

    print("\nROUGH ECONOMIC ANALYSIS:")
    print(df.T)



if __name__ == "__main__":
    main()
