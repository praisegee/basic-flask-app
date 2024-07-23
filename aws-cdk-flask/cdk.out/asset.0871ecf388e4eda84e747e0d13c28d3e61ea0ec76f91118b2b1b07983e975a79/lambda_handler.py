# -*- coding: utf-8 -*-
"""
You will have to install required dependencies via Pip or using conda from anaconda (please be aware that pip is highly dangerous for conda env)

Once dependencies are sucessfully installed you should run your app in CMD (or a conda prompt) then you may do curl or postman request, and get a 
JSON Object as response
"""
import spacy
import awsgi
from flask import Flask, request, jsonify

import fitz  # PyMuPDF
import re

app = Flask(__name__)

# Load the pre-trained spaCy model for English
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_path):
    # Open the PDF file
    doc = fitz.open(pdf_path)
    text = ""

    # Iterate over each page
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()

    return text

def parse_document(doc_text):
    # Process the document text with spaCy
    doc = nlp(doc_text)

    # Initialize variables to store extracted information
    name = ""
    contact_details = {'email': '', 'phone': ''}
    data = {'name':[],'Adress Information':[],'contact_details':[],'Department':[],
            'Area Of Expertise':[],'Title':[]}


    # Process the document for named entities
    for ent in doc.ents:
        if ent.label_ == "PERSON" and not name:
            data['name'].append(ent.text)
        elif ent.label_ == "GPE" or ent.label_ == "LOC":
            data['Adress Information'].append(ent.text)

    email_regex = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    phone_regex = r'(\+?\d{1,4}[\s-]?)?(\(?\d{3}\)?[\s-]?)?\d{3}[\s-]?\d{4}'

    # Find email and phone number in the document text
    emails = re.findall(email_regex, doc_text)
    phones = re.findall(phone_regex, doc_text)

    if emails:
        contact_details['email'] = emails[0]
    if phones:
        contact_details['phone'] = phones[0]

    data['contact_details'].append(contact_details)

    # Split the text into lines to find specific sections
    lines = doc_text.split('\n')
    for line in lines:
        if 'department' in line.lower():
            data['Department'].append(line.split(':')[1].strip())
        elif 'area of expertise' in line.lower() or 'expertyse' in line.lower():
            data['Area Of Expertise'].append(line.split(':')[1].strip())
        elif 'title' in line.lower():
            data['Title'].append(line.split(':')[1].strip())

    return data
"""
# Example usage with the provided PDF file
file_path = '/content/drive/My Drive/Pharmaserv/Proof_Costumer_Tracking.pdf'
document_text = extract_text_from_pdf(file_path)
data = parse_document(document_text)

print(data)"""

import os
import json

def read_file(file_path):
    # Get the file extension
    _, file_extension = os.path.splitext(file_path)

    # Check the file extension and read the file accordingly
    try:
        if file_extension.lower() in ['.txt']:
            with open(file_path, 'r') as file:
                content = file.read()
                #print("Text file content:\n", content)

        elif file_extension.lower() in ['.json']:
            with open(file_path, 'r') as file:
                content = json.load(file)
                #print("JSON file content:\n", json.dumps(content, indent=4))

        elif file_extension.lower() in ['.pdf']:
             content = extract_text_from_pdf(file_path)
             #print("PDF file content:\n", content)

        else:
            with open(file_path, 'rb') as file:
                content = file.read()
                print("Binary file content:\n", content[:100], "...\n[truncated]")

        return parse_document(str(content))

    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return False
"""
# Example usage
file_path = '/content/drive/My Drive/Pharmaserv/Data_second_project/pharmaserv-co-pilot-db.hcps.json'
print(read_file(file_path))"""


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    file_path = f"./{file.filename}"
    file.save(file_path)
    data = read_file(file_path)
    return jsonify(data)

def handler(event, context):
    return awsgi.response(app, event, context)

if __name__ == '__main__':
    app.run(debug=True)