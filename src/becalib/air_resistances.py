import numpy as np
def get_surface_resistances(heat_flow_direction:str)-> tuple:
    """Surface resistances Rsi (Internal)and Rse (external) 
        in accordance with ISO 6946:2007 in [mK/W]

    Args:
        heat_flow_direction (str): 
            "Ho": Horizontal (example: wall)
            "Up": Upwards (example Roof)
            "Do": Downwards (example floor)

    Returns:
        tuple: (Rsi, Rse) in [mK/W]
    """

    if heat_flow_direction== "Ho":
        return (0.13 , 0.04) # (Rsi, Rse)
    elif heat_flow_direction== "Up":
        return (0.10 , 0.04) #(Rsi, Rse)
    elif heat_flow_direction== "Do":
        return (0.17 , 0.04) #(Rsi, Rse)
    else:
        raise ValueError(f"""invalid string heat_flow_direction: {heat_flow_direction}
        available choices: Ho, Up ,Do
        """)


def get_resistance_unventilated_air_layer(
        heat_flow_direction:str,
        thickness:float=0
        )->float:
    """ Thermal resistance of unventilated air layers 
        with high emissivity surfaces 
        in accordance with ISO 6946:2007 in [mK/W]
    Args:
        thickness (float): in meters
        heat_flow_direction (str): 
            "Ho": Horizontal (example: wall)
            "Up": Upwards (example Roof)
            "Do": Downwards (example floor)

    Returns:
        float: Thermal Resistance in [mK/W]
    """
    thicknesses = [0,
                   5*10**-3, #0.005 m or 5 mm
                   7*10**-3,
                   10*10**-3,
                   15*10**-3,
                   25*10**-3,
                   50*10**-3,
                   100*10**-3,
                   300*10**-3]  
    up_r_values =[0,
                  0.11,
                  0.13,
                  0.15,
                  0.16,
                  0.16,
                  0.16,
                  0.16,
                  0.16] 
    ho_r_values =[0,
                  0.11,
                  0.13,
                  0.15,
                  0.17,
                  0.18,
                  0.18,
                  0.18,
                  0.18]
    do_r_values =[0,
                  0.11,
                  0.13,
                  0.15,
                  0.17,
                  0.19,
                  0.21,
                  0.22,
                  0.23]
    
    if heat_flow_direction == "Ho":
        return np.interp(thickness, thicknesses, ho_r_values)
    elif heat_flow_direction == "Up":
        return np.interp(thickness, thicknesses, up_r_values)
    elif heat_flow_direction == "Do":
        return np.interp(thickness, thicknesses, do_r_values)
    else:
        raise ValueError(f"""invalid string heat_flow_direction: {heat_flow_direction}
        available choices: Ho, Up ,Do
        """)
