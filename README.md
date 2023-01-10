<h1 align="center">
   ATPxml converter app
</h1>
<p align="center">
   Tool for converting Automated test platform (ATP) XML files.
</p>
<img src="./media/images/teststeptranlsation.png"/>

## Get started:

**Git**

To install and run your own copy of this first navigate to your desired directory clone the repository:

```
$ git clone https://github.com/bubuding0809/XML-Converter.git
$ cd XML-Converter
```

You will need python version 3 and above to run this application.

**Python**

Create a virtual enviroment to isolate project:

```
$ python3 -m venv env
```

_Feel free to create your virtual enviroment in the project root or somewhere else._

Activate virtual environment

```
// Windows
$ env/Scripts/activate

// macOS
$ source env/bin/activate
```

Install dependencies via requirement.txt

```
pip install -r requirements.txt
```

**requirements.txt**

```
altgraph==0.17.2
click==7.1.2
deepdiff==5.8.1
et-xmlfile==1.1.0
future==0.18.2
openpyxl==3.0.10
ordered-set==4.1.0
pefile==2022.5.30
pyinstaller==5.1
pyinstaller-hooks-contrib==2022.7
PyQt5==5.15.4
pyqt5-plugins==5.15.4.2.2
PyQt5-Qt5==5.15.2
PyQt5-sip==12.10.1
pyqt5-tools==5.15.4.3.2
python-dotenv==0.20.0
pywin32-ctypes==0.2.0
qt5-applications==5.15.2.2.2
qt5-tools==5.15.2.1.2
```

Run application:

```
python app.py
```

## Project architecture:

The project structural diagram can be viewed at the this [link](https://www.figma.com/file/HLLt2wOncSbf3p58NNIHlv/ATPXML-converter-flow-chart?node-id=0%3A1).

## Deployment:

The application can be deployed with the help of [Pyinstaller](https://pyinstaller.org/en/stable/). A detailed guide on how to deploy a PyQt5 application can be found [here](https://www.pythonguis.com/tutorials/packaging-pyqt5-pyside2-applications-windows-pyinstaller/).

Quickly deploy existing application:

```
//Activate your virtual enviroment and navigate to the project root

$ pip install PyInstaller
$ pyinstaller app.py
```

If you look in your folder you'll notice you now have two new folders `dist` and `build`, and a `app.spec` file.

Tweak your build by editing the generated `app.spec` file and rebuild the application with:

```
$ pyinstaller app.spec
```

If you look in your folder you'll notice you now have two new folders dist and build.

The `dist` (for "distribution") folder contains the files to be distributed. This includes your application, bundled as an executable file, together with any associated libraries (for example PyQt5) and binary .dll files.

## Technologies:

- Python 3
- Cross platform GUI framework [PyQt 5](https://doc.qt.io/qtforpython-5/#documentation)
- Python library for .xlsx/.xlsm files [openpyxel](https://openpyxl.readthedocs.io/en/stable/)
- Python library for .xml files [ElementTree XML API](https://docs.python.org/3/library/xml.etree.elementtree.html)
