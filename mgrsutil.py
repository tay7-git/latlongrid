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
import mgrs
import re

class MgrsTool():
    ct = mgrs.MGRS()
    epsg4326 = core.QgsCoordinateReferenceSystem("EPSG:4326")
    re_mgrs = re.compile('([0-9]{1,2})([A-Z]+)([0-9]*)')

    def toMGRS(self, crs, pt):

        transform = core.QgsCoordinateTransform(crs, self.epsg4326)
        pt4326 = transform.transform(pt)

        try:
            mgrsCoords = self.ct.toMGRS(pt4326.y(), pt4326.x())
        except:
#            mgrsCoords = "pt4326: x={0:.3f},y={1:.3f}".format(pt4326.x(), pt4326.y())
            mgrsCoords = None

        return mgrsCoords

    def toEeasting(self, crs, pt):
        m = self.toMGRS(crs, pt)
        zone, letters, easting, northing, precision = self.parseMGRS(m)
        return easting

    def toNorthing(self, crs, pt):
        m = self.toMGRS(crs, pt)
        zone, letters, easting, northing, precision = self.parseMGRS(m)
        return northing

    def toPrecision(self, crs, pt):
        m = self.toMGRS(crs, pt)
        zone, letters, easting, northing, precision = self.parseMGRS(m)
        return precision

# Mgrs 54SVG999574 / zone:'54', letters:'SVG', easting: '999', northing: '574'
# The function Break_Mgrs_String breaks down an Mgrs
# coordinate string into its component parts.
#   Mgrs           : Mgrs coordinate string          (input)
#   Zone           : UTM Zone                        (output)
#   Letters        : Mgrs coordinate string letters  (output)
#   Easting        : Easting value                   (output)
#   Northing       : Northing value                  (output)
#   Precision      : Precision level of Mgrs string  (output)

    def parseMGRS(self, mgrs):
        m = self.re_mgrs.match(mgrs)
        zone = m.group(1)
        letters = m.group(2)
        nums = m.group(3)
        precision = len(nums) / 2
        if precision>0:
            easting = nums[0:precision]
            northing = nums[precision+1:precision*2]
        else:
            easting = ''
            northing = ''

        return zone, letters, easting, northing, precision
