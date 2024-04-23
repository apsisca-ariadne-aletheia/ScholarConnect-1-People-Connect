import os
from PyPDF2 import PdfFileReader
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

# Define the database engine
engine = create_engine('sqlite:///pdf_authenticator.db', echo=True)
Base = declarative_base()

# Define the PDF model for database storage
class PDFDocument(Base):
    __tablename__ = 'pdf_documents'

    id = Column(Integer, primary_key=True)
    filename = Column(String, unique=True)
    authenticated = Column(Integer)

# Create the database tables
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

def authenticate_pdf(file_path):
    # Validate and sanitize input file path
    file_path = file_path.strip()  # Remove leading and trailing spaces
    if not file_path:
        print("Error: File path cannot be empty.")
        return

    # Check if the file path is safe and exists
    if not os.path.exists(file_path):
        print("Error: File not found or invalid file path.")
        return

    # Check if the file is a PDF
    if not file_path.lower().endswith('.pdf'):
        print("Error: File is not a PDF.")
        return

    try:
        # Read the PDF file securely
        with open(file_path, 'rb') as file:
            pdf_reader = PdfFileReader(file)
            num_pages = pdf_reader.getNumPages()
            # Perform authentication logic (e.g., check if it meets certain criteria)
            authenticated = num_pages > 0  # Example: authenticate if the PDF has at least one page

            # Store the authenticated PDF in the database
            pdf_doc = PDFDocument(filename=file_path, authenticated=authenticated)
            session.add(pdf_doc)
            session.commit()

            print(f"PDF '{file_path}' authenticated and stored in the database.")
    except Exception as e:
        print(f"Error: {e}")
        session.rollback()

# Example usage
pdf_file_path = input("Enter the PDF file path: ")
authenticate_pdf(pdf_file_path)
