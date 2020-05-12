from PySide2 import QtWidgets, QtCore, QtGui
from qtgrab.coordinates_widget import CoordinateWidget


class ShotWidget(QtWidgets.QLabel):
    """
    ShotWidget, widget for taking screen shots/grabs. This is mainly a widget
    with a label to display the images of taken screen shot. No button is
    provided for triggering the screenshot action so this can be implemented
    by whoever implements this widget.
    """
    def __init__(self):
        super(ShotWidget, self).__init__()

        self._pmp_screen_grab = None
        self._constrain_image_ratio = False
        self._image_ratio = 1

        # note: a minimum size is needed since without one the widget wouldn't
        # be able to downscale
        self.setMinimumSize(1, 1)

        # set the background
        default_pmp = QtGui.QPixmap(300, 200)
        default_pmp.fill(QtGui.QColor(128, 128, 128))
        self.setPixmap(default_pmp)

    def enable_image_ratio_constraint(self):
        """
        Enables the image ratio constraint when making a screenshot.
        :return: None
        """
        self._constrain_image_ratio = True

    def disable_image_ratio_constraint(self):
        """
        Disable the image ratio constraint when making a screenshot.
        :return: None
        """
        self._constrain_image_ratio = False

    def set_image_ratio(self, value):
        """
        Set the image ratio constraint value
        :param float value: ratio value
        :return: None
        """
        self._image_ratio = float(value)

    def get_coordinates(self):
        """
        Creates a CoordinateWidget dialog for grabbing the coordinates.
        :return: None
        """
        return CoordinateWidget.get_coordinates(
            self._constrain_image_ratio, self._image_ratio)

    def _update_pixmap_size(self):
        """
        Update the current pixmap size to the size of the widget.
        :return: None
        """
        pmp = self.pixmap()
        if self._pmp_screen_grab is not None:
            pmp = self._pmp_screen_grab

        self.setPixmap(pmp.scaled(
            self.size(), QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation))

    @QtCore.Slot()
    def capture_screen(self):
        """
        Start a screen capture.
        :return: None
        """
        top_corner, bottom_corner = self.get_coordinates()
        if top_corner is None or bottom_corner is None:
            return

        width = bottom_corner.x() - top_corner.x()
        height = bottom_corner.y() - top_corner.y()

        # clear out the previous image
        self._pmp_screen_grab = None
        screen = QtWidgets.QApplication.primaryScreen()
        self._pmp_screen_grab = screen.grabWindow(
            QtWidgets.QApplication.desktop().winId(),
            top_corner.x(),
            top_corner.y(),
            width,
            height)
        self._update_pixmap_size()

    def save_capture(self, file_path):
        """
        Shorthand method for saving the screen capture to the given file path.
        :param file_path:
        :raise ValueError: When no screen grab has been made
        :return: bool
        """
        if self._pmp_screen_grab is not None:
            return self._pmp_screen_grab.save(file_path)
        raise ValueError('No Screen grab has yet been made')

    def resizeEvent(self, event):
        """
        Overwritten method from QWidget to also update the pixmap size.
        :param QtGui.QResizeEvent event:
        :return: None
        """
        # update the image scale
        self._update_pixmap_size()
        super(ShotWidget, self).resizeEvent(event)
