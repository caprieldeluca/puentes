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
import importlib
import os
import runpy
import sys

from qgis import processing
from qgis.core import (
    QgsApplication,
    QgsSettings)
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import (
    QCoreApplication,
    QLocale,
    QSettings,
    QTranslator,
    QUrl
)
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

        self.welcome_path = os.path.join(
            os.path.dirname(__file__),
            'welcome.py')

        self.ensure_settings()

        # Init attributes
        self.recent = QSettings().value('puentes/recent')
        self.recent_list = [r for r in self.recent.split(',')]

        self.file_path = self.recent_list[0]

        self.max_length = int(QSettings().value('puentes/max_length'))

    def ensure_settings(self):
        """ Ensure that (at least default) settings exist."""

        if not QSettings().contains('puentes/recent'):
            QSettings().setValue(
                'puentes/recent',
                os.path.join(os.path.dirname(__file__),'welcome.py'))

        if not QSettings().contains('puentes/max_length'):
            QSettings().setValue(
                'puentes/max_length',
                10)

        if not QSettings().contains('puentes/ui/work_dir'):
            QSettings().setValue(
                'puentes/work_dir',
                '')

    def initGui(self):
        """Init actions, run methods, menu entries and provider."""
        # Init actions
        self.run_action = QAction(
            icon=QIcon(os.path.join(os.path.dirname(__file__),
                'run.png')),
            text='&Run',
            parent=self.iface.mainWindow()
        )
        self.configure_action = QAction(
            icon=QIcon(os.path.join(os.path.dirname(__file__),
                'configure.png')),
            text='&Configure',
            parent=self.iface.mainWindow()
        )
        # Connect actions to run methods
        self.run_action.triggered.connect(
            self.run_command
        )
        self.configure_action.triggered.connect(
            self.configure_command
        )
        # Init menu
        self.menu = QMenu('&Puentes')
        self.menu.addActions([
            self.run_action,
            self.configure_action
        ])
        self.iface.pluginMenu().addMenu(self.menu)
        # Init toolbar
        self.toolbar = self.iface.addToolBar('Puentes')
        self.toolbar.setObjectName('Puentes_toolbar')
        self.toolbar.addAction(self.run_action)

    def unload(self):
        """Remove menu entry and toolbar."""
        self.iface.removePluginMenu(
            '&Puentes',
            self.run_action
        )
        self.iface.removePluginMenu(
            '&Puentes',
            self.configure_action
        )
        del self.toolbar

    #####
    # Run command
    #####
    def run_command(self):
        """Load (run) the bridged module"""

        plog("----------")

        try:
            runpy.run_path(self.file_path, init_globals={'plog': plog})

            QSettings().setValue(
                'puentes/recent',
                self.file_path)


        except Exception as e:
            plog(type(e), e)

    #####
    # Configure command
    #####
    def configure_command(self):
        """Set a new Python file to be loaded"""

        (filename, filter) = QFileDialog.getOpenFileName(
            parent=self.iface.mainWindow(),
            caption='Open Python File',
            directory=os.path.dirname(self.file_path),
            filter="*.py")

        if filename:
            self.file_path = filename
            plog("----------")
            plog("File to be run =", self.file_path)


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

