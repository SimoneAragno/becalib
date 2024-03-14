


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/SimoneAragno/becalib">
    <img src="docs/images/logo_big.svg?raw=true" alt="Logo BECALIB"  
    name="BECALIB Building Envelop Component Analysis" height="200">
  </a>
  <!-- <h3 align="center">Title</h3> -->



  <p align="center">
    <!-- An awesome short description -->
    <!-- <br /> -->
    <!-- <a href="https://github.com/SimoneAragno/becalib"><strong>Explore the docs</strong></a> -->
    <!-- <br /> -->
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
<details>
  <summary>Table of Contents</summary>
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
</details>


<!-- ABOUT THE PROJECT -->
## About The Project
  <a href="https://colab.research.google.com/drive/1wi_Zvera_F_ryUTSldSsDxKofC2YJIEZ#scrollTo=QZ7VNNPE2P2L">
    <img src="docs/images/becalib_screenshots.jpg?raw=true" alt="BECALIB screenshots"  
    name="BECALIB Building Envelop Component Analysis screenshots" width="800">
  </a>


BECALIB is a tool designed to run thermal analyses of building envelope components such as walls, roofs, and floors.

With this tool, you can define the materials and air gaps in a multi-layer component, run thermal analyses, and generate diagrams.

Currently, BECALIB focuses on analyzing summer performance. Specifically, it can compute time-shift and decrement factors. These values allow designers to evaluate and quantify a component's ability to break heat flow and reduce cooling loads. 

Static values like u-value and thermal resistance are also available.

BECALIB provides threshold values and performance scores to help designers enhance their components.

The calculations in BECALIB have been developed in accordance with ISO standards, including ISO 13786 and ISO 6946.
<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

Love and:

* [numpy][numpy_url]
* [pandas][pandas_url]
* [matplotlib][matplotlib_url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>




<!-- GETTING STARTED -->
## Getting Started
BECALIB python package is available on [PyPI][pypi_url] repository. 

If you have some experience with python programming and you want a Stand-alone installation, all you need is install [python][python_url] on your machine.

If you are not familiar with python installations you can use/copy BECALIB from [google Colab Notebook DEMO][colab_url].

### Prerequisites
Dependencies of BECALIB are available in requirements.txt file but you do not need to install anything because everything have been wrapped in BECALIB package available on [PyPI][pypi_url]



### Installation

Stand-alone installation:

1. Activate your virtual environnement
2. Install with pip:
  ```
  pip install becalib
  ```

Google colab notbook installation:
  ```
  !pip install becalib
  ```
<p align="right">(<a href="#readme-top">back to top</a>)</p>





[pypi_url]: https://pypi.org/project/becalib/ "PyPI"
[python_url]: https://pypi.org/project/becalib/ "python"
[colab_url]: https://colab.research.google.com/drive/1wi_Zvera_F_ryUTSldSsDxKofC2YJIEZ#scrollTo=QZ7VNNPE2P2L "Colab Notebook DEMO"

[numpy_url]:https://pypi.org/project/numpy/
[pandas_url]:https://pypi.org/project/pandas/
[matplotlib_url]:https://pypi.org/project/matplotlib/



























<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [x] Add Changelog
- [x] Add back to top links
- [ ] Add Additional Templates w/ Examples
- [ ] Add "components" document to easily copy & paste sections of the readme
- [ ] Multi-language Support
    - [ ] Chinese
    - [ ] Spanish

See the [open issues](https://github.com/othneildrew/Best-README-Template/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



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

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Your Name - [@your_twitter](https://twitter.com/your_username) - email@example.com

Project Link: [https://github.com/your_username/repo_name](https://github.com/your_username/repo_name)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Use this space to list resources you find helpful and would like to give credit to. I've included a few of my favorites to kick things off!

* [Choose an Open Source License](https://choosealicense.com)
* [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
* [Malven's Flexbox Cheatsheet](https://flexbox.malven.co/)
* [Malven's Grid Cheatsheet](https://grid.malven.co/)
* [Img Shields](https://shields.io)
* [GitHub Pages](https://pages.github.com)
* [Font Awesome](https://fontawesome.com)
* [React Icons](https://react-icons.github.io/react-icons/search)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
1wi_Zvera_F_ryUTSldSsDxKofC2YJIEZ#scrollTo=QZ7VNNPE2P2L

[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/

[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D

[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 



<script>
a_test = "test"
</script>