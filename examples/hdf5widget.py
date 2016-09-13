# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2004-2016 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/
"""Qt Hdf5 widget examples

.. note:: This module has a dependency on the `h5py <http://www.h5py.org/>`_
    library, which is not a mandatory dependency for `silx`. You might need
    to install it if you don't already have it.
"""

import os
import sys
import numpy
import logging
from silx.gui import qt
import silx.gui.hdf5
from silx.gui.widgets.ThreadPoolPushButton import ThreadPoolPushButton
import html
import h5py
import tempfile

try:
    import fabio
except ImportError:
    fabio = None


_logger = logging.getLogger(__name__)
"""Module logger"""


_file_cache = {}


def get_hdf5_with_all_types():
    global _file_cache
    ID = "alltypes"
    if ID in _file_cache:
        return _file_cache[ID].name

    tmp = tempfile.NamedTemporaryFile(prefix=ID + "_", suffix=".h5", delete=True)
    h5 = h5py.File(tmp.name, "w")

    g = h5.create_group("arrays")
    g.create_dataset("scalar", data=10)
    g.create_dataset("list", data=[10])
    g.create_dataset("image", data=[[10]])
    g.create_dataset("cube", data=[[[10]]])
    g.create_dataset("hypercube", data=[[[[10]]]])

    g = h5.create_group("dtypes")
    g.create_dataset("int32", data=numpy.int32(10))
    g.create_dataset("int64", data=numpy.int64(10))
    g.create_dataset("float32", data=numpy.float32(10))
    g.create_dataset("float64", data=numpy.float64(10))
    g.create_dataset("string_", data=numpy.string_("Hi!"))
    #g.create_dataset("string0",data=numpy.string0("Hi!\x00"))

    g.create_dataset("bool", data=True)
    g.create_dataset("bool2", data=False)
    h5.close()

    _file_cache[ID] = tmp
    return tmp.name


def get_hdf5_with_all_links():
    global _file_cache
    ID = "alllinks"
    if ID in _file_cache:
        return _file_cache[ID].name

    tmp = tempfile.NamedTemporaryFile(prefix=ID + "_", suffix=".h5", delete=True)
    h5 = h5py.File(tmp.name, "w")

    g = h5.create_group("group")
    g.create_dataset("dataset", data=numpy.int64(10))
    h5.create_dataset("dataset", data=numpy.int64(10))

    h5["hard_link_to_group"] = h5["/group"]
    h5["hard_link_to_dataset"] = h5["/dataset"]

    h5["soft_link_to_group"] = h5py.SoftLink("/group")
    h5["soft_link_to_dataset"] = h5py.SoftLink("/dataset")
    h5["soft_link_to_nothing"] = h5py.SoftLink("/foo/bar/2000")

    alltypes_filename = get_hdf5_with_all_types()

    h5["external_link_to_group"] = h5py.ExternalLink(alltypes_filename, "/arrays")
    h5["external_link_to_dataset"] = h5py.ExternalLink(alltypes_filename, "/arrays/cube")
    h5["external_link_to_nothing"] = h5py.ExternalLink(alltypes_filename, "/foo/bar/2000")
    h5["external_link_to_missing_file"] = h5py.ExternalLink("missing_file.h5", "/")
    h5.close()

    _file_cache[ID] = tmp
    return tmp.name


def get_hdf5_with_1000_datasets():
    global _file_cache
    ID = "dataset1000"
    if ID in _file_cache:
        return _file_cache[ID].name

    tmp = tempfile.NamedTemporaryFile(prefix=ID + "_", suffix=".h5", delete=True)
    h5 = h5py.File(tmp.name, "w")

    g = h5.create_group("group")
    for i in range(1000):
        g.create_dataset("dataset%i" % i, data=numpy.int64(10))
    h5.close()

    _file_cache[ID] = tmp
    return tmp.name


def get_hdf5_with_10000_datasets():
    global _file_cache
    ID = "dataset10000"
    if ID in _file_cache:
        return _file_cache[ID].name

    tmp = tempfile.NamedTemporaryFile(prefix=ID + "_", suffix=".h5", delete=True)
    h5 = h5py.File(tmp.name, "w")

    g = h5.create_group("group")
    for i in range(10000):
        g.create_dataset("dataset%i" % i, data=numpy.int64(10))
    h5.close()

    _file_cache[ID] = tmp
    return tmp.name


