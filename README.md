# cognitive-systems-project

Semestral project for Cognitive Systems course. Implemention of a cognitive test called SART. Works cross-platform (tested on Linux and Windows).

## How to run this project
_The easy way:_  

0. Install anaconda or miniconda (smaller)
1. Run ``conda env create -f sart.yml`` to create new conda environment called _sart_.
2. Activate newly created environment by: ``conda activate sart``.
3. To run the project, run main.py in python: ``python ./main.py``.
4. To remove the environment from your system run: ``conda env remove -n sart -y``
  
_The manual way:_  
Python 2.7 (yes... the old one, we had a reason)  
Tkinter  
pillow  
scipy  
numpy  
matplotlib  

### Known issues

- Only use ASCII letters (eg. not čřáíé...) in your name, otherwise saving your results to file will fail.
