
import numpy as np
from becalib.layers import MaterialLayer
from becalib.translator import get_translator


# Dynamic Thermal Analysis #
def get_periodic_penetration_depth_list(
        layers: list[MaterialLayer],
        time_period:float=24
        ) -> np.ndarray:   
    """ list of periodic penetration depth δ in [m] layer by layer
    Args:
        layers (list[MaterialLayer]): ordered list of material layers interior to exterior
        time_period (float, optional): analysis period in [h]. Defaults to 24 h.

    Returns:
        np.ndarray: periodic penetration depths
    """
    
    periodic_penetration_depth_list= []
    time_in_seconds= time_period*3600

    for layer in layers:
        if layer.is_air is False:
            delta_layer= np.sqrt(
                (layer.thermal_conductivity*time_in_seconds)
                / (np.pi * layer.gross_density * layer.specific_heat_capacity)
                )
            periodic_penetration_depth_list.append(delta_layer)
        else:
            periodic_penetration_depth_list.append(None)

    
    return np.array(periodic_penetration_depth_list)


def get_xi_list(
    layers: list[MaterialLayer],
    periodic_penetration_depth_list:np.ndarray,
        ) -> np.ndarray:
    """list of ξ values = s/d thickness / periodic_penetration
        Dimensionless quantity
    Args:
        layers (list[MaterialLayer]): ordered list of material layers interior to exterior
        list of periodic penetration depth δ in [m] layer by layer

    Returns:
        np.ndarray:  ξ = s/d
    """

    xi_list=[]

    i=0

    for layer in layers:
        if layer.is_air is False:
            xi_i= layer.thickness / periodic_penetration_depth_list[i]
            xi_list.append(xi_i)
        else:
            xi_list.append(None)
        
        i +=1

    return np.array(xi_list)


def get_heat_transfer_matrix_layer_list(thermal_resistances:np.ndarray,
                                        xi_list:np.ndarray,
                                        periodic_penetration_depth_list:np.ndarray,
                                        thermal_conductivities:np.ndarray,
                                        ) -> list[np.ndarray]:
    """list of heat transfer matrix layer by layer

    Args:
        thermal_resistances (list[float]):array of all thermal resistances Layer by layer
        xi_list(list): list of ξ values = s/d
        periodic_penetration_depth_list(list):periodic penetration depth δ in [m] layer by layer
        thermal_conductivities(list): thermal conductivities "λ" lambda [W/mK] Layer by Layer 

    Returns:
        list[np.ndarray]: list of heat transfer matrix 
    """
        
    resistances= np.delete(thermal_resistances, 0)
    pp_depths = periodic_penetration_depth_list
    conduct_ies = thermal_conductivities

    ht_matrix_list: list[np.ndarray] = []  # zz : z matrix list
    for i in range(0, len(xi_list)):
        # z is a layer matrix 2X2 of complex values
        z = np.zeros((2, 2), dtype=np.complex128) 
    
        if   xi_list[i] is None:
            # air_layer
            z[0][0] = 1
            z[1][1] = z[0][0]
            z[0][1]= -resistances[i]
            z[1][0]=0

        else: 
            # material layer
            z[0][0] = complex(
                (np.cosh(xi_list[i]) * np.cos(xi_list[i])), 
                (np.sinh(xi_list[i]) * np.sin(xi_list[i]))
                )
            z[1][1] = z[0][0]

            z[0][1] = -(pp_depths[i] / (2 * conduct_ies[i])) * \
                complex(
                    (np.sinh(xi_list[i]) * np.cos(xi_list[i]) + np.cosh(xi_list[i]) * np.sin(xi_list[i])),
                    (np.cosh(xi_list[i]) * np.sin(xi_list[i]) - np.sinh(xi_list[i]) * np.cos(xi_list[i])),
                    )
            z[1][0] = -(conduct_ies[i] / (pp_depths[i])) * \
                complex(
                    (np.sinh(xi_list[i]) * np.cos(xi_list[i]) - np.cosh(xi_list[i]) * np.sin(xi_list[i])),
                    (np.sinh(xi_list[i]) * np.cos(xi_list[i]) + np.cosh(xi_list[i]) * np.sin(xi_list[i])),
                    )
        # add z to zz list
        ht_matrix_list.append(z)

    return ht_matrix_list


