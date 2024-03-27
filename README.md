<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/SimoneAragno/becalib">
    <img src="https://raw.githubusercontent.com/SimoneAragno/becalib/main/docs/images/logo_big.svg" alt="Logo BECALIB"  
    name="BECALIB Building Envelop Component Analysis" height="200">
  </a>
  <!-- <h3 align="center">Title</h3> -->

  <p align="center">
    <!-- An awesome short description -->
    <br />
    <a href="https://github.com/SimoneAragno/becalib"><strong>github repo</strong></a>
    <br />
    <a href="https://colab.research.google.com/drive/1wi_Zvera_F_ryUTSldSsDxKofC2YJIEZ#scrollTo=QZ7VNNPE2P2L">Colab Notebook Demo</a>
    ·
    <a href="https://github.com/SimoneAragno/becalib/issues">Report Bug</a>
    ·
    <a href="https://github.com/SimoneAragno/becalib/issues">Request Feature</a>
    ·
    <a href="https://pypi.org/project/becalib/">PyPI</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
## Table of Contents
<!-- <details> -->
  <!-- <summary>Table of Contents</summary> -->
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#demo">Demo</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
<!-- </details> -->


<!-- ABOUT THE PROJECT -->
## About The Project
  <a href="https://colab.research.google.com/drive/1wi_Zvera_F_ryUTSldSsDxKofC2YJIEZ#scrollTo=QZ7VNNPE2P2L">
    <img src="https://raw.githubusercontent.com/SimoneAragno/becalib/main/docs/images/becalib_screenshots.jpg" alt="BECALIB screenshots"  
    name="BECALIB Building Envelop Component Analysis screenshots" width="800">
  </a>


BECALIB is a tool designed to run thermal analysis of building envelope components such as walls, roofs, and floors.

With this tool, you can define the materials and air gaps in a multi-layer component, run thermal analysis, and generate diagrams.

Currently, BECALIB focuses on analyzing summer performance. Specifically, it can compute time-shift and decrement factors. These values allow designers to evaluate and quantify a component's ability to break heat flow and reduce cooling loads. 

Static values like u-value and thermal resistance are also available.

BECALIB provides threshold values and performance scores to help designers enhance their components.

The calculations in BECALIB have been developed in accordance with ISO standards, including ISO 13786 and ISO 6946.


### Built With
Love and:
* [numpy][numpy_url]
* [pandas][pandas_url]
* [matplotlib][matplotlib_url]

<!-- GETTING STARTED -->
## Getting Started
BECALIB python package is available on [PyPI][pypi_url] repository. 

If you have some experience with python programming and you want a Stand-alone installation, all you need is install [python][python_url] on your machine.

If you are not familiar with python installations you can use/copy BECALIB notebook from [google Colab Notebook DEMO][colab_en_url].

### Prerequisites
Dependencies of BECALIB are available in requirements.txt file but you do not need to install anything because everything have been wrapped in BECALIB package available on [PyPI][pypi_url]

### Demo
Google colab notebooks are available.
If you want to try BECALIB and create your own components you can start here and duplicate the file.

* [google colab notebook demo [English version]][colab_en_url]
* [google colab notebook demo [French version]][colab_fr_url]



### Installation

#### Stand-alone installation:

1. Activate your [virtual environnement][venv_url]
2. Install becalib with pip:
  ```
  pip install becalib
  ```

#### Google colab notebook installation:
  ```
  !pip install becalib
  ```


[pypi_url]: https://pypi.org/project/becalib/ "PyPI"
[python_url]: https://pypi.org/project/becalib/ "python"

[colab_en_url]: https://colab.research.google.com/drive/1wi_Zvera_F_ryUTSldSsDxKofC2YJIEZ#scrollTo=QZ7VNNPE2P2L "Colab Notebook EN DEMO"

[colab_fr_url]: https://colab.research.google.com/drive/1cml04fzYJg9I05-lZxdJ_02pw_JckRT1#scrollTo=QZ7VNNPE2P2L "Colab Notebook FR DEMO"

[numpy_url]:https://pypi.org/project/numpy/
[pandas_url]:https://pypi.org/project/pandas/
[matplotlib_url]:https://pypi.org/project/matplotlib/
[venv_url]:https://docs.python.org/3/tutorial/venv.html



<!-- USAGE EXAMPLES -->
## Usage
You can use BECALIB in a python file or a notebook (jupyter/google colab) 
### 0. import classes and methods from BECALIB library

```python
from becalib import MaterialLayer, AirLayer
from becalib import Component
```

