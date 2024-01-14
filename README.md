## puentes
QGIS plugin to run external Python files.

-----
### With puentes you can:

- Write and save pyqgis code where you want, and run into QGIS with one click.

- Modify the code, save changes and run it again.

- Print messages to Log Messages Panel.

----
### Usage:

In the _Plugins_ menu, a new _Puentes_ node is created. It has two entries: 
- **Configure**: select a Python file to run.
- **Run**: run the file into QGIS.

Also, a **Puentes Toolbar** is added with a button to Run the file.

A keyboard shorcut doesn't come pre-assigned, but feel free to configure one for the Run action.

Each time the Run action is executed again, the changes saved in the file to be run will be reflected.

When run a file, a message is displayed in the _Puentes_ tab, inside _Log Messages_ panel.

Print objects to that tab using **_plog_** function.

----
### The plog() function:

_puentes_ registers a `plog()` function to print objects to the Puentes tab of Log Messages panel.  

The _plog_ name is sent as a global name to the Python file to be run, so `plog()` can be called there instead of `print()`.

Once _puentes_ is installed, _plog_ name is also accesible from any other pyqgis code importing the _plugin_ module of _puentes_ package, so you can also do the following anywhere:

```python
from puentes.plugin import plog

plog("Hello world!")
```

----
### mochila:

If you want to import a personal toolbox of pyqgis modules as a package, in which you can edit files, write new code and run it through _puentes_ plugin, see the [mochila project](https://github.com/caprieldeluca/mochila).


----
### notes:

- The QGIS Log Messages panel does not allow to print angle brackets (_'<'_ and _'>'_) or content between them, so the _plog_ function replaces them with an -arbitrary- choice of characters (_'~::'_ and _':: ~'_).
- The _plog_ function is not intended to collapse with the built-in _print_ function, and it is not recommended to bind their names in the file to be run, so _print_ continues to have its normal -for code run in QGIS but outside QGIS Python Console- behavior (i.e., if QGIS is launched from a shell console or terminal emulator, _print_ will send messages there).
- The path of the file to run is saved in a QGIS setting for the active user profile, in the _/plugins/puentes/file_path_ node. This setting will not be shown in the new (as per QGIS 3.32) settings tree widget.
- Changes in version 1.1:
  - In the event of an exception, the stack trace is logged from the _FrameSummary_ object with index 1, that is, from _runpy.run_path_ (old behavior: log only last object).
  - The path of file to be run is saved in settings each time a new file is configured to run (old behavior: the setting was saved only on run success).
