import streamlit as st
import PyPDF2
import os
import json
from datetime import datetime, timedelta

# Configuration
PDF_FILE_PATH = "your_book.pdf"  # Full path to the PDF file
OUTPUT_DIR = "Daily_Practice"   # Directory to save daily PDFs
PROGRESS_FILE = "progress.txt"  # File to track progress
METADATA_FILE = "metadata.json" # File to track file timestamps

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

def load_metadata():
    """Load metadata from the JSON file."""
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, "r") as file:
            return json.load(file)
    return {}

def save_metadata(metadata):
    """Save metadata to the JSON file."""
    with open(METADATA_FILE, "w") as file:
        json.dump(metadata, file, indent=4)

def delete_expired_files(metadata):
    """Delete files older than 24 hours and update metadata."""
    current_time = datetime.now()
    updated_metadata = {}
    for file_path, timestamp in metadata.items():
        file_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        if current_time - file_time > timedelta(hours=24):
            if os.path.exists(file_path):
                os.remove(file_path)
        else:
            updated_metadata[file_path] = timestamp
    return updated_metadata

def main():
    st.title("Automated Daily Practice PDF Generator")
    st.write("This app generates a set of practice pages daily, allows you to adjust the number of pages, and auto-deletes files after 24 hours.")

    # Page selection slider
    st.sidebar.header("Settings")
    pages_per_day = st.sidebar.slider("Number of pages to practice daily", min_value=1, max_value=20, value=5)

    # Load and clean up metadata
    metadata = load_metadata()
    metadata = delete_expired_files(metadata)
    save_metadata(metadata)

    # Get the last page worked on
    last_page = get_last_page()
    start_page = last_page + 1
    end_page = start_page + pages_per_day

    # Generate the next practice set
    output_path = f"{OUTPUT_DIR}/Practice_{start_page}_to_{end_page - 1}.pdf"
    extract_pages(start_page - 1, end_page - 1, output_path)
    save_last_page(end_page - 1)

    # Save file creation time in metadata
    metadata[output_path] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_metadata(metadata)

    # Display success message and download link
    st.success(f"Today's practice saved as: {output_path}")
    st.write(f"Pages: {start_page} to {end_page - 1}")
    with open(output_path, "rb") as f:
        st.download_button("Download Today's Practice PDF", f, file_name=f"Practice_{start_page}_to_{end_page - 1}.pdf")

if __name__ == "__main__":
    main()
