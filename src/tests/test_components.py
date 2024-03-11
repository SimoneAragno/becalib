import unittest
from becalib.layers import MaterialLayer, AirLayer
from becalib.component import Component
import math
import pandas as pd

#plt.style.use(["science", "retro", "no-latex"])


class TestSummerWallPerformance(unittest.TestCase):

    def test_layer(self):
        """check layer computed values  thermal_diffusivity and thermal_effusivity
        """
        plaster = MaterialLayer(
        name="Plaster",
        thickness=0.15, 
        thermal_conductivity=0.21, 
        gross_density=1150, 
        specific_heat_capacity=1100, 
        )

        self.assertTrue(math.isclose(0.166,plaster.thermal_diffusivity,rel_tol=0.01))
        self.assertTrue(math.isclose(515.41,plaster.thermal_effusivity,rel_tol=0.01))
    
    def test_layer_get_values_fr(self):
        """check layer en->fr translation
        """

        plaster = MaterialLayer(
        name="Plaster",
        thickness=0.15, # m
        thermal_conductivity=0.21, # # W/mK W/mK
        gross_density=1150, # ro kg/mc
        specific_heat_capacity=1100, #  c J/kgK ,3,
        language="fr"
        )

        out_str=plaster.get_values()
        self.assertEqual("Épaisseur : 0.150 [m]",out_str.splitlines()[2])

    def test_air_layer_get_values_fr(self):
        """check air layer en->fr translation
        """

        air_gap = AirLayer(
        name="air_gap",
        thickness=0.19, # m
        heat_flow_direction="Up",
        language="fr"
        )

        out_str=air_gap.get_values()
        self.assertEqual("Conductivité thermique λ : 1.188 [W/mK]",out_str.splitlines()[3])


    def test_wall_get_values_fr(self):
        """check Component get_value method en->fr translation
        """       
        plasterboard = MaterialLayer(
            name="PLACOPLATRE",
            thickness=0.015,
            thermal_conductivity=0.21,
            gross_density=1150,
            specific_heat_capacity=1100,
        )
        clt_panel = MaterialLayer(
            name="Panneau CLT",
            thickness=0.096,
            thermal_conductivity=0.13,
            gross_density=500.0,
            specific_heat_capacity=1600,
        )
        air_gap= AirLayer(
            name= "lame d'air", 
            thickness=0.05,
        )
        insulation = MaterialLayer(
            name="isolant haute densité",
            thickness=0.13,
            thermal_conductivity=0.043,
            gross_density=190,
            specific_heat_capacity=2100,
        )
        plaster = MaterialLayer(
            name="Enduit",
            thickness=0.015,
            thermal_conductivity=0.9,
            gross_density=1800,
            specific_heat_capacity=1000,
        )

        wall_3c = Component(name="Wall_3c", 
                            layers=[plasterboard, 
                                    clt_panel, 
                                    insulation, 
                                    air_gap,
                                    plaster],
                            heat_flow_direction="Ho", 
                            language="fr")

        # print(wall_3c.get_values())

        df=wall_3c.get_layers_dataframe()


    def test_wall_values(self):    

        concrete  =  MaterialLayer(
            name="concrete",
            thickness=0.3, # m
            thermal_conductivity=1.8, # W/mK W/mK
            specific_heat_capacity=1000, #  c J/kgK            
            gross_density=2400, # ro kg/mc
        )

        insulation_a  =  MaterialLayer(
            name="insulation_a",
            thickness=0.1, # m
            thermal_conductivity=0.034, # W/mK W/mK
            specific_heat_capacity=700, #  c J/kgK            
            gross_density=70, # ro kg/mc
        )



        brick_a  =  MaterialLayer(
            name="brick_a",
            thickness=0.08, # m
            thermal_conductivity=0.35, # W/mK W/mK
            specific_heat_capacity=840, #  c J/kgK            
            gross_density=750, # ro kg/mc
        )

        brick_b  =  MaterialLayer(
            name="brick_b",
            thickness=0.12, # m
            thermal_conductivity=0.8, # W/mK W/mK
            specific_heat_capacity=840, #  c J/kgK            
            gross_density=1800, # ro kg/mc
        )

        plaster  =  MaterialLayer(
            name="plaster",
            thickness=0.02, # m
            thermal_conductivity=0.9, # W/mK W/mK
            specific_heat_capacity=840, #  c J/kgK            
            gross_density=1400, # ro kg/mc
        )


        wall = Component(name="Wall Test", 
                        layers=[
                        concrete,
                        insulation_a,
                        brick_a,
                        brick_b,
                        plaster ],
                        heat_flow_direction="Ho",
                        language="en"
                        )
        

        approx_rel_tot= 0.001

        self.assertTrue(math.isclose(0.62,wall.thickness_component,rel_tol=approx_rel_tot))
        self.assertTrue(math.isclose(0.03239,wall.decrement_factor,rel_tol=approx_rel_tot))
        self.assertTrue(math.isclose(17.854,wall.time_shift,rel_tol=approx_rel_tot))
        self.assertTrue(math.isclose(0.008804,wall.periodic_thermal_transmittance,rel_tol=approx_rel_tot))
        self.assertTrue(math.isclose(5.7303,wall.thermal_admittance_int,rel_tol=approx_rel_tot))
        self.assertTrue(math.isclose(7.7158,wall.thermal_admittance_ext,rel_tol=approx_rel_tot))
        self.assertTrue(math.isclose(78.7761,wall.areal_heat_capacity_int,rel_tol=approx_rel_tot))
        self.assertTrue(math.isclose(106.035,wall.areal_heat_capacity_ext,rel_tol=approx_rel_tot))
        self.assertTrue(math.isclose(1031,wall.mass_component,rel_tol=approx_rel_tot))

        self.assertTrue(math.isclose(3.679,wall.thermal_resistance_component,rel_tol=approx_rel_tot))
        self.assertTrue(math.isclose(0.272,wall.thermal_transmittance_component,rel_tol=approx_rel_tot))

        self.assertTrue(math.isclose(980,wall.areal_heat_capacity_component,rel_tol=approx_rel_tot))
        self.assertTrue(math.isclose(1002,wall.time_constant,rel_tol=approx_rel_tot))

        self.assertEqual("Excellent 5/5",wall.threshold_values_italian_dm_26_06_2009)

    def test_wall_values_2(self):    

        concrete  =  MaterialLayer(
            name="concrete",
            thickness=0.1, # m
            thermal_conductivity=1.8, # W/mK W/mK
            specific_heat_capacity=1000, #  c J/kgK            
            gross_density=2400, # ro kg/mc
        )

        air  =  AirLayer(
            name="air",
            thickness=0.1, # m
            heat_flow_direction="Do"

        )

        brick_a  =  MaterialLayer(
            name="brick_a",
            thickness=0.08, # m
            thermal_conductivity=0.35, # W/mK W/mK
            specific_heat_capacity=840, #  c J/kgK            
            gross_density=750, # ro kg/mc

        )

        brick_b  =  MaterialLayer(
            name="brick_b",
            thickness=0.12, # m
            thermal_conductivity=0.8, # W/mK W/mK
            specific_heat_capacity=840, #  c J/kgK            
            gross_density=1800, # ro kg/mc

        )
        iso  =  MaterialLayer(
            name="iso",
            thickness=0.05, # m
            thermal_conductivity=0.035, # W/mK W/mK
            specific_heat_capacity=840, #  c J/kgK            
            gross_density=175, # ro kg/mc

        )

        plaster  =  MaterialLayer(
            name="plaster",
            thickness=0.02, # m
            thermal_conductivity=0.9, # W/mK W/mK
            specific_heat_capacity=840, #  c J/kgK            
            gross_density=1400, # ro kg/mc

        )


        wall = Component(name="Wall", 
                        layers=[
                        concrete,
                        air,
                        brick_a,
                        brick_b,
                        iso,
                        plaster ],
                        heat_flow_direction="Ho"

                        )
        

        approx_rel_tot= 0.01

        self.assertTrue(math.isclose(0.47,wall.thickness_component,rel_tol=approx_rel_tot)) # m spessore totale
        self.assertTrue(math.isclose(0.06014,wall.decrement_factor,rel_tol=approx_rel_tot)) # - fd Fattore di decremento (attenuazione)
        self.assertTrue(math.isclose(13.376,wall.time_shift,rel_tol=approx_rel_tot)) #  phi (h) Ritardo fattore di decremento (sfasamento)
        self.assertTrue(math.isclose(0.026908,wall.periodic_thermal_transmittance,rel_tol=approx_rel_tot)) # Yie  # [W/m2K] Trasmittanza termica periodica 
        self.assertTrue(math.isclose(6.0131,wall.thermal_admittance_int,rel_tol=approx_rel_tot)) # Yii # [W/m2K] Ammettenza termica lato interno 
        self.assertTrue(math.isclose(1.9639,wall.thermal_admittance_ext,rel_tol=approx_rel_tot)) #  Yee  # [W/m2K] Ammettenza termica lato esterno 
        self.assertTrue(math.isclose(82.966,wall.areal_heat_capacity_int,rel_tol=approx_rel_tot)) # k1  #[kJ/m2K] Capacità termica areica lato interno 
        self.assertTrue(math.isclose(27.034,wall.areal_heat_capacity_ext,rel_tol=approx_rel_tot)) # k2=  #[kJ/m2K] Capacità termica areica lato esterno 
        self.assertTrue(math.isclose(553,wall.mass_component,rel_tol=approx_rel_tot)) # Ms  # [kg/m2]	Massa superficiale	
        self.assertTrue(math.isclose(2.235,wall.thermal_resistance_component,rel_tol=approx_rel_tot)) #  Rt  # [m2K/W]	Resistenza termica totale 	
        self.assertTrue(math.isclose(0.447,wall.thermal_transmittance_component,rel_tol=approx_rel_tot))  # U   # [W/m2K]	Trasmittanza 	
        self.assertTrue(math.isclose(503,wall.areal_heat_capacity_component,rel_tol=approx_rel_tot)) # Cta  # [kJ/m2K]	Capacità termica areica 	
        self.assertTrue(math.isclose(312,wall.time_constant,rel_tol=approx_rel_tot)) # t  # [h] Costante di tempo	

        self.assertEqual("Excellent 5/5",wall.threshold_values_italian_dm_26_06_2009)

    def test_wall_fr(self):

        beton  =  MaterialLayer(
            name="Béton",
            thickness=0.1, # m
            thermal_conductivity=1.8, # lambda W/mK
            specific_heat_capacity=1000, # calore spec c J/kgK            
            gross_density=2400, # ro kg/mc
        )

        couche_air  =  AirLayer(
            name="Couche d'air",
            thickness=0.1, # m
            heat_flow_direction="Do"

        )

        monomur  =  MaterialLayer(
            name="Monomur",
            thickness=0.08, # m
            thermal_conductivity=0.35, # lambda W/mK
            specific_heat_capacity=840, # calore spec c J/kgK            
            gross_density=750, # ro kg/mc

        )

        brique  =  MaterialLayer(
            name="Brique",
            thickness=0.12, # m
            thermal_conductivity=0.8, # lambda W/mK
            specific_heat_capacity=840, # calore spec c J/kgK            
            gross_density=1800, # ro kg/mc

        )
        isolant  =  MaterialLayer(
            name="Isolant",
            thickness=0.05, # m
            thermal_conductivity=0.035, # lambda W/mK
            specific_heat_capacity=840, # calore spec c J/kgK            
            gross_density=175, # ro kg/mc

        )

        enduit  =  MaterialLayer(
            name="Enduit",
            thickness=0.02, # m
            thermal_conductivity=0.9, # lambda W/mK
            specific_heat_capacity=840, # calore spec c J/kgK            
            gross_density=1400, # ro kg/mc

        )


        paroi = Component(name="Paroi", 
                        layers=[
                        beton,
                        couche_air,
                        monomur,
                        brique,
                        isolant,
                        enduit ],
                        heat_flow_direction="Do",
                        language="fr",
                        time_period=24

                        )
        
        self.assertIsInstance(paroi.get_layers_dataframe(data_type="df"),pd.DataFrame)
        self.assertEqual(type(paroi.get_layers_dataframe(data_type="st")),type(pd.DataFrame().style.format()))
        out_str=paroi.get_values()
        self.assertEqual("Période : 24 [h]",out_str.splitlines()[4])
        out_str=paroi.get_summer_performance_key_values()
        self.assertEqual("Résistance: 2.315 [m²K/W] Rsi and Rse included",out_str.splitlines()[6])



if __name__ == '__main__':
    unittest.main()