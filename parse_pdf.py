from PyPDF2 import PdfReader, PdfWriter

def extract_first_two_pages(input_path, output_path):
    # Create a PDF reader object
    reader = PdfReader(input_path)
    
    # Create a PDF writer object
    writer = PdfWriter()
    
    # Add the first two pages to the writer
    for page in reader.pages[:2]:
        writer.add_page(page)
    
    # Write the output to a new file
    with open(output_path, 'wb') as output_file:
        writer.write(output_file)