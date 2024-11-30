from flask import Flask, request, send_file, render_template_string
from PyPDF2 import PdfMerger

app = Flask(__name__)

# HTML content as a string (or you can load it from a file)
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Merge PDFs</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin: 50px;
        }
        h1 {
            color: #4CAF50;
        }
        form {
            margin-top: 20px;
        }
        input[type="file"] {
            margin: 10px 0;
        }
        button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <h1>Merge Your PDFs</h1>
    <p>Select multiple PDF files to merge them into one.</p>
    <form action="/merge" method="POST" enctype="multipart/form-data">
        <input type="file" name="pdfs" multiple required>
        <br>
        <button type="submit">Merge PDFs</button>
    </form>
</body>
</html>

"""

@app.route('/')
def index():
    # Render the HTML page
    return render_template_string(html_content)

@app.route('/merge', methods=['POST'])
def merge_pdfs():
    if 'pdfs' not in request.files:
        return "No files uploaded", 400

    files = request.files.getlist('pdfs')
    merger = PdfMerger()

    for file in files:
        if file.filename.endswith('.pdf'):
            merger.append(file)

    output_path = "merged.pdf"
    merger.write(output_path)
    merger.close()

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