def get_hdf5_with_100000_datasets():
    global _file_cache
    ID = "dataset100000"
    if ID in _file_cache:
        return _file_cache[ID].name

    tmp = tempfile.NamedTemporaryFile(prefix=ID + "_", suffix=".h5", delete=True)
    h5 = h5py.File(tmp.name, "w")

    g = h5.create_group("group")
    for i in range(100000):
        g.create_dataset("dataset%i" % i, data=numpy.int64(10))
    h5.close()

    _file_cache[ID] = tmp
    return tmp.name


def get_edf_with_all_types():
    global _file_cache
    ID = "alltypesedf"
    if ID in _file_cache:
        return _file_cache[ID].name

    tmp = tempfile.NamedTemporaryFile(prefix=ID + "_", suffix=".edf", delete=True)

    header = fabio.fabioimage.OrderedDict()
    header["integer"] = "10"
    header["float"] = "10.5"
    header["string"] = "Hi!"
    header["integer_list"] = "10 20 50"
    header["float_list"] = "1.1 3.14 500.12"
    header["motor_pos"] = "10 2.5 a1"
    header["motor_mne"] = "integer_position float_position named_position"

    data = numpy.array([[10, 50],[50, 10]])
    fabiofile = fabio.edfimage.EdfImage(data, header)
    fabiofile.write(tmp.name)

    _file_cache[ID] = tmp
    return tmp.name

def get_edf_with_100000_frames():
    global _file_cache
    ID = "frame100000"
    if ID in _file_cache:
        return _file_cache[ID].name

    tmp = tempfile.NamedTemporaryFile(prefix=ID + "_", suffix=".edf", delete=True)

    fabiofile = None
    for framre_id in range(100000):
        data = numpy.array([[framre_id, 50],[50, 10]])
        if fabiofile is None:
            header = fabio.fabioimage.OrderedDict()
            header["nb_frames"] = "100000"
            fabiofile = fabio.edfimage.EdfImage(data, header)
        else:
            header = fabio.fabioimage.OrderedDict()
            header["frame_nb"] = framre_id
            fabiofile.appendFrame(fabio.edfimage.Frame(data, header, framre_id))
    fabiofile.write(tmp.name)

    _file_cache[ID] = tmp
    return tmp.name


