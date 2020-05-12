from qtgrab.coordinates_widget import CoordinateWidget
from pytestqt.qtbot import QtBot
from PySide2 import QtCore, QtGui
import pytest


def test_default_values(qtbot):
    """
    Test the default values from the coordinate widget.
    :param QtBot qtbot:
    :return: None
    """
    co_widget = CoordinateWidget()
    qtbot.addWidget(co_widget)

    # assert the start values are set to None
    assert co_widget.top_corner is None
    assert co_widget.bottom_corner is None


@pytest.mark.parametrize(
    'p1,p2', [(QtCore.QPoint(100, 100), QtCore.QPoint(200, 200))])
def test_top_down_coordinate_grabbing(qtbot, p1, p2):
    """
    Test coordinate grabbing when grabbing from the 'top' of the screen to
    the 'bottom' of the screen
    :param QtBot qtbot:
    :return: None
    """
    co_widget = CoordinateWidget()
    qtbot.addWidget(co_widget)

    qtbot.mouseClick(co_widget, QtCore.Qt.LeftButton, pos=p1)
    qtbot.mouseClick(co_widget, QtCore.Qt.LeftButton, pos=p2)

    assert co_widget.top_corner.x() == pytest.approx(p1.x(), 1)
    assert co_widget.top_corner.y() == pytest.approx(p1.y(), 1)

    assert co_widget.bottom_corner.x() == pytest.approx(p2.x(), 1)
    assert co_widget.bottom_corner.y() == pytest.approx(p2.y(), 1)


@pytest.mark.parametrize(
    'p1,p2', [(QtCore.QPoint(500, 500), QtCore.QPoint(200, 200))])
def test_bottom_up_coordinate_grabbing(qtbot, p1, p2):
    """
    Test coordinate grabbing when grabbing from the 'bottom' of the screen to
    the 'top' of the screen.
    :param QtBot qtbot:
    :return: None
    """
    co_widget = CoordinateWidget()
    qtbot.addWidget(co_widget)

    qtbot.mouseClick(co_widget, QtCore.Qt.LeftButton, pos=p1)
    qtbot.mouseClick(co_widget, QtCore.Qt.LeftButton, pos=p2)

    assert co_widget.top_corner.x() == pytest.approx(p2.x(), 1)
    assert co_widget.top_corner.y() == pytest.approx(p2.y(), 1)

    assert co_widget.bottom_corner.x() == pytest.approx(p1.x(), 1)
    assert co_widget.bottom_corner.y() == pytest.approx(p1.y(), 1)


@pytest.mark.parametrize('p', [(QtCore.QPoint(100, 100))])
def test_anchor_resetting(qtbot, p):
    """
    Test if the anchort point is properly reset when pressing the right mouse
    button
    :param QtBot qtbot:
    :param QtCore.QPoint p:
    :return: None
    """
    co_widget = CoordinateWidget()
    qtbot.addWidget(co_widget)

    assert co_widget._anchor_point is None
    qtbot.mouseClick(co_widget, QtCore.Qt.LeftButton, pos=p)

    # check if the first click is properly registered
    assert co_widget._anchor_point.x() == pytest.approx(p.x(), 1)
    assert co_widget._anchor_point.y() == pytest.approx(p.y(), 1)

    # reset the anchor point by right clicking
    qtbot.mouseClick(co_widget, QtCore.Qt.RightButton)
    assert co_widget._anchor_point is None


@pytest.mark.parametrize(
    'ratio, p1, p2, p3, p4', [
        (1.0, QtCore.QPoint(100, 100), QtCore.QPoint(300, 200),
         QtCore.QPoint(100, 100), QtCore.QPoint(200, 200)),
        (1.0, QtCore.QPoint(300, 200), QtCore.QPoint(100, 100),
         QtCore.QPoint(100, 100), QtCore.QPoint(200, 200))
    ])
def test_ratio_constraining(qtbot, ratio, p1, p2, p3, p4):
    """
    Test if the ratio constraint is properly enforced.
    :param QtBot qtbot:
    :param float ratio: image ratio
    :param QtCore.QPoint p1: First click point
    :param QtCore.QPoint p2: Second click point
    :param QtCore.QPoint p3: expected top position of the capture area
    :param QtCore.QPoint p4: expected bootm position of the capture area
    :return: None
    """
    co_widget = CoordinateWidget()
    qtbot.addWidget(co_widget)

    # co_widget.set_image_ratio(ratio)
    co_widget.enable_ratio_constraint()

    qtbot.mouseClick(co_widget, QtCore.Qt.LeftButton, pos=p1)
    qtbot.mouseClick(co_widget, QtCore.Qt.LeftButton, pos=p2)

    assert co_widget.top_corner.x() == pytest.approx(p3.x(), 1)
    assert co_widget.top_corner.y() == pytest.approx(p3.y(), 1)

    assert co_widget.bottom_corner.x() == pytest.approx(p4.x(), 1)
    assert co_widget.bottom_corner.y() == pytest.approx(p4.y(), 1)


def test_ratio_constraint_toggling(qtbot):
    """
    Test if ratio constraing is actually disabled.
    :param QtBot qtbot:
    :return: None
    """
    co_widget = CoordinateWidget()
    qtbot.addWidget(co_widget)

    p1 = QtCore.QPoint(100, 100)
    p2 = QtCore.QPoint(300, 200)
    p3 = QtCore.QPoint(200, 200)

    co_widget.set_image_ratio(1)
    co_widget.enable_ratio_constraint()

    qtbot.mouseClick(co_widget, QtCore.Qt.LeftButton, pos=p1)
    qtbot.mouseClick(co_widget, QtCore.Qt.LeftButton, pos=p2)

    assert co_widget.top_corner.x() == pytest.approx(p1.x(), 1)
    assert co_widget.top_corner.y() == pytest.approx(p1.y(), 1)

    assert co_widget.bottom_corner.x() == pytest.approx(p3.x(), 1)
    assert co_widget.bottom_corner.y() == pytest.approx(p3.y(), 1)

    co_widget.disable_ratio_constraint()

    qtbot.mouseClick(co_widget, QtCore.Qt.LeftButton, pos=p1)
    qtbot.mouseClick(co_widget, QtCore.Qt.LeftButton, pos=p2)

    assert co_widget.top_corner.x() == pytest.approx(p1.x(), 1)
    assert co_widget.top_corner.y() == pytest.approx(p1.y(), 1)

    assert co_widget.bottom_corner.x() == pytest.approx(p2.x(), 1)
    assert co_widget.bottom_corner.y() == pytest.approx(p2.y(), 1)


def test_mouse_movement_registering(qtbot):
    """
    Test if mouse move movements are properly stored.
    :param QtBot qtbot:
    :return: None
    """
    co_widget = CoordinateWidget()
    qtbot.addWidget(co_widget)

    p = QtCore.QPointF(100, 100)
    # simulate some mouse movement
    move_event = QtGui.QMouseEvent(
        QtCore.QEvent.Type.MouseMove,
        p,
        QtCore.Qt.MouseButton.NoButton,
        QtCore.Qt.MouseButtons(),
        QtCore.Qt.KeyboardModifiers()
    )

    co_widget.mouseMoveEvent(move_event)

    assert co_widget._mouse_pos.x() == pytest.approx(p.x(), 1)
    assert co_widget._mouse_pos.y() == pytest.approx(p.y(), 1)

    qtbot.mouseClick(
        co_widget, QtCore.Qt.LeftButton, pos=QtCore.QPoint(p.x(), p.y()))

    co_widget.mouseMoveEvent(move_event)
