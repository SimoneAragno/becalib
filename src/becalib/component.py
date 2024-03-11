import numpy as np
import pandas as pd
from becalib.charts import plot_component_layers, plot_sinusoidal_wave
from becalib.layers import MaterialLayer
from becalib.air_resistances import get_surface_resistances
from becalib.translator import get_translator
from becalib.algos import *
import copy


class Component():
    def __init__(self,
        name: str,
        layers: list[MaterialLayer],
        heat_flow_direction:str,
        time_period: float = 24, 
        language: str= "en"
        ):
        """Summer analysis of multi layer component like wall, roof or floor

        Args:
            name (str): component name \n
            layers (list[MaterialLayer]): ordered list of material layers interior to exterior\n
            heat_flow_direction (str): \n
                                        "Ho": Horizontal (example: wall)\n
                                        "Up": Upwards (example Roof)\n
                                        "Do": Downwards (example floor)\n
            time_period (float, optional): analysis period in [h]. Defaults to 24 h.\n

        """
        self.name=name
        self.layers=layers
        self.heat_flow_direction=heat_flow_direction
        self.time_period=time_period
        self.language=language
        
        # Compute all values
        self.update()
    
    def _set_parameter_names_strings(self):
        """set all string needed to print values labels in different languages
        """
        _=get_translator(self.language)

        self.component_str=_("Component")
        self.heat_flow_direction_str=_("Heat flow direction")
        self.time_period_str = _("Time period")

        self.surface_thermal_resistance_int_str=_("Interior surface thermal resistance Rsi")
        self.surface_thermal_resistance_ext_str=_("Exterior surface thermal resistance Rse")
        self.thickness_component_str=_("Thickness")
        self.thermal_resistance_component_str=_("Resistance")
        self.thermal_transmittance_component_str= _("Transmittance")
        self.periodic_thermal_transmittance_str = _("Periodic transmittance")
        self.decrement_factor_str=_("Decrement factor")
        self.time_shift_str=_("Time shift")
        self.thermal_admittance_int_str=_("Interior admittance")
        self.thermal_admittance_ext_str=_("Exterior admittance")
        self.areal_heat_capacity_int_str=_("Interior areal heat capacity")
        self.areal_heat_capacity_ext_str=_("Exterior areal heat capacity")
        self.areal_heat_capacity_str=_("Areal heat capacity")

        self.mass_component_str= _("Surface mass")

        self.threshold_values_italian_dm_26_06_2009_str=_("Summer performance")

    def update(self):
        """Compute all values with last inputs
        """
        # Surface resistances Rsi (Internal)and Rse (external)
        (self.surface_thermal_resistance_int,
        self.surface_thermal_resistance_ext)=get_surface_resistances(
                                                heat_flow_direction=self.heat_flow_direction)
        
        self._set_parameter_names_strings()

        # Override heat_flow_direction for air layers
        list_of_layers= []
        for layer in self.layers:
            if layer.is_air is True:
                layer.heat_flow_direction = self.heat_flow_direction
                list_of_layers.append(layer)
            else:
                list_of_layers.append(layer)
        
        self.layers = list_of_layers

        # np.array of thickness of each Layer
        self.thicknesses= np.array([layer.thickness for layer in self.layers])

        # sum of thicknesses of all layers in [m]
        self.thickness_component= np.sum(self.thicknesses,)

        # array of thermal conductivities "λ" lambda [W/mK] Layer by Layer 
        self.thermal_conductivities= np.array([layer.thermal_conductivity for layer in self.layers])

        # array of gross densities "ρ" rho [kg/mc] Layer by Layer  
        densities_list = []
        for layer in self.layers:
            if layer.is_air is False:
                densities_list.append(layer.gross_density)
            else:
                densities_list.append(None)
        self.gross_densities= np.array(densities_list)

        # array of Specific heat capacities "c" [J/kgK] Layer by layer
        specific_heats_list=[]
        for layer in self.layers:
            if layer.is_air is False:
                specific_heats_list.append(layer.specific_heat_capacity)
            else:
                specific_heats_list.append(None)

        self.specific_heat_capacities= np.array(specific_heats_list)

        ##  Steady-State Thermal Analysis ##

        # thermal_resistances
        # array of all thermal resistances Layer by layer
        # including internal and external surface thermal resistances
        resistances = np.array([layer.thermal_resistance for layer in self.layers])
        resistances = np.insert(resistances, 0, self.surface_thermal_resistance_int)
        resistances = np.append(resistances, self.surface_thermal_resistance_ext)

        self.thermal_resistances= resistances

        # Component thermal resistance R in [m²K/W]
        # sum of layer resistances including internal 
        # and external resistances
        self.thermal_resistance_component = np.sum(self.thermal_resistances)


        #thermal_transmittance_component U-value in  W/m²K)
        self.thermal_transmittance_component= 1 / self.thermal_resistance_component
    
    
        ###  Dynamic Thermal Analysis ###

        # periodic_penetration_depth
        self._periodic_penetration_depth_list=get_periodic_penetration_depth_list(layers= self.layers,
                                            time_period= self.time_period
                                            )
        # XI
        self._xi_list=get_xi_list(layers=self.layers,
                                  periodic_penetration_depth_list= self._periodic_penetration_depth_list
                                  
        )
        # heat_transfer_matrix layer by layer
        self._heat_transfer_matrix_layer_list = \
            get_heat_transfer_matrix_layer_list(
                thermal_resistances=self.thermal_resistances,
                xi_list=self._xi_list,
                periodic_penetration_depth_list=self._periodic_penetration_depth_list,
                thermal_conductivities=self.thermal_conductivities)
        
        # heat_transfer_matrix component
        self._heat_transfer_matrix_component = \
            get_heat_transfer_matrix_component(
                ht_matrix_list= self._heat_transfer_matrix_layer_list,
                surface_thermal_resistance_int=self.surface_thermal_resistance_int,
                surface_thermal_resistance_ext=self.surface_thermal_resistance_ext) 
        
        # periodic_thermal_transmittance
        self.periodic_thermal_transmittance= \
            get_periodic_thermal_transmittance(heat_transfer_matrix_component=self._heat_transfer_matrix_component)
        
        # decrement_factor
        self.decrement_factor=get_decrement_factor(
            periodic_thermal_transmittance= self.periodic_thermal_transmittance,
            thermal_transmittance_component= self.thermal_transmittance_component)
        
        # time_shift
        self.time_shift=get_time_shift(
            heat_transfer_matrix_component=self._heat_transfer_matrix_component,
            time_period=self.time_period)
        
        # thermal_admittance_int
        self.thermal_admittance_int= get_thermal_admittance_int(self._heat_transfer_matrix_component) 
        # thermal_admittance_ext
        self.thermal_admittance_ext= get_thermal_admittance_ext(self._heat_transfer_matrix_component) 

        # areal_heat_capacity_int
        self.areal_heat_capacity_int= get_areal_heat_capacity_int(
            self._heat_transfer_matrix_component,
            self.time_period )        
        # areal_heat_capacity_ext        
        self.areal_heat_capacity_ext= get_areal_heat_capacity_ext(
            self._heat_transfer_matrix_component,
            self.time_period)
        # areal_heat_capacity_component
        self.areal_heat_capacity_component=\
            get_areal_heat_capacity_component(self.layers)
        
        # time_constant
        self.time_constant= get_time_constant(
            self.areal_heat_capacity_component, 
            self.thermal_resistance_component)
        
        # threshold_values_italian_dm_26_06_2009
        self.threshold_values_italian_dm_26_06_2009=\
            get_threshold_values_italian_dm_26_06_2009(
                self.time_shift,
                self.decrement_factor,
                self.language
            )
        
        # mass_component        
        self.mass_component=get_mass_component(self.layers)

    # Methods to get computed values by strings, DataFrames or charts
    def get_layers_dataframe(self,
            data_type:str="st"):
        """get pandas dataframe or styler objet (for notebooks) of layers

        Args:
            data_type (str, optional): _description_. Defaults to "st"=styler objet or "df"=dataframe

        Returns:
            object: pandas dataframe or styler
        """

        list_of_layers_dict=[]

        _=get_translator(language=self.language)

        list_of_layers_dict.append({"name":_("Interior surface"),
                                    "thermal_resistance":self.surface_thermal_resistance_int}
                                    )
        for layer in self.layers:
            layer_dict= {}

            if layer.is_air==False:
                dict_of_computed_values= {"thermal_resistance":layer.thermal_resistance,
                                   "thermal_diffusivity":layer.thermal_diffusivity,
                                   "thermal_effusivity":layer.thermal_effusivity
                                   }

                layer_dict=dict(copy.copy(layer.__dict__))


                layer_dict.pop("language")
                layer_dict.update(dict_of_computed_values)

            if layer.is_air==True:
                
                dict_of_computed_values= {"thermal_resistance":layer.thermal_resistance}
                layer_dict=dict(copy.copy(layer.__dict__))

                layer_dict.pop("heat_flow_direction")
                
                layer_dict.update(dict_of_computed_values)


            list_of_layers_dict.append(layer_dict)
        
        list_of_layers_dict.append({"name":_("Exterior surface"),
                                    "thermal_resistance":self.surface_thermal_resistance_ext}
                                    )
        
        df=pd.DataFrame(list_of_layers_dict)

        df=df.reindex(columns=[
            'name',
            'thickness',
            'thermal_conductivity',
            "thermal_resistance",
            'is_air',
            "gross_density",
            "specific_heat_capacity",
            
            "thermal_diffusivity",
            "thermal_effusivity"
        ])
    
        df = df.rename(columns=
                {'name': _('Name'),
                'thickness': _("Thickness [m]"),
                'is_air': _('is_air'),
                'thermal_conductivity': _('Conductivity λ [W/mK]'),
                "gross_density":_("Gross density ρ [kg/m³]"),
                "specific_heat_capacity":_("Specific heat capacity c [J/kgK]"),
                "thermal_resistance":_("Resistance R [m²K/W]"),
                "thermal_diffusivity":_("Diffusivity α [m²/ (s*10^6)]"),
                "thermal_effusivity":_("Effusivity")

                })
        
        style_object=df.style.format(
            {_("Thickness [m]"): '{:.2f}', 
            _('Conductivity λ [W/mK]'): '{:.3f}',
            _("Gross density ρ [kg/m³]"): '{:.0f}',
            _("Specific heat capacity c [J/kgK]"): '{:.0f}',
            _("Resistance R [m²K/W]"): '{:.3f}',
            _("Diffusivity α [m²/ (s*10^6)]"): '{:.3f}',
            _("Effusivity"): '{:.1f}',
            }, 
            na_rep='', precision=1)
        
        if data_type=="st":
            return style_object
        else:
            return df
    
    def _get_layers_data_string(self)->str:
        """get string of data layer by layer

        Returns:
            str: layers data
        """

        _=get_translator(self.language)

        #list of layer data
        out_layers_str=_("Layers:")
        out_layers_str=out_layers_str+"\n"+ "-----------------------"+"\n"+_("Interior")
        for layer in self.layers:
            out_layers_str=out_layers_str+ "\n"+"-----------------------"
            layer.language= self.language
            out_layers_str=out_layers_str+ "\n" + layer.get_values()
        out_layers_str=out_layers_str+"\n"+ "-----------------------"+"\n"+ _("Exterior")+"\n"+ "-----------------------"

        return out_layers_str

    def get_values(self):
        """get string of all inputs and output values
        """
        return \
