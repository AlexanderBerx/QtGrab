from qtgrab.sample import SampleUi
from qtgrab.coordinates_widget import CoordinateWidget
from pytestqt.qtbot import QtBot
from PySide2 import QtCore, QtWidgets
import pytest
import os


@pytest.mark.parametrize(
    'p1, p2', [(QtCore.QPoint(100, 100), QtCore.QPoint(200, 300))])
def test_sample_widget(qtbot, monkeypatch, tmpdir, p1, p2):
    """
    Test if the sample widget can be instanced and be used as it is intended.
    :param QtBot qtbot:
    :param MonkeyPatch monkeypatch:
    :return: None
    """
    # monkeypatch coordinate getting
    monkeypatch.setattr(
        CoordinateWidget, 'get_coordinates',
        lambda *args: (p1, p2))
    # monkeypatch file dialog to return None
    monkeypatch.setattr(
        QtWidgets.QFileDialog, 'getSaveFileName',
        lambda *args, **kwargs: (None, ''))

    sample_widget = SampleUi()
    qtbot.addWidget(sample_widget)

    # try to save without making a capture
    qtbot.mouseClick(sample_widget.btn_save, QtCore.Qt.LeftButton)

    # monkeypatch file dialog to return a path
    monkeypatch.setattr(
        QtWidgets.QFileDialog, 'getSaveFileName',
        lambda *args, **kwargs: (os.path.join(str(tmpdir), 'test.png'), ''))

    # create a screen grab without changing any of the settings
    qtbot.mouseClick(sample_widget.btn_capture, QtCore.Qt.LeftButton)
    # save the capture
    qtbot.mouseClick(sample_widget.btn_save, QtCore.Qt.LeftButton)

    # turn on the ratio constraint
    sample_widget.toggle_ratio(True)
    # turn off the ratio constraint
    sample_widget.toggle_ratio(False)
    # set the image ratio
    sample_widget.set_ratio_value(1)
