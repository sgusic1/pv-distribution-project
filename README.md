# Techno-Economic and Load-Flow Analysis of a Solar Power Plant Integration into a 110/10/0.4 kV Distribution Network

## Project Description

This project analyzes the impact of connecting a photovoltaic (PV) power plant to a simplified distribution network with voltage levels of 110/10/0.4 kV.

The primary focus of the project is on power system analysis, utilizing Python as a tool for modeling, calculation and results visualization.

## Project Goal

The goal is to analyze how different PV power plant capacities affect:

- Voltage profiles,
- Active and reactive power flows,
- Network losses,
- Transformer loading,
- Power imports from the external 110 kV grid,
- Rough economic viability of the PV system.

## Network Model

The modeled network includes:

- A 110 kV external grid,
- A 110/10 kV transformer,
- A 10 kV busbar,
- A 10 kV line,
- A 10/0.4 kV transformer,
- A 0.4 kV busbar (Point of Common Coupling),
- A low-voltage consumer,
- A PV power plant connected to the 0.4 kV busbar.

## Analyzed Scenarios

The following scenarios were analyzed in the steady-state (static) analysis:

- S0: Without a PV power plant,
- S1: 100 kW PV power plant,
- S2: 300 kW PV power plant,
- S3: 500 kW PV power plant,
- S4: 500 kW PV power plant under low load conditions,
- S5: 500 kW PV power plant under peak load conditions.

## 24-Hour Simulation

In addition to the static scenarios, a simplified 24-hour simulation was conducted for the 300 kW PV power plant. Daily consumption and PV generation profiles were utilized to analyze variations in voltage, grid imports, losses and transformer loading throughout the day.

## Economic Analysis

A rough economic assessment was performed, which includes:

- Annual production of the PV system,
- Estimation of self-consumption,
- Annual savings,
- Capital expenditure (Investment cost),
- Simple payback period.

## Model Limitations

The model is simplified and does not constitute an official grid connection study. A real-world project would require actual distribution network data, detailed equipment parameters, voltage regulation mechanisms, protection devices, short-circuit analysis, harmonics, unbalance assessments and compliance with the grid operator's active technical grid codes.

## Conclusion

The results indicate that the PV power plant can reduce active power imports from the external grid and cover a portion of local consumption. Concurrently, higher PV capacities can increase the voltage at the point of common coupling, especially during periods of high generation and low consumption. Therefore, to select the optimal PV system capacity, it is essential to analyze voltage variations, power flows, losses and grid element loading.
