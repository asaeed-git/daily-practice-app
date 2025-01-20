import PyPDF2

# Configuration
input_pdf_path = "GATBook.pdf"  # Replace with the path to your PDF
output_dir = "Daily_Practice"  # Directory to save the daily PDFs
pages_per_day = 5  # Number of pages to extract daily
progress_file = "progress.txt"  # File to store your progress

def get_last_page():
    """Retrieve the last page number from the progress file."""
    try:
        with open(progress_file, "r") as file:
            return int(file.read().strip())
    except FileNotFoundError:
        return 0

def save_last_page(last_page):
    """Save the last page number to the progress file."""
    with open(progress_file, "w") as file:
        file.write(str(last_page))

def extract_pages(start_page, end_page, output_path):
    """Extract pages from a PDF and save to a new file."""
    with open(input_pdf_path, "rb") as input_pdf:
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
    # Get the last page worked on
    last_page = get_last_page()
    start_page = last_page + 1
    end_page = start_page + pages_per_day

    # Extract and save the next set of pages
    output_path = f"{output_dir}/Practice_{start_page}_to_{end_page - 1}.pdf"
    extract_pages(start_page - 1, end_page - 1, output_path)

    # Update progress
    save_last_page(end_page - 1)
    print(f"Today's practice saved as: {output_path}")

if __name__ == "__main__":
    import os
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    main()
