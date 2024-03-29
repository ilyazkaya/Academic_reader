import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView

class PDFViewer(QMainWindow):
    def __init__(self, pdf_path):
        super().__init__()
        self.initUI(pdf_path)

    def initUI(self, pdf_path):
        # Create a QPdfView widget
        self.pdfView = QPdfView(self)
        self.setCentralWidget(self.pdfView)

        # Load the PDF document
        self.pdfDocument = QPdfDocument(self)
        self.pdfDocument.load(pdf_path)

        # Set the document for the view
        self.pdfView.setDocument(self.pdfDocument)

        # Set the window size and title
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('PDF Viewer')
        self.show()

def main():
    app = QApplication(sys.argv)
    pdf_path = rf'C:\Users\il_ka\PycharmProjects\Academic_reader\papers\Knop 2013 Morphological and physiological properties of enhanced green fluorescent protein (EGFP)-expressing wide-field amacrine cells in the ChAT-EGFP mouse line.pdf'  # Replace with your PDF file path
    viewer = PDFViewer(pdf_path)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()