def get_heat_transfer_matrix_component(
        ht_matrix_list:list[np.ndarray],
        surface_thermal_resistance_int:float,
        surface_thermal_resistance_ext:float) -> np.ndarray:
    """heat transfer matrix f multi layers components
        Z = Z_i * Z_1 * Z_1 * Z_2 ... * Z_N-1 * Z_N * Z_e
    
    Args:
        ht_matrix_list(list): list of heat transfer matrix layer by layer
        surface_thermal_resistance_int(float): Internal surface resistances Rsi
        surface_thermal_resistance_ext(float): External surface resistances Rse

    Returns:
        np.ndarray: heat_transfer_matrix [Z]
    """

    htm = np.zeros((2, 2), dtype=np.complex128)
    htm = ht_matrix_list[-1]  # Z_N

    for i in range(1, len(ht_matrix_list)):  
        htm = htm.dot(ht_matrix_list[-1 - i])  # dot product or scalar product


    # heat transfer matrix interior surface layer
    Z_i = np.array(
        [
            [complex(1, 0), complex(-surface_thermal_resistance_int)],
            [complex(0, 0), complex(1, 0)],
        ],
        dtype=np.complex128,
    )

    ## heat transfer matrix exterior surface layer
    Z_e = np.array(
        [
            [complex(1, 0), complex(-surface_thermal_resistance_ext)],
            [complex(0, 0), complex(1, 0)],
        ],
        dtype=np.complex128,
    )

    htm = Z_e.dot(htm)# dot product or scalar product
    htm = htm.dot(Z_i)# dot product or scalar product

    return htm

def get_periodic_thermal_transmittance(heat_transfer_matrix_component) -> float:
    """periodic_thermal_transmittance component value \n
        Yie in W/m²K

    Args:
        heat_transfer_matrix_component(array): heat transfer matrix f multi layers components

    Returns:
        float: Yie in W/m²K
    """

    Z_12  = heat_transfer_matrix_component[0][1]

    mod_Z_12 = np.sqrt((Z_12.real) ** 2 + (Z_12.imag) ** 2) # modulo 

    Y_ie = 1/mod_Z_12

    return Y_ie


def get_decrement_factor(periodic_thermal_transmittance,
                        thermal_transmittance_component
                        ) -> float:
    """decrement_factor = Y_ie / u-value
    Args:
        periodic_thermal_transmittance(float)
        thermal_transmittance_component(float)

    Returns:
        float: decrement_factor [-]
    """
    return (
        periodic_thermal_transmittance / thermal_transmittance_component
    )

def get_time_shift(heat_transfer_matrix_component,
                   time_period) -> float:
    """time_shift

    Args:
        heat_transfer_matrix_component(np.ndarray):
        time_period(float):

    Returns:
        float: time_shift in [h]
    """

    htm = heat_transfer_matrix_component
    htm_12= htm[0][1]

    phase=(np.arctan2(htm_12.imag, htm_12.real)) * time_period / (2 * np.pi)

    return phase + time_period / 2


def get_thermal_admittance_int(heat_transfer_matrix_component) -> float:
    """thermal_admittance_int Y_ii in W/m²K
    Args:
        heat_transfer_matrix_component(np.ndarray):

    Returns:
        float: Y_ii in W/m²K

    """
    htm = heat_transfer_matrix_component

    Y_ii = -htm[0][0] / htm[0][1]
    Y_ii = np.sqrt((Y_ii.real) ** 2 + (Y_ii.imag) ** 2)  # the module

    return Y_ii


def get_thermal_admittance_ext(heat_transfer_matrix_component) -> float:
    """thermal_admittance_int Y_ee in W/m²K
    Args:
        heat_transfer_matrix_component(np.ndarray):

    Returns:
        float: Y_ee in W/m²K

    """

    htm = heat_transfer_matrix_component

    Y_ee = -htm[1][1] / htm[0][1]
    Y_ee = np.sqrt((Y_ee.real) ** 2 + (Y_ee.imag) ** 2)  # the module

    return Y_ee


