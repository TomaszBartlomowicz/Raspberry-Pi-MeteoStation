from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QTextEdit,
                             QHBoxLayout, QSizePolicy, QVBoxLayout, QScrollArea)
from PyQt5.QtCore import Qt

class ErrorConsole(QWidget):
    def __init__(self, theme, backend):
        super().__init__()

        self.theme = theme
        self.backend = backend
        self.title = QLabel("Errors detected:")
        self.error_window = QTextEdit()

        self.back_button = QPushButton("Main menu")
        self.back_button.clicked.connect(self.close)

        self.clear_button = QPushButton("Clear errors")
        self.clear_button.clicked.connect(self.clear_button_clicked)

        self.scroll_area = QScrollArea()
        self.scroll_area.setVerticalScrollBarPolicy(2)
        self.errors_widget = QWidget()
        self.layout()
        self.styling()
        self.display_errors()



    def display_errors(self):
        """Displays errors in the error console"""
        if self.backend.errors:
            for error in self.backend.errors:
                self.styling()
                self.error_window.append(error)
                self.error_window.append(81 * "-")

        else:
            self.error_window.setStyleSheet("color: #11c208;"
                                            "font-size: 30px;")
            self.error_window.append("<center><h1>No errors detected</h1></center>")
            self.clear_button.setDisabled(True)

    def clear_button_clicked(self):
        """Clears console"""
        self.error_window.clear()
        self.backend.errors.clear()
        self.error_window.setStyleSheet("color: #11c208;"
                                        "font-size: 30px;")
        self.error_window.append("<center><h1>Error console cleared!</h1><center>")

    def styling(self):
        """Sets styling"""
        self.title.setStyleSheet("font-size: 35px;")
        self.back_button.setStyleSheet("font-size: 25px;")
        self.clear_button.setStyleSheet("font-size: 25px;"
                                        "background-color: darkred;"
                                        "color: white;")
        self.title.setAlignment(Qt.AlignCenter)

        style = ("""
                    QTextEdit {
                        border: 3px solid darkred;   /* Zielona ramka */
                        border-radius: 10px;          /* Zaokrąglone rogi */
                        padding: 10px;                /* Wewnętrzne marginesy */
                        font-size: 30px;              /* Rozmiar czcionki */
                    }sc
                """)

        self.error_window.setStyleSheet(style)
        self.error_window.setReadOnly(True)
        self.error_window.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.scroll_area.setWidgetResizable(True)

    def layout(self):
        """Manages layout"""

        top_layout = QHBoxLayout()
        top_layout.addWidget(self.title)


        errors_layout = QVBoxLayout()
        errors_layout.addWidget(self.error_window)


        self.errors_widget.setLayout(errors_layout)
        self.scroll_area.setWidget(self.errors_widget)

        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch(1)
        bottom_layout.addWidget(self.clear_button)
        bottom_layout.addStretch(1)
        bottom_layout.addWidget(self.back_button)
        bottom_layout.addStretch(1)

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.scroll_area)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)