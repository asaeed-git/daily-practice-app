import streamlit as st
import PyPDF2
import os

# Configuration (Edit these paths and values as needed)
PDF_FILE_PATH = "GATBook.pdf"  # Full path to the PDF file
OUTPUT_DIR = "Daily_Practice"   # Directory to save daily PDFs
PAGES_PER_DAY = 5               # Number of pages to extract daily
PROGRESS_FILE = "progress.txt"  # File to track progress

# Ensure output directory exists
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def get_last_page():
    """Retrieve the last page number from the progress file."""
    try:
        with open(PROGRESS_FILE, "r") as file:
            return int(file.read().strip())
    except FileNotFoundError:
        return 0

def save_last_page(last_page):
    """Save the last page number to the progress file."""
    with open(PROGRESS_FILE, "w") as file:
        file.write(str(last_page))

def extract_pages(start_page, end_page, output_path):
    """Extract pages from a PDF and save to a new file."""
    with open(PDF_FILE_PATH, "rb") as input_pdf:
        reader = PyPDF2.PdfReader(input_pdf)
        writer = PyPDF2.PdfWriter()

        for page_num in range(start_page, end_page):
            if page_num < len(reader.pages):
                writer.add_page(reader.pages[page_num])
            else:
                break

        with open(output_path, "wb") as output_pdf:
            writer.write(output_pdf)

def main():
    st.title("Automated Daily Practice PDF Generator")
    st.write("This app automatically generates a set of practice pages every day.")

    # Get the last page worked on
    last_page = get_last_page()
    start_page = last_page + 1
    end_page = start_page + PAGES_PER_DAY

    # Generate the next practice set
    output_path = f"{OUTPUT_DIR}/Practice_{start_page}_to_{end_page - 1}.pdf"
    extract_pages(start_page - 1, end_page - 1, output_path)
    save_last_page(end_page - 1)

    # Display success message and download link
    st.success(f"Today's practice saved as: {output_path}")
    st.write(f"Pages: {start_page} to {end_page - 1}")
    with open(output_path, "rb") as f:
        st.download_button("Download Today's Practice PDF", f, file_name=f"Practice_{start_page}_to_{end_page - 1}.pdf")

if __name__ == "__main__":
    main()
