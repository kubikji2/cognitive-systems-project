# cognitive-systems-project

Semestral project for Cognitive Systems course. Implemention of a cognitive test called SART. Works cross-platform (tested on Linux and Windows).

## How to run this project

_The Anaconda way:_  

1. Install anaconda or miniconda (smaller)
2. Open terminal in project's root and run ``conda env create -f windows.yml`` in Windows OS, or ``conda env create -f linux.yml`` in Ubuntu OS, to create a new conda environment called _sart_.
3. Activate the environment: ``conda activate sart``.
4. Run the project: ``python ./main.py``.

- To later remove the environment from your system run: ``conda env remove -n sart -y``
  
_The manual way:_  
  
Install:  
&nbsp;&nbsp;Python 2.7 (yes... the old one, we had a reason)  
And these libs:  
&nbsp;&nbsp;Tkinter  
&nbsp;&nbsp;pillow  
&nbsp;&nbsp;scipy  
&nbsp;&nbsp;numpy  
&nbsp;&nbsp;matplotlib  
And run it

### Known issues

- Only use ASCII letters (eg. not čřáíé...) in your name, otherwise saving your results to file will fail.
