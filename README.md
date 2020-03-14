Python Tkinter Minesweeper
===========================

Minesweeper game written in Python using Tkinter GUI library.

<img src="https://i.imgur.com/vqYzYh9.png" alt="Screenshot on Windows 10" height="350"/>

Introduction:
----------
Hello all (and hello fellow Looneys)! This is my project that I've been working on to surprise the Looneybins. There is plenty that still needs to be added/fixed in this game. See "To Do" section for things that need to be added.

Executing the Script:
----------
There are a couple of things that need to be installed in order for you to run this program. I've outlined some steps you will need to know in order to run this script and play minesweeper. **NOTE:** These instructions are for Windows **ONLY**. These steps **should** work for linux and Mac; however, I cannot promise you will not have any issues with it.

1. Install Python 3.7.
    * There is a possibility that python may already be installed on your computer. To check, open up command prompt on the computer. In the terminal, type `<python --version>`. If you see text That says `<Python 3.7.x>` (x being a number) then you are good to go!
    * I highly recommend installing Python by using [Anaconda] (https://www.anaconda.com/distribution/#download-section). Anaconda has a great package manager if you plan on getting into Python more. **NOTE:** During installation, there is an option to install Python into the PATH environment variable. I recommend checking this box if you do not not Python installed on your machine.
    * You can also install the latest version of Python [here] (https://www.python.org/downloads/windows/). As long as the Python is greater than "Python 3.7" it should be compaatible. Going this route might require the installation of additional packages. If you go this route and you run into errors, you will need to find me or "@" me in Lowco's discord and I can help you when I'm available.
1. Install PIL package.
    **If Anaconda was installed:**
    1. Open up the command prompt and type in the following `<conda --version>`. This will display the version of the conda package manager. If you do not see anything appear, it means Anaconda was not installed properly!
    1. If installed properly, type the following into the command prompt `<conda install Pillow>`. Wait for this to finish.
    **Other Installation of Python**
    1. TODO
1. Close that command prompt and save the files from github to your computer. You will need `<images>` folder and the `<minesweeper.py>` file. They **MUST** be placed within the same folder!
1. Launch the script!
    1. Double click on `<minesweeper.py>` and it should launch!
    1. If it doesn't open up, or you want to be fancy, open up command prompt and navigate to where the file is located. This can be done by using the command `<cd>` which stands for **c**hange **d**irectory. I have this script installed on my a secondary drive, so to change to my location, I would type `<D:\Python_Projects\lowco-minesweeper>`. Once in the correct directory, type `<python minesweeper.py>` to open up the game!
1. Have fun!


Contents:
----------
- */minesweeper.py* - The actual python program
- */images/* - GIF Images ready for usage with Tkinter
- */images/original* - Original PNG images made with GraphicsGale
- */images/lowco/* - PNG Images ready for usage with Tkinter
- */images/lowco/original/* - Original PNG images downloaded from the interwebs.

To Do:
----------
- Have specific number of mines, rather than random
- Highscore table
- Adjustable grid and mine count via UI
- Add compatability with Python 2.7
