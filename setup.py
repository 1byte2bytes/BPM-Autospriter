from distutils.core import setup
import py2exe

setup(
    console=['autosprite.py'],
    options={
        "py2exe":{
            "excludes":["PIL._imagingagg", "PyQt4", "PyQt5", "PySide", "_imaging_gif", "_util", "cffi", "readline", "tkinter"]
        }
    }
)