### 1. Materials layers setup
Instantiate a layer objet for each component layer \
Example of concrete layer setup:
```python
concrete  =  MaterialLayer(
            name="Concrete",
            thickness=0.1, # m
            thermal_conductivity=1.8, # lambda W/mK
            specific_heat_capacity=1000, #  c J/kgK            
            gross_density=2400, # ro kg/mc
```

Example of air gap layer setup:
```python
air_gap  =  AirLayer(
    name="air_gap",
    thickness=0.1, # m
    heat_flow_direction="Do"
)
```

### 2. Components setup:
Instantiate a component objet and set:
* List of layers  (interior to exterior)
* Heat flow direction:\
            "Ho": Horizontal (example: wall) or \
            "Up": Upwards (example Roof) or \
            "Do": Downwards (example floor)
* language (en, fr, etc..)

```python
wall = Component(name="Wall", 
                layers=[
                concrete,
                air_gap,
                concrete ],
                heat_flow_direction="Do",
                language="en"
                )
```
### 3. Get component table (Pandas DataFrame)

```python
wall.get_layers_dataframe(data_type="st")
```
<a href="https://colab.research.google.com/drive/1wi_Zvera_F_ryUTSldSsDxKofC2YJIEZ#scrollTo=QZ7VNNPE2P2L">
  <img src="https://raw.githubusercontent.com/SimoneAragno/becalib/main/docs/images/becalib_comp_dataframe_en.png" alt="BECALIB screenshots"  
  name="BECALIB Building Envelop Component Analysis screenshots" width="800">
</a>

### 4. Print values
```python
print(wall.get_summer_performance_key_values())
```

```
#######################################
Component: wall

Time period: 24 [h]

Thickness: 0.440 [m]
Resistance: 2.114 [m²K/W] Rsi and Rse included
Transmittance: 0.473 [W/m²K]

Decrement factor: 0.055 [-]
Time shift: 13.0 [h]

Interior areal heat capacity: 67.185 [kJ/m²K] 

Summer performance: Excellent 5/5 (in accordance with italian DM 26/06/2009)
Surface mass: 612.8 [kg/m²]

#######################################
```

### 5. Plot diagrams
```python
wall.get_component_layers_chart().show()
```

<a href="https://colab.research.google.com/drive/1wi_Zvera_F_ryUTSldSsDxKofC2YJIEZ#scrollTo=QZ7VNNPE2P2L">
  <img src="https://raw.githubusercontent.com/SimoneAragno/becalib/main/docs/images/layers_en.png" alt="BECALIB screenshots"  
  name="BECALIB Building Envelop Component Analysis screenshots" width="400">
</a>

```python
paroi.get_component_sinusoidal_wave_chart().show()
```
<a href="https://colab.research.google.com/drive/1wi_Zvera_F_ryUTSldSsDxKofC2YJIEZ#scrollTo=QZ7VNNPE2P2L">
  <img src="https://raw.githubusercontent.com/SimoneAragno/becalib/main/docs/images/waves_en.png" alt="BECALIB screenshots"  
  name="BECALIB Building Envelop Component Analysis screenshots" width="400">
</a>



<!-- ROADMAP -->
## Roadmap
- [x] Material and air layers classes
- [x] Components classes
- [x] Air resistances computations (ISO 6946:2007)
- [x] Summer Analysis values (ISO 13786)
- [x] Summer Analysis charts (ISO 13786)
- [ ] Add docs with Sphinx
    - [ ] set Sphinx docs
    - [ ] deploy docs static pages
- [ ] Add materials database
    - [ ] Define standard materials database
    - [ ] Component setup from material database
- [ ] Add Condensation risk analysis
    - [ ] Computations
    - [ ] Glaser diagram
- [ ] Add Comparator tools
    - [ ] Materials comparator table
    - [ ] Materials comparator charts
    - [ ] Components comparator table
    - [ ] Components comparator charts
- [ ] Multi-language (gettext)
    - [x] French
    - [ ] Italian
    - [ ] Spanish

See the [open issues](https://github.com/SimoneAragno/becalib/issues) for a full list of proposed features (and known issues).


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->

## License
Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->

## Contact

Simone ARAGNO - aragno.simone@gmail.com

Project Link: [https://github.com/SimoneAragno/becalib](https://github.com/SimoneAragno/becalib)




<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Best-README-Template](https://github.com/othneildrew/Best-README-Template)
* [ISO 13786:2017 Thermal performance of building components Dynamic thermal characteristics Calculation methods](https://www.iso.org/standard/65711.html)


