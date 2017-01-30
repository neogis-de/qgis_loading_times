# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Loading_Times
                                 A QGIS plugin
 Measure how much time your plugins need to load
                              -------------------
        begin                : 2016-09-19
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Thomas Baumann
        email                : thomasfindichgut@gmx.de
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 
 Stopwatch Icon by Ilsur Aptukov from the Noun Project
 
"""
import pprint
import operator

# only for debugging
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# -----------


#from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
#from PyQt4.QtGui import QAction, QIcon
import qgis
from qgis.utils import plugin_times


# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from loading_time_dialog import Loading_TimesDialog
import os.path


class Loading_Times:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'Loading_Times_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = Loading_TimesDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Plugin Loading Times')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'Loading_Times')
        self.toolbar.setObjectName(u'Loading_Times')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('Loading_Times', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/Loading_Times/stopwatch.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Plugin Loading Times'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Plugin Loading Times'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        
        # show the dialog
        self.dlg.show()
        #print(self.dlg.loading_time_table)
        while self.dlg.loading_time_table.rowCount() > 0:
            #print(self.dlg.loading_time_table.rowCount())
            self.dlg.loading_time_table.removeRow(0);
        
        #self.dlg.loading_time_table.setRowCount(0);

        
        plugin_load_times= qgis.utils.plugin_times
        sorted_load_times = sorted(plugin_load_times.items(), key=operator.itemgetter(1))
        #print(len(sorted_load_times))
        self.dlg.loading_time_table.setRowCount(len(sorted_load_times))
        
        #reset order if user switched sorting manually
        self.dlg.loading_time_table.sortItems(1, Qt.AscendingOrder)
                
        self.dlg.loading_time_table.setHorizontalHeaderLabels([u'Name',u'Time'])
        
        plugin_items=dict(sorted_load_times)
        row = 0
        for name, time in plugin_items.iteritems():
            plugin_name = QTableWidgetItem(name)
            plugin_time = QTableWidgetItem(time)
            self.dlg.loading_time_table.setItem(row,0,plugin_name)
            self.dlg.loading_time_table.setItem(row,1,plugin_time)
            row += 1
        self.dlg.loading_time_table.sortItems(1, Qt.AscendingOrder)
        self.dlg.loading_time_table.resizeColumnsToContents()
        self.dlg.loading_time_table.horizontalHeader().setStretchLastSection(True)
        self.dlg.loading_time_table.setSortingEnabled(True)
        #scroll to row0 if user scrolled down manually
        #print(self.dlg.loading_time_table.item(1, 1))
        self.dlg.loading_time_table.scrollToItem(self.dlg.loading_time_table.item(1, 1), QAbstractItemView.PositionAtCenter)
        #print(dict(sorted_load_times))
        #pprint.pprint(sorted_load_times)
        

        
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
