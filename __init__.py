# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MgrsGrid
                                 A QGIS plugin
 Create Lat/lon grid based on layer extend
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
 This script initializes the plugin, making it known to QGIS.
"""


def name():
    return "MgrsGrid"


def description():
    return "Create Lat/lon grid based on layer extend"


def version():
    return "Version 0.1"


def icon():
    return "icon.png"


def qgisMinimumVersion():
    return "2.0"

def author():
    return "Mikhail Tchernychev"

def email():
    return "mikhail_tchernychev@yahoo.com"

def classFactory(iface):
    # load MgrsGrid class from file MgrsGrid
    from mgrsgrid import MgrsGrid
    return MgrsGrid(iface)
