# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MgrsUtil
                                 A QGIS plugin
Utility function for MGRS.
                              -------------------
        begin                : 2015-07-21
        copyright            : (C) 2015 by tay7
        email                : tay7.git@gmail.com
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
from mgrs import Mgrs
import re

class MgrsTool():
  ct = Mgrs()
  epsg4326 = core.QgsCoordinateReferenceSystem("EPSG:4326")
  re_mgrs = re.compile('([0-9]{1,2})([A-Z]+)([0-9]*)')

  def toMgrs(self, pt):
#        canvas = iface.mapCanvas()
        canvas = qgis.utils.iface.mapCanvas()

#        canvasCrs = canvas.mapRenderer().destinationCrs()

        try:
             canvasCrs = canvas.mapSettings().destinationCrs()
        except:
             canvasCrs = canvas.mapRenderer().destinationCrs()

        transform = QgsCoordinateTransform(canvasCrs, self.epsg4326)
        pt4326 = transform.transform(pt.x(), pt.y())

        try:
            mgrsCoords = self.ct.toMgrs(pt4326.y(), pt4326.x())
        except:
            mgrsCoords = None

        return mgrsCoords

# Mgrs 54SVG999574 / zone:'54', letters:'SVG', easting: '999', northing: '574'
# The function Break_Mgrs_String breaks down an Mgrs
# coordinate string into its component parts.
#   Mgrs           : Mgrs coordinate string          (input)
#   Zone           : UTM Zone                        (output)
#   Letters        : Mgrs coordinate string letters  (output)
#   Easting        : Easting value                   (output)
#   Northing       : Northing value                  (output)
#   Precision      : Precision level of Mgrs string  (output)

  def parseMgrs(self, mgrs):
        m = re_mgrs.match(mgrs)
        zone = m.group(0)
        letters = m.group(1)
        nums = m.group(2)
        precision = len(nums) / 2
        if precision>0:
            Easting = nums[0:precision]
            Northing = nums[precision+1,precision*2]
        else:
            Easting = ''
            Northing = ''

        return ( zone, letters, easting, nothing, precision )
