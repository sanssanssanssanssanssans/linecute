import sys, os
from PySide6.QtCore import Qt
from PySide6.QtGui import QMovie
from PySide6.QtWidgets import QApplication, QLabel, QMenu

if getattr(sys, "frozen", False):
    BASE = sys._MEIPASS
else:
    BASE = os.path.dirname(__file__)

GIF_PATH = os.path.join(BASE, r"Line.gif")

class FloatingGif(QLabel):
    def __init__(self, gif_path):
        super().__init__()

        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setScaledContents(True)

        self.movie = QMovie(gif_path)
        self.setMovie(self.movie)
        self.movie.start()

        self.resize(320, 320)
        self.move(200, 200)
        
        self.drag_pos = None
        self.opacity = 1.0
        self.locked = False

    def mousePressEvent(self, e):
        if self.locked: return
        if e.button() == Qt.LeftButton:
            self.drag_pos = e.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        if self.locked: return
        if self.drag_pos and e.buttons() & Qt.LeftButton:
            self.move(e.globalPosition().toPoint() - self.drag_pos)

    def mouseReleaseEvent(self, e):
        self.drag_pos = None

    def wheelEvent(self, e):
        if self.locked: return
        if QApplication.keyboardModifiers() & Qt.ControlModifier:
            delta = 0.05 if e.angleDelta().y() > 0 else -0.05
            self.opacity = max(0.3, min(1.0, self.opacity + delta))
            self.setWindowOpacity(self.opacity)
        else:
            step = 30 if e.angleDelta().y() > 0 else -30
            w = max(80, self.width() + step)
            h = max(80, self.height() + step)
            self.resize(w, h)

    def contextMenuEvent(self, e):
        menu = QMenu(self)
        text_lock = "잠금 ✔" if self.locked else "잠금 ✘"
        act_lock = menu.addAction(text_lock)
        act_exit = menu.addAction("종료")
        act = menu.exec(e.globalPos())

        if act == act_exit:
            QApplication.quit()
        elif act == act_lock:
            self.locked = not self.locked

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = FloatingGif(GIF_PATH)
    w.show()
    sys.exit(app.exec())