f"""#######################################
{self.component_str}: {self.name}

{self.heat_flow_direction_str}: {self.heat_flow_direction} (|"Ho": Horizontal (wall) |"Up": Upwards (Roof) | "Do": Downwards (floor))
{self.time_period_str}: {self.time_period} [h]

{self.surface_thermal_resistance_int_str}: {self.surface_thermal_resistance_int} [m²K/W]
{self.surface_thermal_resistance_ext_str}: {self.surface_thermal_resistance_ext} [m²K/W]

{self.thickness_component_str}: {self.thickness_component:.3f} [m]
{self.thermal_resistance_component_str}: {self.thermal_resistance_component:.3f} [m²K/W] Rsi and Rse included
{self.thermal_transmittance_component_str}: {self.thermal_transmittance_component:.3f} [W/m²K]

{self.periodic_thermal_transmittance_str}: {self.periodic_thermal_transmittance:.3f} [W/m²K]
{self.decrement_factor_str}: {self.decrement_factor:.3f} [-]
{self.time_shift_str}: {self.time_shift:.1f} [h]

{self.thermal_admittance_int_str}: {self.thermal_admittance_int:.3f} [W/m²K]
{self.thermal_admittance_ext_str}: {self.thermal_admittance_ext:.3f} [W/m²K]

{self.areal_heat_capacity_int_str}: {self.areal_heat_capacity_int:.3f} [kJ/m²K] 
{self.areal_heat_capacity_ext_str}: {self.areal_heat_capacity_ext:.3f} [kJ/m²K]

{self.areal_heat_capacity_str}: {self.areal_heat_capacity_component:.3f} [kJ/m²K]

{self.threshold_values_italian_dm_26_06_2009_str}: {self.threshold_values_italian_dm_26_06_2009} (in accordance with italian DM 26/06/2009)
{self.mass_component_str}: {self.mass_component:.1f} [kg/m²]

{self._get_layers_data_string()}
#######################################"""

    def get_summer_performance_key_values(self):
        """get string of component key values inputs and output
        """
        return \
