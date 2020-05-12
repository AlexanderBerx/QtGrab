import copy
from PySide2 import QtWidgets, QtCore, QtGui


class CoordinateWidget(QtWidgets.QDialog):
    """
    CoordinateWidget, widget for marking an area. First left click for marking
    the top left corner you want to grab. Second left click for marking the
    bottom right corner.
    """

    def __init__(self):
        super(CoordinateWidget, self).__init__()
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)
        self.setMouseTracking(True)

        # properties
        self._unmarked_color = QtGui.QColor(0, 0, 0, 100)
        self._marked_color = QtGui.QColor(0, 0, 0, 1)
        self._line_color = QtGui.QColor(255, 0, 0, 200)

        self._mouse_pos = QtCore.QPoint(0, 0)
        self._marked_area = None
        self._constrain_image_ratio = False
        self._image_ratio = 1.0
        self._anchor_point = None
        self._top_corner = None
        self._bottom_corner = None

    @property
    def top_corner(self):
        """
        The top left corner of the marked area.
        :return: QtCore.QPoint
        """
        return self._top_corner

    @property
    def bottom_corner(self):
        """
        The bottom right corner of the marked area.
        :return: QtCore.QPoint
        """
        return self._bottom_corner

    def set_image_ratio(self, value):
        """
        Set the image ratio.
        :param float value: image ratio
        :return: None
        """
        self._image_ratio = float(value)

    def enable_ratio_constraint(self):
        """
        Enables the ratio constraint.
        :return: None
        """
        self._constrain_image_ratio = True

    def disable_ratio_constraint(self):
        """
        Disables the ratio constraint.
        :return: None
        """
        self._constrain_image_ratio = False

    def _calculate_marked_area(self, anchor_point, offset_point):
        """
        Calculate the marked area between the given anchor point and offset
        point.
        :param QtCore.QPoint anchor_point:
        :param QtCore.QPoint offset_point:
        :return: QtCore.QRect
        """
        marked_area = self._get_area_between_points(
            anchor_point, offset_point)

        if self._constrain_image_ratio:
            marked_area.setWidth(
                int(marked_area.height() * self._image_ratio))

            # move towards the cursor
            new_pos = copy.copy(anchor_point)

            if offset_point.x() > anchor_point.x():
                new_pos.setX(new_pos.x() - marked_area.width())

            if offset_point.y() > anchor_point.y():
                new_pos.setY(new_pos.y() - marked_area.height())

            marked_area.moveTo(new_pos)

        return marked_area

    def mouseMoveEvent(self, event):
        """
        Triggers on mouse move events. The mouse position is stored and the
        widget is repainted.
        :param QtGui.QMouseEvent event: mouse event
        :return: None
        """
        # update the mouse position
        self._mouse_pos.setX(event.x())
        self._mouse_pos.setY(event.y())

        # calculate the marked area
        if self._anchor_point is not None:
            result = self._calculate_marked_area(
                self._anchor_point, event.pos())
            self._marked_area = result

        # repaint the widget
        self.update()

        super(CoordinateWidget, self).mouseMoveEvent(event)

    def mousePressEvent(self, event):
        """
        React to left mouse button clicks. On the first click the top left
        corner is stored. On the second click the bottom right corner will be
        stored and the widget will close itself. On right clicks the top corner
        will be reset.
        :param QtGui.QMouseEvent event: mouse event
        :return: None
        """
        if QtCore.Qt.LeftButton == event.button():
            if self._anchor_point is None:
                self._anchor_point = event.pos()
            else:
                self._marked_area = self._calculate_marked_area(
                    self._anchor_point, event.pos())
                self._calc_corners()
                self.close()
        elif QtCore.Qt.RightButton == event.button():
            self._anchor_point = None
            self.repaint()

    def _calc_corners(self):
        """
        Caculate the corners of the marked area.
        :return: None
        """
        self._top_corner = self._marked_area.bottomRight()
        self._bottom_corner = self._marked_area.topLeft()

    def _paint_lines_without_anchor(self, painter):  # pragma: no cover
        """
        Paint the cursor reference lines without an anchor point.
        :param QtGui.QPainter painter: painter object to paint on
        :return: None
        """
        pen = QtGui.QPen(self._line_color, 2, QtCore.Qt.SolidLine)
        painter.setPen(pen)
        # from the right
        painter.drawLine(
            0, self._mouse_pos.y(), self.width(), self._mouse_pos.y())
        # from bottom
        painter.drawLine(
            self._mouse_pos.x(), 0, self._mouse_pos.x(), self.height())

    def _paint_lines_marked_area(self, painter):  # pragma: no cover
        """
        Paint the reference lines according to the marked area.
        :param QtGui.QPainter painter: painter object to paint on
        :return: None
        """
        pen = QtGui.QPen(self._line_color, 2, QtCore.Qt.SolidLine)
        painter.setPen(pen)

        bottom_x = self._marked_area.x()
        bottom_y = self._marked_area.y()
        top_x = self._marked_area.right()
        top_y = self._marked_area.bottom()

        # paint left to right line
        painter.drawLine(0, bottom_y, bottom_x, bottom_y)
        # paint top to bottom line
        painter.drawLine(bottom_x, 0, bottom_x, bottom_y)
        # paint right to left line
        painter.drawLine(self.width(), top_y, top_x, top_y)
        # paint bottom to top line
        painter.drawLine(top_x, self.height(), top_x, top_y)

    def _paint_cursor_lines(self, painter):  # pragma: no cover
        """
        paint the lines indicating the marked area.
        :param QtGui.QPainter painter: painter object to paint on
        :return: None
        """
        if self._anchor_point is None:
            self._paint_lines_without_anchor(painter)
        else:
            self._paint_lines_marked_area(painter)

    def _paint_regions(self, painter):  # pragma: no cover
        """
        Paint the marked and unmarked regions.
        :param QtGui.QPainter painter: painter object to paint on
        :return: None
        """
        if self._anchor_point is None:
            # no area is yet marked so just fill the entire background
            painter.fillRect(
                0, 0, self.width(), self.height(), self._unmarked_color)
        else:
            # marked region
            marked_region = self._marked_area
            painter.fillRect(marked_region, self._marked_color)

            # paint the left region
            left_region = self._get_area_between_points(
                QtCore.QPoint(0, 0), marked_region.topRight())
            painter.fillRect(left_region, self._unmarked_color)

            # paint the upper region
            upper_region = self._get_area_between_points(
                QtCore.QPoint(marked_region.right(), 0),
                QtCore.QPoint(self.width(), marked_region.bottom()))
            painter.fillRect(upper_region, self._unmarked_color)

            # paint the right region
            right_region = self._get_area_between_points(
                QtCore.QPoint(marked_region.left(), marked_region.bottom()),
                QtCore.QPoint(self.width(), self.height()))
            painter.fillRect(right_region, self._unmarked_color)

            # paint the bottom region
            bottom_region = self._get_area_between_points(
                QtCore.QPoint(0, marked_region.top()),
                QtCore.QPoint(marked_region.left(), self.height()))
            painter.fillRect(bottom_region, self._unmarked_color)

    def _get_area_between_points(self, p1, p2):
        """
        Calculate the are between two given points.
        :param QtCore.QPoint p1:
        :param QtCore.QPoint p2:
        :return: QtCore.QRect
        """
        y_upper = p1.y() if p1.y() < p2.y() else p2.y()
        y_lower = p2.y() if p2.y() > p1.y() else p1.y()

        x_upper = p1.x() if p1.x() < p2.x() else p2.x()
        x_lower = p2.x() if p2.x() > p1.x() else p1.x()

        area = QtCore.QRect(
            x_lower, y_lower, x_upper - x_lower, y_upper - y_lower)
        return area

    def paintEvent(self, event):  # pragma: no cover
        """
        Paint the widget.
        :param QtGui.QPaintEvent event:
        :return: None
        """
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)

        self._paint_regions(painter)
        self._paint_cursor_lines(painter)

        painter.end()

    @classmethod
    def get_coordinates(
            cls, enable_constraint=False, ratio=1):  # pragma: no cover
        inst = cls()

        if enable_constraint:
            inst.enable_ratio_constraint()
            inst.set_image_ratio(ratio)

        inst.showFullScreen()
        inst.exec_()
        return inst.top_corner, inst.bottom_corner
