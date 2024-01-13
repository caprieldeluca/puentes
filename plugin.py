# -*- coding: utf-8 -*-
"""
************************************************************************
Name                 : plugin.py
Description          : QGIS plugin to run external Python files.
copyright            : (C) 2023 by Gabriel De Luca
email                : caprieldeluca@gmail.com
 ***********************************************************************
  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.
************************************************************************
"""

import io
from pathlib import Path
import runpy
import sys, traceback

from qgis.core import QgsApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import QSettings
from qgis.PyQt.QtWidgets import (
    QAction,
    QMenu,
    QFileDialog
)


class Puentes:
    """Main plugin class."""

    def __init__(self, iface):
        """Init the plugin."""
        self.iface = iface

        self.welcome_path = str(Path(__file__).parent / 'welcome.py')
        self.file_path = QSettings().value('plugins/puentes/file_path', self.welcome_path)


    def initGui(self):
        """Init actions, menu entries and toolbar."""

        # Init actions
        self.run_action = QAction(
            icon=QIcon(str(Path(__file__).parent / 'run.png')),
            text='&Run',
            parent=self.iface.mainWindow())
        self.configure_action = QAction(
            icon=QIcon(str(Path(__file__).parent / 'configure.png')),
            text='&Configure',
            parent=self.iface.mainWindow())

        # Connect actions to run methods
        self.run_action.triggered.connect(
            self.run_command)
        self.configure_action.triggered.connect(
            self.configure_command)

        # Init menu
        self.menu = QMenu('&Puentes')
        self.menu.addActions([
            self.run_action,
            self.configure_action])
        self.iface.pluginMenu().addMenu(self.menu)

        # Init toolbar
        self.toolbar = self.iface.addToolBar('Puentes Toolbar')
        self.toolbar.setObjectName('Puentes Toolbar')
        self.toolbar.addAction(self.run_action)


    def unload(self):
        """Remove menu entry and toolbar."""
        self.iface.removePluginMenu(
            '&Puentes',
            self.run_action)
        self.iface.removePluginMenu(
            '&Puentes',
            self.configure_action)
        del self.toolbar


    #####
    # Run command
    #####
    def run_command(self):
        """Load (run) the bridged module"""

        plog("----------")
        plog("Run:", self.file_path)
        try:
            runpy.run_path(self.file_path, init_globals={'plog': plog})

        except Exception:
            # From Python 3.10 only exc_value (the Exception instance) is needed,
            #  exc_type and exc_traceback are preserved for backwards compatibility
            exc_type, exc_value, exc_traceback = sys.exc_info()
            # Create a StackSummary object to get its length
            stack_length = len(traceback.extract_tb(exc_traceback))
            # Define limit as negative index to remove first frame 
            #  (this file exception) from the stacktrace
            limit = 1 - stack_length
            plog(*traceback.format_exception(exc_type,
                                            exc_value,
                                            exc_traceback,
                                            limit=limit))


    #####
    # Configure command
    #####
    def configure_command(self):
        """Set a new Python file to be loaded"""

        (filename, filter) = QFileDialog.getOpenFileName(
            parent=self.iface.mainWindow(),
            caption='Open Python File',
            directory=str(Path(self.file_path).parent),
            filter="*.py")

        if filename:
            self.file_path = str(Path(filename))
            # Save the path to settings right here, so it does not
            #  depend on run.
            QSettings().setValue('plugins/puentes/file_path', self.file_path)
            
            plog("----------")
            plog("Configured to run:", self.file_path)


#####
# plog (global)
#####

def plog(*objects, level=0):
    """Send *objects as log to Puentes tab of Log Messages Panel

    Use plog() instead of print() in pyqgis files.
    The plog name is assigned as a global name to the executed file.
    'from puentes.plugin import plog can be used in any other code from QGIS.

    level:  0 INFO (default)
            1 WARNING
            2 CRITICAL
    """

    messagelog = QgsApplication.messageLog()
    stringio = io.StringIO()
    # End without newline, so force to flush the io buffer
    print(*objects, end='', file=stringio, flush=True)
    msg = stringio.getvalue()
    formatted_msg = msg.replace("<","~::").replace(">","::~")
    messagelog.logMessage(
        message=formatted_msg,
        tag="Puentes",
        level=level)

