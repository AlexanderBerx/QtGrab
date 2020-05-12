import sys
from PySide2 import QtWidgets, QtCore, QtGui
from qtgrab.shot_widget import ShotWidget


class SampleUi(QtWidgets.QWidget):
    """
    SampleUi, inherits from QWidget, demonstrates a possible use ot the
    ShotWidget
    """
    def __init__(self):
        super(SampleUi, self).__init__()
        self._create_ui()

    def _create_ui(self):
        """
        Create the widget's UI
        :return: None
        """
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        self._shot_widget = ShotWidget()

        # create and set a background image for the shot widget
        bg = QtGui.QPixmap(300, 200)
        bg.fill(QtGui.QColor(128, 128, 128))
        self._shot_widget.setPixmap(bg)
        layout.addWidget(self._shot_widget)

        # toggle the ratio constraint on and off
        self._chb_constrain_ratio = QtWidgets.QCheckBox(
            'Constrain Capture image ratio')
        self._chb_constrain_ratio.stateChanged[int].connect(self.toggle_ratio)
        layout.addWidget(self._chb_constrain_ratio)

        # control the ratio constraint amount
        ratio_layout = QtWidgets.QHBoxLayout()
        ratio_layout.addWidget(QtWidgets.QLabel('Ratio:'))
        self._spn_ratio = QtWidgets.QDoubleSpinBox()
        self._spn_ratio.setValue(1)
        self._spn_ratio.setSingleStep(0.01)
        self._spn_ratio.setEnabled(False)
        self._spn_ratio.valueChanged[float].connect(self.set_ratio_value)
        ratio_layout.addWidget(self._spn_ratio)

        layout.addLayout(ratio_layout)

        # capture button
        self.btn_capture = QtWidgets.QPushButton('Create Capture')
        layout.addWidget(self.btn_capture)
        self.btn_capture.clicked.connect(self._shot_widget.capture_screen)

        # save the capture button
        self.btn_save = QtWidgets.QPushButton('Save Capture')
        layout.addWidget(self.btn_save)
        self.btn_save.clicked.connect(self.save_capture)

    @QtCore.Slot(int)
    def toggle_ratio(self, state):
        """
        Set the ratio constraint to the given state
        :param int state:
        :return: None
        """
        state = bool(state)
        self._spn_ratio.setEnabled(state)
        if state:
            self._shot_widget.enable_image_ratio_constraint()
        else:
            self._shot_widget.disable_image_ratio_constraint()

    @QtCore.Slot(float)
    def set_ratio_value(self, value):
        """
        Set the ratio value
        :param float value:
        :return: None
        """
        self._shot_widget.set_image_ratio(value)

    @QtCore.Slot()
    def save_capture(self):
        """
        Save the screen grab to the selected file path.
        :return: None
        """
        file_path, file_filter = QtWidgets.QFileDialog.getSaveFileName(
            caption='Save the capture',
            filter='*.png'
        )
        if file_path is None:
            return

        self._shot_widget.save_capture(file_path)


def main():  # pragma: no cover
    app = QtWidgets.QApplication([])
    sample_window = SampleUi()
    sample_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()  # pragma: no cover
