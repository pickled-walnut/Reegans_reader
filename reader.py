import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QFileDialog, QMenuBar, QMenu, QAction, QColorDialog, QFontDialog, QInputDialog
from PyQt5.QtGui import QColor, QFont, QTextCharFormat
from PyQt5.QtCore import Qt
from OCR import ImageReader

class TextEditor(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize the UI components
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Text File Viewer")
        self.setGeometry(100, 100, 800, 600)

        # Create a layout for the window
        layout = QVBoxLayout()

        # Create a QTextEdit widget for displaying the text file
        self.textEdit = QTextEdit(self)
        self.textEdit.setReadOnly(True)  # Make it read-only for viewing
        layout.addWidget(self.textEdit)

        # Add buttons for opening a file and adjusting settings
        self.openButton = QPushButton('Open Text File', self)
        self.openButton.clicked.connect(self.openFile)
        layout.addWidget(self.openButton)

        # Set up menu for font and color adjustments
        self.setMenuBar()

        # Set the layout for the window
        self.setLayout(layout)

    def setMenuBar(self):
        # Create a menu bar with options for changing font and color
        menubar = QMenuBar(self)

        # File Menu
        fileMenu = menubar.addMenu('File')
        openFileAction = QAction('Open Text File', self)
        openFileAction.triggered.connect(self.openFile)
        fileMenu.addAction(openFileAction)

        openImageAction = QAction('Open Image for OCR', self)
        openImageAction.triggered.connect(self.openImage)
        fileMenu.addAction(openImageAction)

        # View Menu
        viewMenu = menubar.addMenu('View')

        # Font Action
        fontAction = QAction('Change Font', self)
        fontAction.triggered.connect(self.changeFont)
        viewMenu.addAction(fontAction)

        # Text Color Action
        textColorAction = QAction('Change Text Color', self)
        textColorAction.triggered.connect(self.changeTextColor)
        viewMenu.addAction(textColorAction)

        # Background Color Action
        bgColorAction = QAction('Change Background Color', self)
        bgColorAction.triggered.connect(self.changeBackgroundColor)
        viewMenu.addAction(bgColorAction)

        # Resize Text Action
        resizeTextAction = QAction('Resize Text', self)
        resizeTextAction.triggered.connect(self.resizeText)
        viewMenu.addAction(resizeTextAction)

    def openFile(self):
        # Open file dialog to load a text file
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "Open Text File", "", "Text Files (*.txt);;All Files (*)", options=options)
        if filePath:
            with open(filePath, 'r', encoding='utf-8') as file:
                fileContent = file.read()
                self.textEdit.setPlainText(fileContent)

    def openImage(self):
        # Open file dialog to select an image
        options = QFileDialog.Options()
        imagePath, _ = QFileDialog.getOpenFileName(self, "Open Image File", "",
                                                   "Image Files (*.png;*.jpg;*.jpeg;*.bmp;*.gif)", options=options)
        if imagePath:
            extracted_text = self.get_image_data(imagePath)  # Call your OCR function to extract text
            self.textEdit.setPlainText(extracted_text)

    def get_image_data(self, path):
        # This method uses the ImageReader class to extract text from an image
        reader = ImageReader(path)
        data = reader.get_data()  # Assuming this returns the text data
        return data

    def changeFont(self):
        # Open font dialog for font selection
        font, ok = QFontDialog.getFont(self.textEdit.font(), self)
        if ok:
            self.textEdit.setFont(font)

    def changeTextColor(self):
        # Get the current text color from the QTextEdit's document
        current_color = self.textEdit.textColor()

        # Open the QColorDialog to allow the user to pick a new text color
        color = QColorDialog.getColor(current_color, self, "Choose Text Color")

        # If a valid color is chosen, update the text color for the entire document
        if color.isValid():
            # Use QTextCursor to select all text in the document
            cursor = self.textEdit.textCursor()
            cursor.select(cursor.Document)

            # Create a QTextCharFormat and set the foreground color
            fmt = QTextCharFormat()
            fmt.setForeground(color)

            # Apply the formatting to the entire document
            cursor.mergeCharFormat(fmt)

    def changeBackgroundColor(self):
        # Get the current background color of the QTextEdit
        current_color = self.textEdit.palette().color(self.textEdit.backgroundRole())

        # Open the QColorDialog to allow the user to pick a new color
        color = QColorDialog.getColor(current_color, self, "Choose Background Color")

        # If a valid color is chosen, update the background color
        if color.isValid():
            self.textEdit.setStyleSheet(f'background-color: {color.name()};')

    def resizeText(self):
        # Ask the user to input the new font size
        new_size, ok = QInputDialog.getInt(self, 'Resize Text', 'Enter new font size:', 12, 1, 100, 1)

        if ok:
            # Create a QTextCursor to select all text in the document
            cursor = self.textEdit.textCursor()
            cursor.select(cursor.Document)

            # Create a QTextCharFormat and set the new font size
            fmt = QTextCharFormat()
            font = self.textEdit.font()
            font.setPointSize(new_size)
            fmt.setFont(font)

            # Apply the formatting to the entire document
            cursor.mergeCharFormat(fmt)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Create and show the main window
    editor = TextEditor()
    editor.show()

    # Execute the application
    sys.exit(app.exec_())
