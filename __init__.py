# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Loading_Times
                                 A QGIS plugin
 Measure how much time your plugins need to load
                             -------------------
        begin                : 2016-09-19
        copyright            : (C) 2016 by Thomas Baumann
        email                : thomasfindichgut@gmx.de
        git sha              : $Format:%H$
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


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load Loading_Times class from file Loading_Times.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .loading_time import Loading_Times
    return Loading_Times(iface)
