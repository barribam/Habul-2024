from PyQt5 import QtWidgets, QtCore, QtGui

class CircularButton(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(50, 50)  # Establecer un tamaño fijo para que sea circular
        self.setStyleSheet("""
            QPushButton {
                border-radius: 25px;  
                background-image: url('Imagenes/logo.ico'); /* Cambiar la ruta de la imagen */
                background-repeat: no-repeat;
                background-position: center;
                background-size: contain; /* Ajustar la imagen para que quepa dentro del contenedor sin distorsionar */
                background-color: white;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.3); /* Cambiar el color de fondo al pasar el cursor */
            }
        """)
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))  # Cambiar el cursor al pasar sobre el botón
        self.drag_start_position = None  # Inicializar la posición de inicio del arrastre

    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.drag_start_position = event.pos()  # Registrar la posición de inicio del arrastre
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            delta = event.pos() - self.drag_start_position
            self.move(self.pos() + delta)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            # Obtener la posición final del ratón en relación con la ventana
            final_position = event.globalPos()
            # Calcular la distancia Manhattan entre la posición inicial y final
            manhattan_distance = (final_position - self.drag_start_position).manhattanLength()
            # Si la distancia es mayor que 40 píxeles, solo actualizamos la posición del botón
            if manhattan_distance > 40:
                self.move(event.globalPos())
            else:
                self.showNormal()  # Abrir la ventana de superposición si la distancia es menor que 40 píxeles
                super().mouseReleaseEvent(event)

    def open_overlay(self):
        # Emitir la señal para abrir la ventana
        self.window().show_overlay()

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Habul")
        self.resize(500, 200)
        
        # Establecer el icono de la ventana
        icon_path = "Imagenes/logo.ico"
        self.setWindowIcon(QtGui.QIcon(icon_path))
        
        # Establecer la ventana sin bordes y siempre visible
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowStaysOnTopHint)

        self.overlay_widget = None  # Inicializar el widget de superposición

        # Crear el widget central
        central_widget = QtWidgets.QWidget(self)  
        self.setCentralWidget(central_widget) 
        
        # Crear un layout para el contenido
        layout = QtWidgets.QVBoxLayout(central_widget)  
        
        # Ajustar los márgenes y espaciado del layout
        layout.setContentsMargins(20, 10, 20, 30)  
        layout.setSpacing(10)  # Ajustar el espaciado entre widgets
    
    
        label = QtWidgets.QLabel("Traductor de Lengua de señas a texto")
        
        label.setAlignment(QtCore.Qt.AlignCenter)  
        
        layout.addWidget(label, alignment=QtCore.Qt.AlignTop)  
        
        # Crear un contenedor (QFrame) con borde negro
        frame = QtWidgets.QFrame()  
        frame.setFrameShape(QtWidgets.QFrame.Box)  
        frame.setLineWidth(1)  
        
        layout.addWidget(frame, stretch=1)  

    def show_overlay(self):
        # Crear una nueva ventana con la imagen del sol
        self.overlay_widget = QtWidgets.QMainWindow()
        self.overlay_widget.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)

        # Establecer la transparencia de la ventana
        self.overlay_widget.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Obtener las dimensiones de la pantalla
        screen_geometry = QtWidgets.QDesktopWidget().screenGeometry()

        # Crear un botón circular en la esquina superior izquierda de la pantalla
        button_size = 50  # Tamaño del botón
        button = CircularButton(self.overlay_widget)
        button.move(15, 15)  # Posicionar en la esquina superior izquierda
        button.setFixedSize(button_size, button_size)  # Establecer el tamaño del botón
        button.setText("")  # Eliminar el texto del botón
        button.clicked.connect(self.return_to_main_window)  

        self.overlay_widget.setGeometry(screen_geometry)  # Establecer la misma geometría que la pantalla
        self.overlay_widget.show()

    def return_to_main_window(self):
        self.hide_overlay()  # Ocultar la ventana del sol
        self.resize(500, 200)
        self.showNormal()

    def hide_overlay(self):
        # Cerrar la ventana del sol
        if self.overlay_widget:
            self.overlay_widget.close()
            self.overlay_widget = None

    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.WindowStateChange:
            if self.windowState() & QtCore.Qt.WindowMinimized:
                self.hide()
                self.show_overlay()  # Crear una nueva ventana con la imagen del sol
            elif self.windowState() & QtCore.Qt.WindowMaximized:
                self.show()
                self.hide_overlay()  # Cerrar la ventana del sol si se restaura la ventana principal
        return super(MyWindow, self).changeEvent(event)  # Llamar al método base para no interferir

    def restoreEvent(self, event):
        if self.isMinimized():
            self.showNormal()
        super().restoreEvent(event)

# Crear la aplicación y mostrar la ventana
app = QtWidgets.QApplication([])
window = MyWindow()
window.show()  # Mostrar la ventana
app.exec_()  # Ejecutar el bucle de eventos