# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MgrsGrid
                                 A QGIS plugin
 Create MGRS grid based on layer extend
                              -------------------
        begin                : 2013-09-27
        copyright            : (C) 2013 by Mikhail Tchernychev
        email                : mikhail_tchernychev@yahoo.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis import core

# Initialize Qt resources from file resources.py
import resources_rc

# Import the code for the dialog
from mgrsgriddialog import MgrsGridDialog
from mgrsgridtype   import MgrsGridType
from mgrsgridlayer  import MgrsGridLayer

import os.path

import webbrowser, os

# Set up current path.
currentPath = os.path.dirname( __file__ )

class MgrsGrid:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'mgrsgrid_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/mgrsgrid/icon.png"),
            u"MGRS grid lines", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&MgrsGrid", self.action)

        self.help_action = QAction(
            QIcon(":/plugins/mgrsgrid/help.png"),
            u"Help on MGRS grid", self.iface.mainWindow())
        # connect the action to the run method
        self.help_action.triggered.connect(self.help)
        self.iface.addPluginToMenu(u"&MgrsGrid", self.help_action)

        core.QgsPluginLayerRegistry.instance().addPluginLayerType(MgrsGridType())

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&MgrsGrid", self.action)
        self.iface.removePluginMenu(u"&MgrsGrid", self.help_action)

        self.iface.removeToolBarIcon(self.action)
        core.QgsPluginLayerRegistry.instance().removePluginLayerType(MgrsGridLayer.LAYER_TYPE)

    # run method that performs all the real work
    def run(self):
        # show the dialog
        layer = MgrsGridLayer()
        layer.showDialog()

        # Run the dialog event loop
        if layer.isValid():
            core.QgsMapLayerRegistry.instance().addMapLayer(layer)

    def help(self):
        webbrowser.open(currentPath + "/help/mgrs_plugin.html")