def get_areal_heat_capacity_int(heat_transfer_matrix_component,
                                time_period:float) -> float:
    """interior areal heat capacity [kJ/m²K]
        k1 = P/ 2 pi |Y_22-Y_12|
    
    Args:
        heat_transfer_matrix_component(np.ndarray):
        time_period(float): in hours

    Returns:
        float: [kJ/m²K]
    """
    
    htm = heat_transfer_matrix_component
    return (
        (time_period * 3600)
        / (2 * np.pi)
        * np.sqrt(
            (((htm[0][0] - 1) / htm[0][1]).real) ** 2
            + (((htm[0][0] - 1) / htm[0][1]).imag) ** 2
        )
    ) / 1000  # kJ/m2 K


def get_areal_heat_capacity_ext(heat_transfer_matrix_component,
                                time_period) -> float:
    """exterior areal heat capacity  [kJ/m²K]
        k2 = P/ 2 pi |Y_11-Y_12|
    Args:
        heat_transfer_matrix_component(np.ndarray):
        time_period(float): in hours

    Returns:
        float: [kJ/m²K]
    """


    htm = heat_transfer_matrix_component
    return (
        (time_period * 3600)
        / (2 * np.pi)
        * np.sqrt(
            (((htm[1][1] - 1) / htm[0][1]).real) ** 2
            + (((htm[1][1] - 1) / htm[0][1]).imag) ** 2
        )
    ) / 1000  


def get_areal_heat_capacity_component(
        layers: list[MaterialLayer]) -> float:
    """component areal heat capacity in [kJ/m²K]
        areal heat capacity of all layers

    Args:
        layers (list[MaterialLayer]): ordered list of material layers interior to exterior

    Returns:
        float: [kJ/m²K]
    """

    areal_heat_capacity_list=[]

    for layer in layers:
        if layer.is_air is False:
            areal_heat_capacity_list.append(layer.gross_density*layer.thickness*layer.specific_heat_capacity)

        else:
            #TODO check if 0 is ok for air layer
            areal_heat_capacity_list.append(0)

    return np.sum(np.array(areal_heat_capacity_list))/1000


def get_time_constant(areal_heat_capacity_component,thermal_resistance_component)->float:
    """time_constant in h
    Args:
        areal_heat_capacity_component(float): component areal heat capacity in [kJ/m²K]
        thermal_resistance_component(float): Component thermal resistance R in [m²K/W]

    Returns:
        float: h
    """
    return areal_heat_capacity_component*thermal_resistance_component*1000/3600


def get_threshold_values_italian_dm_26_06_2009(
        time_shift:float,
        decrement_factor:float,
        language:str="en"):
    """threshold values in accordance with italian rule DM 26/06/2009 \n
        Possible scores: \n
            Excellent 5/5 \n
            Good 4/5 \n
            Medium 3/5 \n
            Sufficient 2/5 \n
            Poor 1/5 \n
            Impossible score

    Args:
        time_shift(float): in hours
        decrement_factor(float): [-]
        language(str): en, fr, etc

    Returns:
        str: score 
    """
    _=get_translator(language=language)

    if time_shift >12 and decrement_factor<0.15:
        return _("Excellent 5/5") 
    
    elif (10<time_shift <=12) and (0.15 <= decrement_factor<0.3):
        return _("Good 4/5")
    
    elif (8<time_shift <=10) and (0.3 <= decrement_factor<0.4):
        return _("Medium 3/5") 
    
    elif (6<time_shift <=8) and (0.4 <= decrement_factor<0.6):
        return _("Sufficient 2/5") 
    
    elif time_shift <=6 and (0.6 <= decrement_factor):
        return _("Poor 1/5") 
    else:
        return _("Impossible score") 
    

def get_mass_component(layers: list[MaterialLayer]) -> float:
    """component mass per square meters in kg/m²
    Args:
        layers (list[MaterialLayer]): ordered list of material layers interior to exterior

    Returns:
        float: component mass per square meters in [kg/m²]
    """
    mass_list = []
    for layer in layers:
        if layer.is_air is False:
            mass_list.append(layer.gross_density*layer.thickness)
        else:
            # if air add 0
            mass_list.append(0)

    return np.sum(np.array(mass_list))





