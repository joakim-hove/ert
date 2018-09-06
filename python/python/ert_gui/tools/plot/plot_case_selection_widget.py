import sys

try:
  from PyQt4.QtCore import pyqtSignal, QSignalMapper, Qt
  from PyQt4.QtGui import QWidget, QVBoxLayout, QHBoxLayout, QToolButton, QComboBox
except ImportError:
  from PyQt5.QtCore import pyqtSignal, QSignalMapper, Qt
  from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QToolButton, QComboBox


from ert_gui.ertwidgets import resourceIcon
from ert_gui.tools.plot import PlotCaseModel


class CaseSelectionWidget(QWidget):

    caseSelectionChanged = pyqtSignal()

    def __init__(self, current_case):
        QWidget.__init__(self)
        print "Creating widget: CaseSelectionWidget"
        self.__model = PlotCaseModel()

        self.__signal_mapper = QSignalMapper(self)
        self.__case_selectors = {}
        self.__case_selectors_order = []

        layout = QVBoxLayout()

        add_button_layout = QHBoxLayout()
        self.__add_case_button = QToolButton()
        self.__add_case_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.__add_case_button.setText("Add case to plot")
        self.__add_case_button.setIcon(resourceIcon("ide/small/add"))
        self.__add_case_button.clicked.connect(self.addCaseSelector)

        # OK Her
        add_button_layout.addStretch()
        add_button_layout.addWidget(self.__add_case_button)
        add_button_layout.addStretch()

        layout.addLayout(add_button_layout)

        self.__case_layout = QVBoxLayout()
        self.__case_layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(self.__case_layout)

        #OK Her
        # Det er addCaseSelector som feiler
        self.addCaseSelector(disabled=True, current_case=current_case)
        layout.addStretch()
        #Feiler her

        self.setLayout(layout)
        self.__signal_mapper.mapped[QWidget].connect(self.removeWidget)
        print "Widget CaseSelectionWidget complete"

    def __caseName(self, widget):
        """ @rtype: str """
        return str(self.__case_selectors[widget].currentText())

    def getPlotCaseNames(self):
        if self.__model.rowCount() == 0:
            return []

        return [self.__caseName(widget) for widget in self.__case_selectors_order]

    def checkCaseCount(self):
        state = True
        if len(self.__case_selectors_order) == 5:
            state = False

        self.__add_case_button.setEnabled(state)


    def addCaseSelector(self, disabled=False, current_case=None):
        print "Starter: addCaseSelector: %s" % current_case
        widget = QWidget()

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(layout)

        # Return here is OK
        combo = QComboBox()
        combo.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLengthWithIcon)
        # Return here isi OK
        combo.setMinimumContentsLength(20)
        print "Calling setModel: %s" % self.__model

        combo.setModel(self.__model)
        # Feiler her
        return

        if current_case is not None:
            index = 0
            for item in self.__model:
                if item == current_case:
                    combo.setCurrentIndex(index)
                    break
                index += 1

        combo.currentIndexChanged.connect(self.caseSelectionChanged.emit)
        # Feiler her

        layout.addWidget(combo, 1)

        button = QToolButton()
        button.setAutoRaise(True)
        button.setDisabled(disabled)
        button.setIcon(resourceIcon("ide/small/delete"))
        button.clicked.connect(self.__signal_mapper.map)

        layout.addWidget(button)

        self.__case_selectors[widget] = combo
        self.__case_selectors_order.append(widget)
        self.__signal_mapper.setMapping(button, widget)

        self.__case_layout.addWidget(widget)

        self.checkCaseCount()
        self.caseSelectionChanged.emit()
        print "AddCaseSelector complete"


    def removeWidget(self, widget):
        self.__case_layout.removeWidget(widget)
        del self.__case_selectors[widget]
        self.__case_selectors_order.remove(widget)
        widget.setParent(None)
        self.caseSelectionChanged.emit()

        self.checkCaseCount()

