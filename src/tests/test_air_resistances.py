import unittest
from becalib.air_resistances import get_surface_resistances, get_resistance_unventilated_air_layer


class TestAirResist(unittest.TestCase):

    def test_get_res_ho(self):
        self.assertEqual((0.13 , 0.04),get_surface_resistances(heat_flow_direction="Ho"))
    
    def test_get_res_up(self):
        self.assertEqual((0.10 , 0.04),get_surface_resistances(heat_flow_direction="Up"))

    def test_get_res_do(self):
        self.assertEqual((0.17 , 0.04),get_surface_resistances(heat_flow_direction="Do"))

    


    def test_get_resistance_unventilated_air_layer(self):

        self.assertEqual(
            get_resistance_unventilated_air_layer(
            heat_flow_direction="Do",
            thickness=5*10**-3),
            0.11
            )
        
        self.assertEqual(
            get_resistance_unventilated_air_layer(
            heat_flow_direction="Do",
            thickness=15*10**-3),
            0.17
            )
        self.assertEqual(
            get_resistance_unventilated_air_layer(
            heat_flow_direction="Up",
            thickness=10*10**-3),
            0.15
            )
        
        self.assertEqual(
            get_resistance_unventilated_air_layer(
            heat_flow_direction="Ho",
            thickness=0*10**-3),
            0
            )
        self.assertEqual(
            get_resistance_unventilated_air_layer(
            heat_flow_direction="Ho",
            thickness=2),
            0.18
            )
        



if __name__ == '__main__':
    unittest.main()