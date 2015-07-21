# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MgrsGridDialog
                                 A QGIS plugin
 Create MGRS(Military grid reference system) grid based on layer extend
                             -------------------
        forked               : 2015-07-21
        copyright            : (C) 2013 by Mikhail Tchernychev
                               (C) 2015 by tay7
        email                : tay7.git@gmail.com

This plugin is based from 'LatLon Grid'
                             -------------------
        original porject     : LatLon Grid
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

from PyQt4 import QtCore, QtGui, uic
from ui_mgrsgrid import Ui_MgrsGrid
from qgis.core import *
import qgis.utils
from qgis import core, gui


# create the dialog for zoom to point
#from PyQt4.QtCore import *


#( Ui_MgrsGrid, QDialog ) = uic.loadUiType( r'C:\Users\misha\.qgis2\python\plugins\MgrsGrid\ui_mgrsgrid.ui' )

import os
#( Ui_MgrsGrid, QDialog ) =  uic.loadUiType(os.path.join( os.path.dirname( __file__ ), 'ui_mgrsgrid.ui' ))

def load_combo_box_with_vector_layers(qgis, combo_box, set_selected, selectedText) :

    from mgrsgridtype import MgrsGridLayer

    selection  = -1

    for name, layer in QgsMapLayerRegistry.instance().mapLayers().iteritems():

        if layer.type() == QgsMapLayer.PluginLayer and layer.pluginLayerType() == MgrsGridLayer.LAYER_TYPE :
            continue


        combo_box.addItem(layer.name())

        if selectedText == layer.name():
            selection =  combo_box.count()-1


    if selection != -1:
        combo_box.setCurrentIndex(selection)


class MgrsGridDialog(QtGui.QDialog):
    def __init__(self, gridlayer):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_MgrsGrid()
        self.ui.setupUi(self)

        self.gridlayer = gridlayer

        self.label_attributes = core.QgsLabelAttributes()

        self.symbol = core.QgsLineSymbolV2.createSimple({'width':'0', 'color':'0,255,0'})


    def chooseFont(self):

        font = QtGui.QFont(self.label_attributes.family(), self.label_attributes.size())
        font.setBold(self.label_attributes.bold())
        font.setItalic(self.label_attributes.italic())
        font.setStrikeOut(self.label_attributes.strikeOut())
        font.setUnderline(self.label_attributes.underline())

        dlg = QtGui.QFontDialog()
        dlg.setCurrentFont(font)
        dlg.setModal(True)
        dlg.show()
        result = dlg.exec_()

        if result == 1:
            font = dlg.selectedFont()
            self.label_attributes.setFamily(font.family())
            self.label_attributes.setBold(font.bold())
            self.label_attributes.setItalic(font.italic())
            self.label_attributes.setUnderline(font.underline())
            self.label_attributes.setStrikeOut(font.strikeOut())
            self.label_attributes.setSize(font.pointSizeF(), core.QgsLabelAttributes.PointUnits)


    def accept(self):
        QtGui.QDialog.accept(self)
        self.gridlayer.parent_layer_name =  self.ui.selected_layer.currentText()

    def show(self):

        self.ui.selected_layer.clear()
        load_combo_box_with_vector_layers(qgis.utils.iface, self.ui.selected_layer, True, self.gridlayer.parent_layer_name)

        #if self.ui.selected_layer.count() != 0 :
        #    self.ui.warningLabel.setText("")
        #else :
        #    self.ui.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(False)

        QtGui.QDialog.show(self)


    def chooseColour(self):
        dlg = QtGui.QColorDialog(self.label_attributes.color())
        dlg.setOptions(QtGui.QColorDialog.ShowAlphaChannel)
        dlg.setModal(True)
        dlg.show()
        result = dlg.exec_()

        if result == 1:
            self.label_attributes.setColor(dlg.selectedColor())

    def chooseStyle(self):
        if QGis.QGIS_VERSION_INT < 10800:
            dlg = gui.QgsSymbolV2SelectorDialog(self.symbol,
                                                core.QgsStyleV2.defaultStyle())
        else:
            dlg = gui.QgsSymbolV2SelectorDialog(self.symbol,
                                                core.QgsStyleV2.defaultStyle(),
                                                None)
        dlg.setModal(True)
        dlg.show()
        dlg.exec_()

    def changeLayer(self, layer_name):
		pass

    def changeFormat(self, iformat):

        if iformat == 0:
           self.ui.long_spacing_label.setText("Longitude spacing, deg:")
           self.ui.lat_spacing_label.setText("Latitude spacing, deg:")

        if iformat == 1 :
            self.ui.long_spacing_label.setText("Longitude spacing, min:")
            self.ui.lat_spacing_label.setText("Latitude spacing, min:")

        if iformat == 2 :
            self.ui.long_spacing_label.setText("Longitude spacing, sec:")
            self.ui.lat_spacing_label.setText("Latitude spacing, sec:")