f"""#######################################
{self.component_str}: {self.name}

{self.time_period_str}: {self.time_period} [h]

{self.thickness_component_str}: {self.thickness_component:.3f} [m]
{self.thermal_resistance_component_str}: {self.thermal_resistance_component:.3f} [m²K/W] Rsi and Rse included
{self.thermal_transmittance_component_str}: {self.thermal_transmittance_component:.3f} [W/m²K]

{self.decrement_factor_str}: {self.decrement_factor:.3f} [-]
{self.time_shift_str}: {self.time_shift:.1f} [h]

{self.areal_heat_capacity_int_str}: {self.areal_heat_capacity_int:.3f} [kJ/m²K] 

{self.threshold_values_italian_dm_26_06_2009_str}: {self.threshold_values_italian_dm_26_06_2009} (in accordance with italian DM 26/06/2009)
{self.mass_component_str}: {self.mass_component:.1f} [kg/m²]

#######################################"""

    def get_component_layers_chart(self):
        """get a matplotlib pyplot object of component layers
        Returns:
            pyplot: matplotlib pyplot object
        """       
        layer_names= np.array([layer.name for layer in self.layers])     
        return plot_component_layers(
                        names=layer_names,
                        thickness=self.thicknesses,
                        heat_flow_direction=self.heat_flow_direction,
                        language=self.language
                        )
    def get_component_sinusoidal_wave_chart(self,
            max_temp:float = 35, 
            min_temp:float = 28,):
        """sinusoidal waves matplotlib pyplot object of time_shift and decrement_factor

        Args:
            max_temp (float, optional): Max temperature. Defaults to 35°C.
            min_temp (float, optional): Min temperature. Defaults to 28°C.

        Returns:
            matplotlib pyplot object: sinusoidal waves
        """

        return plot_sinusoidal_wave(
            decrement_factor= self.decrement_factor, 
            time_shift=self.time_shift,
            time_period=self.time_period,
            max_temp=max_temp, 
            min_temp=min_temp, 
            language=self.language
                )