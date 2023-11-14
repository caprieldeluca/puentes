## puentes
QGIS plugin to run external Python files.

-----
### With puentes you can:

- Write and save pyqgis code where you want, and run into QGIS with one click.

- Modify the code, save changes and run it again.

- Print messages to Log Messages Panel.

----
### Usage:

In the Plugins menu, a new Puentes node is created. It has two entries: 
- **Configure**: select a Python file to run.
- **Run**: run the file into QGIS.

Also, a **Puentes Toolbar** is added with a button to Run the file.

A keyboard shorcut doesn't come pre-assigned, but feel free to configure one for the Run action.

When run a file, a message is displayed in the Puentes tab inside Log Messages panel.

Print objects to that tab using _plog_ function.

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

If you want to import a personal toolbox of pyqgis modules as a package, in which you can edit files, write new code and run it trhough _puentes_ plugin, see the [mochila project](https://github.com/caprieldeluca/mochila).
