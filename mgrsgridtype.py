"""
***************************************************************************
 MgrsGridType - registers itself to Quantum as a Plugin Layer
                                 A QGIS plugin
 Overlays a user-definable grid on the map.
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

from qgis import core
from mgrsgridlayer  import MgrsGridLayer


class MgrsGridType(core.QgsPluginLayerType):
    def __init__(self):
        core.QgsPluginLayerType.__init__(self, MgrsGridLayer.LAYER_TYPE)

    def createLayer(self):
        return MgrsGridLayer()

    def showLayerProperties(self, layer):
        layer.showDialog()
        return True
