import os
import pytest
from pytestqt.qtbot import QtBot
from PySide2 import QtCore, QtWidgets, QtGui
from qtgrab.shot_widget import ShotWidget
from qtgrab.coordinates_widget import CoordinateWidget


@pytest.mark.parametrize(
    'p1, p2, expected_height, expected_width',
    [(QtCore.QPoint(100, 100), QtCore.QPoint(200, 200), 100, 100)])
def test_assumed_integration(
        qtbot, monkeypatch, p1, p2, expected_height, expected_width):
    """
    Test the assumed integration of the ShotWidget.
    :param QtBot qtbot:
    :param MonkeyPatch monkeypatch:
    :param QtCore.QPoint p1:
    :param QtCore.QPoint p2:
    :param int expected_height:
    :param int expected_width:
    :return: None
    """
    shot_widget = ShotWidget()
    # mock the coordinate grabbing dialog
    monkeypatch.setattr(
        shot_widget, 'get_coordinates',
        lambda : (p1, p2))

    qtbot.addWidget(shot_widget)

    btn_trigger = QtWidgets.QPushButton()
    btn_trigger.clicked.connect(shot_widget.capture_screen)
    qtbot.addWidget(btn_trigger)

    # test if no screenshot has been made
    assert shot_widget._pmp_screen_grab is None
    qtbot.mouseClick(btn_trigger, QtCore.Qt.LeftButton)

    # test if a screenshot was made
    assert isinstance(shot_widget._pmp_screen_grab, QtGui.QPixmap)

    # test if the screenshot has the expected size
    img_height = shot_widget._pmp_screen_grab.height()
    img_width = shot_widget._pmp_screen_grab.width()

    assert img_height == pytest.approx(expected_height, 1)
    assert img_width == pytest.approx(expected_width, 1)


@pytest.mark.parametrize(
    'p1, p2', [(QtCore.QPoint(100, 100), None),
               (None, QtCore.QPoint(100, 100)),
               (None, None)])
def test_coordinate_canceling(qtbot, monkeypatch, p1, p2):
    """
    Test if failed coordinate grabbing actually cancels the screen grabbing.
    :param QtBot qtbot:
    :param MonkeyPatch monkeypatch:
    :param QtCore.QPoint p1:
    :param QtCore.QPoint p2:
    :return: None
    """
    shot_widget = ShotWidget()
    # mock the coordinate grabbing dialog
    monkeypatch.setattr(
        shot_widget, 'get_coordinates',
        lambda : (p1, p2))

    qtbot.addWidget(shot_widget)

    btn_trigger = QtWidgets.QPushButton()
    btn_trigger.clicked.connect(shot_widget.capture_screen)
    qtbot.addWidget(btn_trigger)

    # test if no screenshot has been made
    qtbot.mouseClick(btn_trigger, QtCore.Qt.LeftButton)
    assert shot_widget._pmp_screen_grab is None


def test_default_coordinate_grabbing(qtbot, monkeypatch):
    """
    Test if no ratio constraining is enforced by default.
    :param QtBot qtbot:
    :param MonkeyPatch monkeypatch:
    :return: None
    """
    def mocked_coordinate_getting(enable_constraint, ratio):
        assert enable_constraint is False
        assert ratio == 1

    monkeypatch.setattr(
        CoordinateWidget, 'get_coordinates', mocked_coordinate_getting)

    shot_widget = ShotWidget()
    qtbot.addWidget(shot_widget)

    shot_widget.get_coordinates()

    # disabling the ratio constraint shouldn't make a difference
    shot_widget.disable_image_ratio_constraint()
    shot_widget.get_coordinates()


def test_coordinate_grabbing_options(qtbot, monkeypatch):
    """
    Test if options are used as expected.
    :param QtBot qtbot:
    :param MonkeyPatch monkeypatch:
    :return: None
    """
    def mocked_coordinate_getting(enable_constraint, ratio):
        assert enable_constraint is True
        assert ratio == 5

    monkeypatch.setattr(
        CoordinateWidget, 'get_coordinates', mocked_coordinate_getting)

    shot_widget = ShotWidget()
    qtbot.addWidget(shot_widget)

    shot_widget.enable_image_ratio_constraint()
    shot_widget.set_image_ratio(5)
    shot_widget.get_coordinates()


def test_resizing(qtbot):
    """
    Simply test if resizing doesn't trigger any errors
    :param QtBot qtbot:
    :return: None
    """
    shot_widget = ShotWidget()
    qtbot.addWidget(shot_widget)

    event = QtGui.QResizeEvent(QtCore.QSize(200, 200), shot_widget.size())
    shot_widget.resizeEvent(event)


def test_image_save_failing(qtbot, tmpdir):
    """
    Test if image saving fails if no grab has been made
    :param QtBot qtbot:
    :param LocalPath tmpdir:
    :return: None
    """
    shot_widget = ShotWidget()
    qtbot.addWidget(shot_widget)

    test_path = os.path.join(str(tmpdir), '.png')

    with pytest.raises(ValueError):
        shot_widget.save_capture(test_path)


def test_image_save(qtbot, tmpdir, monkeypatch):
    """
    Test image saving.
    :param QtBot qtbot:
    :param LocalPath tmpdir:
    :param MonkeyPatch monkeypatch:
    :return: None
    """
    shot_widget = ShotWidget()
    qtbot.addWidget(shot_widget)
    test_path = os.path.join(str(tmpdir), '.png')

    monkeypatch.setattr(
        shot_widget, 'get_coordinates',
        lambda : (QtCore.QPoint(100, 100), QtCore.QPoint(300, 200)))

    shot_widget.capture_screen()
    shot_widget.save_capture(test_path)

    assert os.path.isfile(test_path)