class Hdf5TreeViewExample(qt.QMainWindow):
    """
    This window show an example of use of a Hdf5TreeView.

    The tree is initialized with a list of filenames. A panel allow to play
    with internal property configuration of the widget, and a text screen
    allow to display events.
    """

    def __init__(self, filenames=None):
        """
        :param files_: List of HDF5 or Spec files (pathes or
            :class:`silx.io.spech5.SpecH5` or :class:`h5py.File`
            instances)
        """
        qt.QMainWindow.__init__(self)
        self.setWindowTitle("Silx HDF5 widget example")

        self.__asyncload = False
        self.__treeview = silx.gui.hdf5.Hdf5TreeView()
        """Silx HDF5 TreeView"""
        self.__text = qt.QTextEdit(self)
        """Widget displaying information"""

        spliter = qt.QSplitter()
        spliter.addWidget(self.__treeview)
        spliter.addWidget(self.__text)
        spliter.setStretchFactor(1, 1)

        main_panel = qt.QWidget(self)
        layout = qt.QVBoxLayout()
        layout.addWidget(spliter)
        layout.addWidget(self.createTreeViewConfigurationPanel(self, self.__treeview))
        layout.setStretchFactor(spliter, 1)
        main_panel.setLayout(layout)

        self.setCentralWidget(main_panel)

        # append all files to the tree
        for file_name in filenames:
            self.__treeview.model().appendFile(file_name)

        self.__treeview.activated.connect(lambda index: self.displayEvent("activated", index))
        self.__treeview.clicked.connect(lambda index: self.displayEvent("clicked", index))
        self.__treeview.doubleClicked.connect(lambda index: self.displayEvent("doubleClicked", index))
        self.__treeview.entered.connect(lambda index: self.displayEvent("entered", index))
        self.__treeview.pressed.connect(lambda index: self.displayEvent("pressed", index))

        self.__treeview.addContextMenuCallback(self.customContextMenu)
        # lamba function will never be called cause we store it as weakref
        self.__treeview.addContextMenuCallback(lambda event: None)
        # you have to store it first
        self.__store_lambda = lambda event: self.anotherCustomContextMenu(event)
        self.__treeview.addContextMenuCallback(self.__store_lambda)

    def displayEvent(self, eventName, index):

        def formatKey(name, value):
            name, value = html.escape(str(name)), html.escape(str(value))
            return "<li><b>%s</b>: %s</li>" % (name, value)

        text = "<html>"
        text += "<h1>Event</h1>"
        text += "<ul>"
        text += formatKey("name", eventName)
        text += formatKey("index", type(index))
        text += "</ul>"

        text += "<h1>Selected HDF5 objects</h1>"

        for h5py_obj in self.__treeview.selectedH5pyObjects():
            text += "<h2>HDF5 object</h2>"
            text += "<ul>"
            text += formatKey("filename", h5py_obj.file.filename)
            text += formatKey("basename", h5py_obj.name.split("/")[-1])
            text += formatKey("hdf5name", h5py_obj.name)
            text += formatKey("obj", type(h5py_obj))
            text += formatKey("dtype", getattr(h5py_obj, "dtype", None))
            text += formatKey("shape", getattr(h5py_obj, "shape", None))
            text += formatKey("attrs", getattr(h5py_obj, "attrs", None))
            if hasattr(h5py_obj, "attrs"):
                text += "<ul>"
                for key, value in h5py_obj.attrs.items():
                    text += formatKey(key, value)
                text += "</ul>"
            text += "</ul>"

        text += "</html>"
        self.__text.setHtml(text)

    def useAsyncLoad(self, useAsync):
        self.__asyncload = useAsync

    def __fileCreated(self, filename):
        if self.__asyncload:
            self.__treeview.model().insertFileAsync(filename)
        else:
            self.__treeview.model().insertFile(filename)

    def customContextMenu(self, event):
        """Called to populate the context menu

        :param silx.gui.hdf5.Hdf5ContextMenuEvent event: Event
            containing expected information to populate the context menu
        """
        selectedObjects = event.source().selectedH5pyObjects()
        menu = event.menu()

        hasDataset = False
        for object in selectedObjects:
            if hasattr(object, "value"):
                hasDataset = True
                break

        if len(menu.children()):
            menu.addSeparator()

        if hasDataset:
            action = qt.QAction("Do something on the datasets", event.source())
            menu.addAction(action)

    def anotherCustomContextMenu(self, event):
        """Called to populate the context menu

        :param silx.gui.hdf5.Hdf5ContextMenuEvent event: Event
            containing expected information to populate the context menu
        """
        selectedObjects = event.source().selectedH5pyObjects()
        menu = event.menu()

        if len(menu.children()):
            menu.addSeparator()

        for object in selectedObjects:
            if hasattr(object, "filename"):
                filename = os.path.basename(object.filename)
                action = qt.QAction("Do something on %s" % filename, event.source())
                menu.addAction(action)

    def __hdf5ComboChanged(self, index):
        function = self.__hdf5Combo.itemData(index)
        self.__createHdf5Button.setCallable(function)

    def __edfComboChanged(self, index):
        function = self.__edfCombo.itemData(index)
        self.__createEdfButton.setCallable(function)

    def createTreeViewConfigurationPanel(self, parent, treeview):
        """Create a configuration panel to allow to play with widget states"""
        panel = qt.QWidget(parent)
        panel.setLayout(qt.QHBoxLayout())

        content = qt.QGroupBox("Create HDF5", panel)
        content.setLayout(qt.QVBoxLayout())
        panel.layout().addWidget(content)

        combo = qt.QComboBox()
        combo.addItem("Containing all types", get_hdf5_with_all_types)
        combo.addItem("Containing all links", get_hdf5_with_all_links)
        combo.addItem("Containing 1000 datasets", get_hdf5_with_1000_datasets)
        combo.addItem("Containing 10000 datasets", get_hdf5_with_10000_datasets)
        combo.addItem("Containing 100000 datasets", get_hdf5_with_100000_datasets)
        combo.activated.connect(self.__hdf5ComboChanged)
        content.layout().addWidget(combo)

        button = ThreadPoolPushButton("Create")
        button.setCallable(combo.itemData(combo.currentIndex()))
        button.succeeded.connect(self.__fileCreated)
        content.layout().addWidget(button)

        self.__hdf5Combo = combo
        self.__createHdf5Button = button

        asyncload = qt.QCheckBox("Async load", content)
        asyncload.setChecked(self.__asyncload)
        asyncload.toggled.connect(lambda: self.useAsyncLoad(asyncload.isChecked()))
        content.layout().addWidget(asyncload)

        content.layout().addStretch(1)

        if fabio is not None:
            content = qt.QGroupBox("Create EDF", panel)
            content.setLayout(qt.QVBoxLayout())
            panel.layout().addWidget(content)

            combo = qt.QComboBox()
            combo.addItem("Containing all types", get_edf_with_all_types)
            combo.addItem("Containing 100000 datasets", get_edf_with_100000_frames)
            combo.activated.connect(self.__edfComboChanged)
            content.layout().addWidget(combo)

            button = ThreadPoolPushButton("Create")
            button.setCallable(combo.itemData(combo.currentIndex()))
            button.succeeded.connect(self.__fileCreated)
            content.layout().addWidget(button)

            self.__edfCombo = combo
            self.__createEdfButton = button

            content.layout().addStretch(1)

        option = qt.QGroupBox("Tree options", panel)
        option.setLayout(qt.QVBoxLayout())
        panel.layout().addWidget(option)

        multiselection = qt.QCheckBox("Multi-selection", option)
        multiselection.setChecked(treeview.selectionMode() == qt.QAbstractItemView.MultiSelection)
        switch_selection = lambda: treeview.setSelectionMode(
                qt.QAbstractItemView.MultiSelection if multiselection.isChecked()
                else qt.QAbstractItemView.SingleSelection)
        multiselection.toggled.connect(switch_selection)
        option.layout().addWidget(multiselection)

        filedrop = qt.QCheckBox("Drop external file", option)
        filedrop.setChecked(treeview.model().isFileDropEnabled())
        filedrop.toggled.connect(lambda: treeview.model().setFileDropEnabled(filedrop.isChecked()))
        option.layout().addWidget(filedrop)

        filemove = qt.QCheckBox("Reorder files", option)
        filemove.setChecked(treeview.model().isFileMoveEnabled())
        filemove.toggled.connect(lambda: treeview.model().setFileMoveEnabled(filedrop.isChecked()))
        option.layout().addWidget(filemove)

        option.layout().addStretch(1)

        option = qt.QGroupBox("Header options", panel)
        option.setLayout(qt.QVBoxLayout())
        panel.layout().addWidget(option)

        autosize = qt.QCheckBox("Auto-size headers", option)
        autosize.setChecked(treeview.header().hasAutoResizeColumns())
        autosize.toggled.connect(lambda: treeview.header().setAutoResizeColumns(autosize.isChecked()))
        option.layout().addWidget(autosize)

        columnpopup = qt.QCheckBox("Popup to hide/show columns", option)
        columnpopup.setChecked(treeview.header().hasHideColumnsPopup())
        columnpopup.toggled.connect(lambda: treeview.header().setEnableHideColumnsPopup(columnpopup.isChecked()))
        option.layout().addWidget(columnpopup)

        define_columns = qt.QComboBox()
        define_columns.addItem("Default columns", treeview.model().COLUMN_IDS)
        define_columns.addItem("Only name and Value", [treeview.model().NAME_COLUMN, treeview.model().VALUE_COLUMN])
        define_columns.activated.connect(lambda index: treeview.header().setSections(define_columns.itemData(index)))
        option.layout().addWidget(define_columns)

        option.layout().addStretch(1)

        panel.layout().addStretch(1)

        return panel


def main(filenames):
    """
    :param filenames: list of file paths
    """
    app = qt.QApplication([])
    window = Hdf5TreeViewExample(filenames)
    window.show()
    result = app.exec_()
    # remove ending warnings relative to QTimer
    app.deleteLater()
    sys.exit(result)


if __name__ == "__main__":
    main(sys.argv[1:])
