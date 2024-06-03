import PyPDF2
import pandas as pd
from fpdf import FPDF

# Step 1: Extract Text from PDF and Save to CSV
def extract_text_from_pdf(pdf_path):
    pdf_file = open("/Users/macbook/Desktop/AI_IMAGER/invoice.pdf", 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    extracted_text = ""
    for page in pdf_reader.pages:
        extracted_text += page.extract_text()
    pdf_file.close()
    return extracted_text

def save_to_csv(text, csv_path):
    lines = text.split('\n')
    data = []
    for line in lines:
        if line.strip():  # Ignore empty lines
            if ':' in line:
                key, value = line.split(':', 1)
                data.append([key.strip(), value.strip()])
            else:
                data.append([line.strip(), ""])  # For lines without a colon
    
    df = pd.DataFrame(data, columns=['Field', 'Value'])
    df.to_csv(csv_path, index=False)

pdf_path = '/Users/macbook/Desktop/AI_IMAGER/invoice.pdf'
csv_path = 'extracted_data.csv'

extracted_text = extract_text_from_pdf(pdf_path)
save_to_csv(extracted_text, csv_path)
print(f'Data saved to {csv_path}')

# Step 2: Modify the CSV file manually

# Step 3: Read the Modified CSV File and Create a New PDF
def read_from_csv(csv_path):
    df = pd.read_csv("/Users/macbook/Desktop/AI_IMAGER/extracted_data.csv")
    text = ""
    for index, row in df.iterrows():
        text += f"{row['Field']}: {row['Value']}\n"
    return text

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Modified Document', 0, 1, 'C')

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

def create_pdf(pdf_path, text):
    pdf = PDF()
    pdf.add_page()
    pdf.chapter_body(text)
    pdf.output(pdf_path)

# Read from the modified CSV file and create a new PDF
new_csv_path = 'modified_data.csv'  # Ensure this file is edited with your modifications
new_pdf_path = 'modified_document.pdf'

modified_text = read_from_csv(new_csv_path)
create_pdf(new_pdf_path, modified_text)
print(f'Modified PDF created at {new_pdf_path}')
