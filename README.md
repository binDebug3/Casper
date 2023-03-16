<a name="readme-top"></a>

<div align="center">
    <h1 align="center">Casper</h1>
    <p align="center">
        A web scraping program that gathers online listings 
        to generate used car purchase recommendations by Dallin Stewart
    </p>
</div>

<hr>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#welcome">Welcome</a></li>
    <li><a href="#description">Description</a></li>
    <li><a href="#instructions">Instructions for Download</a></li>
    <li><a href="#use">Instructions for Use</a></li>
    <li><a href="#packages">Packages</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>

<!-- Welcome -->
## Welcome

Casper is a python program that uses selenium to gather data used car sales online from
retailers including AutoTrader, CarsDirect, CarGuru, Carvana, Lowbook, and KSL. As of the 
most recent update, Casper only searches for cars in the Provo, Utah area. After gathering 
data, Casper scores each car on how good of a deal the sale is and generates a CSV report of
the current market in addition to the market history since November 2022.

The name Casper is inspired by the Spanish word 'raspar', which means 'to scrape'. It is also 
a reference to 'Casper the Friendly Ghost' because when Casper is running, it looks like a ghost
is controlling your computer!

<hr>

### Description

1. AutoTrader.py scrapes basic listing data according to parameters from <a href='autotrader.com'>autotrader.com</a>
2. CarGuru.py scrapes basic listing data according to parameters from <a href='carguru.com'>carguru.com</a>
3. CarsDirect.py scrapes basic listing data according to parameters from <a href='carsdirect.com'>carsdirect.com</a>
4. Carvana.py scrapes basic listing data according to parameters from <a href='carvana.com'>carvana.com</a>
5. KSL.py scrapes basic listing data according to parameters from <a href='ksl.com'>ksl.com</a>
6. Lowbook.py scrapes basic listing data according to parameters from <a href='lowbook.com'>lowbook.com</a>
7. CG_Detail.py scrapes detailed information according to parameters
8. KSL_Detail.py scrapes detailed information according to parameters
9. CD_Detail.py scrapes detailed information according to parameters </br></br>
10. Compressor.py compresses images scraped from websites using a custom image compression algorithm
11. Search.py performs operations for scraping that are input and website agnostic
12. main.py contains configuration details and calls each of the website scrapers to build final CSV reports

<hr>

### Instructions for Download
You'll need to start by downloading a few python packages with these commands:
- pip install <a href=https://selenium-python.readthedocs.io/installation.html>selenium</a>
- pip install <a href=https://pandas.pydata.org/docs/getting_started/install.html>pandas</a>
- pip install <a href=https://scipy.org/install/>scipy</a>
- pip install <a href=https://matplotlib.org/stable/users/installing/index.html>matplotlib</a>
- pip install <a href=https://numpy.org/install/>numpy</a>
- pip install <a href=https://pypi.org/project/plyer/>plyer</a>
- pip install <a href=https://imageio.readthedocs.io/en/v2.8.0/installation.html>imageio</a>
- pip install <a href=''>pytorch</a>

You can then <a href=https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository>
clone this project</a> to your own machine from GitHub and then run the webscraper in any Python development environment.

<p align="right">(<a href="#readme-top">top</a>)</p>

<hr>

### Instructions for Use

1. Create a CSV file for each website and put them in a folder called 'Data': </br>
a) autotrader.csv</br>
b) CarsDirect.csv</br>
c) CarGuru.csv</br>
e) Carvana.csv</br>
e) ksl.csv</br>
f) current_market.csv</br>
2. Run 'main.py'

<p align="right">(<a href="#readme-top">top</a>)</p>

<hr>

### Packages

[![Python][Python-icon]][Python-url] &emsp; &emsp; [![Jupyter][Jupyter-icon]][Jupyter-url] &emsp; &emsp; &nbsp; 
[![Numpy][Numpy-icon]][Numpy-url] &emsp; &emsp; [![Scipy][Scipy-icon]][Scipy-url]

[![Matplotlib][Matplotlib-icon]][Matplotlib-url] &emsp; &emsp; [![ImageIO][ImageIO-icon]][ImageIO-url] &emsp; &emsp;
[![Pandas][Pandas-icon]][Pandas-url] &emsp; &emsp; [![Selenium][Selenium-icon]][Selenium-url]

[![PyTorch][PyTorch-icon]][PyTorch-url] &emsp; &emsp; [![Plyer][Plyer-icon]][Plyer-url]

<p align="right">(<a href="#readme-top">top</a>)</p>


<!-- CONTACT -->
## Contact

Dallin Stewart - dallinpstewart@gmail.com

[![LinkedIn][linkedin-icon]][linkedin-url]
[![GitHub][github-icon]][github-url]
[![Email][email-icon]][email-url]

<p align="right">(<a href="#readme-top">top</a>)</p>

<hr>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* <a href='https://www.linkedin.com/in/benjamin-mcmullin/'>Benjamin McMullin</a> for writing Lowbook.py
* Brigham Young University, Applied and Computational Mathematics - [About](https://acme.byu.edu/)
* Brigham Young University Volume 1, Volume 2 Labs - [Lab Descriptions](https://acme.byu.edu/2022-2023-materials)

<p align="right">(<a href="#readme-top">top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES for DATA SCRAPING -->
[Python-icon]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/

[Jupyter-icon]: https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=Jupyter&logoColor=white
[Jupyter-url]: https://jupyter.org/

[NumPy-icon]: https://img.shields.io/badge/NumPy-2596be?style=for-the-badge&logo=numpy&logoColor=white
[NumPy-url]: https://numpy.org/

[Matplotlib-icon]: https://img.shields.io/badge/Matplotlib-3776AB?style=for-the-badge&logo=matplotlib&logoColor=white
[Matplotlib-url]: https://matplotlib.org/

[Pandas-icon]: https://img.shields.io/badge/Pandas-120756?style=for-the-badge&logo=pandas&logoColor=white
[Pandas-url]: https://pandas.pydata.org/

[Scipy-icon]: https://img.shields.io/badge/SciPy-8CAAE6?style=for-the-badge&logo=scipy&logoColor=white
[Scipy-url]: https://www.scipy.org/

[Selenium-icon]: https://img.shields.io/badge/Selenium-999999?style=for-the-badge&logo=selenium&logoColor=white
[Selenium-url]: https://selenium-python.readthedocs.io/

[Plyer-icon]: https://img.shields.io/badge/Plyer-999999?style=for-the-badge&logo=plyer&logoColor=white
[Plyer-url]: https://plyer.readthedocs.io/en/latest/

[ImageIO-icon]: https://img.shields.io/badge/ImageIO-999999?style=for-the-badge&logo=imageio&logoColor=white
[ImageIO-url]: https://imageio.readthedocs.io/en/stable/


<!-- MARKDOWN LINKS & IMAGES for MACHINE LEARNING -->

[PyTorch-icon]: https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white
[PyTorch-url]: https://pytorch.org/


<!-- MARKDOWN LINKS & IMAGES for CONTACT -->

[linkedIn-icon]: https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white
[linkedIn-url]: https://www.linkedin.com/in/dallinstewart/

[github-icon]: https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white
[github-url]: https://github.com/binDebug3

[Email-icon]: https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white
[Email-url]: mailto:dallinpstewart@gmail.com