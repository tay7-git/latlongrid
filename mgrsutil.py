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

#for Debugging.
import sys
import pdb
# pdb.set_trace()

class MgrsTool():
    ct = mgrs.MGRS()
    epsg4326 = core.QgsCoordinateReferenceSystem("EPSG:4326")
    re_mgrs = re.compile('([0-9]{1,2})([A-Z]+)([0-9]*)')

    def toMGRS(self, crs, pt ,inDegrees=True, MGRSPrecision=5):

        transform = core.QgsCoordinateTransform(crs, self.epsg4326)
        pt4326 = transform.transform(pt)

        try:
            mgrsCoords = self.ct.toMGRS(pt4326.y(), pt4326.x(), inDegrees, MGRSPrecision)
        except:
#            mgrsCoords = "pt4326: x={0:.3f},y={1:.3f}".format(pt4326.x(), pt4326.y())
            mgrsCoords = None

        return mgrsCoords

    def toZone(self, crs, pt, inDegrees=True, MGRSPrecision=5):
        m = self.toMGRS(crs, pt, inDegrees, MGRSPrecision)
        (zone, letters, easting, northing, precision) = self.parseMGRS(m)
        return zone

    def toEeasting(self, crs, pt, inDegrees=True, MGRSPrecision=5):
        m = self.toMGRS(crs, pt, inDegrees, MGRSPrecision)
        (zone, letters, easting, northing, precision) = self.parseMGRS(m)
        return easting

    def toNorthing(self, crs, pt, inDegrees=True, MGRSPrecision=5):
        m = self.toMGRS(crs, pt, inDegrees, MGRSPrecision)
        (zone, letters, easting, northing, precision) = self.parseMGRS(m)
        return northing

    def toPrecision(self, crs, pt, inDegrees=True, MGRSPrecision=5):
        m = self.toMGRS(crs, pt, inDegrees, MGRSPrecision)
        (zone, letters, easting, northing, precision) = self.parseMGRS(m)
        return precision

    def toPoint(self, crs, MGRS, inDegrees=True):
        lat, lon = self.toLatLon(MGRS)
        transform4326 = core.QgsCoordinateTransform(self.epsg4326, crs)
        pt = transform4326.transform(lon, lat)
        return pt

    def toLatLon(self, MGRS, inDegrees=True):
        (lat, lon) = self.ct.toLatLon(MGRS, inDegrees)
        return (lat, lon)

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
        if mgrs is None:
            return (None,None,None,None,None)
        try:
            m = self.re_mgrs.match(mgrs)
        except:
            sys.stdout.write('parseMGRS("{0}") -> None\n'.format(mgrs))
            return (None,None,None,None,None)

        zone = m.group(1)
        letters = m.group(2)
        nums = m.group(3)
        precision = len(nums) / 2
        if precision > 0:
            easting = nums[0:precision]
            northing = nums[precision:precision*2]
        else:
            easting = ''
            northing = ''

        return (zone, letters, easting, northing, precision)
