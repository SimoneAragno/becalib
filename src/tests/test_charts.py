import unittest
import matplotlib.pyplot as plt
import json
import numpy as np
from becalib.charts import plot_sinusoidal_wave,plot_component_layers
import math



class Testplot(unittest.TestCase):

    def test_plot(self):
        
        plt_sinu= plot_sinusoidal_wave(
            max_temp= 35, # °C
            min_temp = 28, # °C
            time_period =24, # in hours
            decrement_factor=1,  # ammortissement
            time_shift=6,
            language="fr"
              )
        

        # plt_sinu.show()
        self.assertTrue(bool(plt_sinu))


    def test_wall_layer(self):

        plt_lay= plot_component_layers(
            names=["layer 1","layer 2","layer 3"],
            thickness=[0.1,0.5,0.8],
            heat_flow_direction="Ho",
            language="fr"
        )

        # plt_lay.show()
        self.assertTrue(bool(plt_lay))





if __name__ == '__main__':
    unittest.main()