import numpy as np
from becalib.air_resistances import get_resistance_unventilated_air_layer
from becalib.translator import get_translator


class LayerBase():
    """common layer parameter of materials and air layers
    """
    def __init__(self, 
        name:str,
        thickness:float, # m
        is_air:bool =False,
        language:str="en"
                 ):
        """input parameters

        Args:
            name (str): name of layer
            thickness (float): "d" in m thickness of layer
        """
        
        self.name = name
        if not type(thickness)  is float:
            raise ValueError("thickness: have to be à float type")
        
        self.thickness= thickness # m
        self.is_air= is_air
        self.language=language


class MaterialLayer(LayerBase):
    """Material Layer 
    Args:
        LayerBase (Class): inheritance of parameters from LayerBase class
    """
    def __init__(self,
        name:str,
        thickness:float, # m
        thermal_conductivity:float, 
        gross_density:float,
        specific_heat_capacity:float,
        is_air:bool =False,
        language:str="en" 

        ):
        
        """Material Layer input parameters

        Args:
            name (str): 
            thickness (float):  "d" in m thickness of layer
            thermal_conductivity (float): "λ" lambda [W/mK]
            gross_density (float): "ρ" rho [kg/mc]
            specific_heat_capacity (float): "c" [J/kgK]
            is_air (bool, optional): Defaults to False
            language (str, optional): Defaults to "en". 
        """

        super().__init__(name,
                      thickness,
                      is_air,
                      language)



        self.thermal_conductivity= thermal_conductivity  # λ [W/mK]
        self.gross_density =gross_density # ro [kg/m³]
        self.specific_heat_capacity= specific_heat_capacity  # c [J/kgK]   
    
    

    @property
    def thermal_resistance(self):
        """R in m²K/W
        Returns:
            float: Thermal resistance d/λ
        """

        return self.thickness / self.thermal_conductivity
    
    
    @property
    def thermal_diffusivity(self):
        """alpha = lambda/(ro * c)  in [m²/ (s*10^6)]
        Returns:
            float: [m²/ (s*10^6)]
        """
        return (self.thermal_conductivity/self.specific_heat_capacity/self.gross_density)*10**6
    

    @property
    def thermal_effusivity(self):
        """thermal_effusivity

        Returns:
            float: thermal_effusivity
        """
        return np.sqrt(self.thermal_conductivity*self.specific_heat_capacity*self.gross_density)



    def get_values(self):
        _=get_translator(self.language)

        layer_values_str=_("Layer values")
        input_str=_("INPUTS:")
        thickness_str= _("Thickness")
        thermal_conductivity_str=_("Thermal conductivity λ")
        gross_density_str=_("Gross density ρ")
        specific_heat_capacity_str=_("Specific heat capacity c")
        output_str= _("OUTPUTS:")

        thermal_resistance_str=_("Thermal resistance R")
        thermal_diffusivity_str=_("Thermal diffusivity α")
        thermal_effusivity_str=_("Thermal effusivity")
        return \
f"""{self.name}: 

{thickness_str} : {self.thickness:0.3f} [m]
{thermal_conductivity_str} : {self.thermal_conductivity:0.3f} [W/mK]
{gross_density_str} : {self.gross_density:0.0f} [kg/mc]
{specific_heat_capacity_str} : {self.specific_heat_capacity:0.0f} [J/kgK]
{thermal_resistance_str} : {self.thermal_resistance:0.3f} [m²K/W]
{thermal_diffusivity_str} : {self.thermal_diffusivity:0.3f} [m²/ (s*10^6)]
{thermal_effusivity_str} : {self.thermal_effusivity:0.1f}"""


class AirLayer(LayerBase):
    def __init__(self,
        name:str,
        thickness:float,
        heat_flow_direction:str="Ho",
        is_air:bool =True,   
        language:str="en"     

        ):
        """ AirLayer non-ventilated 
        Args:
            name (str): 
            thickness (float):  "d" in m thickness of layer 
            heat_flow_direction (str):  "Ho": Horizontal (example: wall)
                                        "Up": Upwards (example Roof)
                                        "Do": Downwards (example floor)
            is_air (bool, optional): Defaults to True
            language (str, optional): Defaults to "en". 
        """
        super().__init__(name,
                      thickness,
                      is_air,
                      language)

        self.heat_flow_direction= heat_flow_direction
        self.is_air=True
        

    @property
    def thermal_resistance(self):
        """R of air layer in m²K/W
        Returns:
            float: 
        """
        return get_resistance_unventilated_air_layer(
            thickness=self.thickness,
            heat_flow_direction=self.heat_flow_direction)
    

    @property
    def thermal_conductivity(self):
        "lambda W/mK"
        return self.thickness/self.thermal_resistance
    


    def get_values(self):
        _=get_translator(self.language)

        layer_values_str=_("Layer values")

        input_str=_("INPUTS:")

        thickness_str= _("Thickness")
        thermal_conductivity_str=_("Thermal conductivity λ")
        heat_flow_direction_str=_("Heat flow direction")

        output_str= _("OUTPUTS:")

        thermal_resistance_str=_("Thermal resistance R")


        return \
f"""{self.name}:

{thickness_str} : {self.thickness:0.3f} [m]
{thermal_conductivity_str} : {self.thermal_conductivity:0.3f} [W/mK]
{heat_flow_direction_str} : {self.heat_flow_direction} "Ho": Horizontal (wall),"Up": Upwards (Roof),"Do": Downwards (floor)
{thermal_resistance_str} : {self.thermal_resistance:0.3f} m²K/W"""