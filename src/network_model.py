import pandapower as pp

def create_network():
    """
    Simplified model of a 110/10/0.4 kV distirbution network.
    
    Structure:
    110 kV external grid (external network)
        -> 110/10 kV transformer
        -> 10 kV busbar
        -> 10 kV line (feeder)
        -> 10/0.4 kV transformer
        -> 0.4 kV consumer and PV power plant connection point (P0i - Point of Intersection)
    """
    
    net = pp.create_empty_network()
    
    # 1. Busbar
    bus_110 = pp.create_bus(
        net,
        vn_kv=110,
        name="B1 - 110 kV external grid"
    )
    
    bus_10_substation = pp.create_bus(
        net, 
        vn_kv=10,
        name="B2 - 10 kV substation busbar"
    )
    
    bus_10_feeder = pp.create_bus(
        net,
        vn_kv=10,
        name="B3 - 10 kV Line End"
    )
    
    bus_04 = pp.create_bus(
        net,
        vn_kv=0.4,
        name="B4 - 0.4 kV consumer and PV"
    )
    
    # 2. 110 kV external grid
    pp.create_ext_grid(
        net,
        bus=bus_110,
        vm_pu=1.02,
        name="110 kV external grid"
    )
    
    # 3. Transformer 110/10 kV
    pp.create_transformer_from_parameters(
        net,
        hv_bus=bus_110,
        lv_bus=bus_10_substation,
        sn_mva=25,
        vn_hv_kv=110,
        vn_lv_kv=10,
        vk_percent=10,
        vkr_percent=0.5,
        pfe_kw=25,
        i0_percent=0.1,
        name="TR1 110/10 kV 25 MVA"
    )
    
    # 4. 10 kv feeder
    pp.create_line_from_parameters(
        net,
        from_bus=bus_10_substation,
        to_bus=bus_10_feeder,
        length_km=5,
        r_ohm_per_km=0.32,
        x_ohm_per_km=0.35,
        c_nf_per_km=10,
        max_i_ka=0.3,
        name="10 kV feeder 5 km length"
    )
    
    # 5. Transformer 10/0.4 kV
    pp.create_transformer_from_parameters(
        net,
        hv_bus=bus_10_feeder,
        lv_bus=bus_04,
        sn_mva=0.63,
        vn_hv_kv=10,
        vn_lv_kv=0.4,
        vk_percent=6,
        vkr_percent=1.2,
        pfe_kw=1.2,
        i0_percent=0.3,
        name="TR2 10/0.4 kV 630 kVA"
    )
    
    # 6. Consumer 0.4 kV
    pp.create_load(
        net,
        bus=bus_04,
        p_mw=0.35,
        q_mvar=0.12,
        name="Low voltage consumer"
    )
    
    return net