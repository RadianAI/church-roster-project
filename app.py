from flask import Flask, render_template, request
import os
from docx import Document

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def parse_roster(filepath):
    doc = Document(filepath)
    rows = []

    # Assuming your docx tables have these columns:
    # Date | I.T. Operator | I.T. Email | P.A. Operator | P.A. Email | Comments
    for table in doc.tables:
        for row in table.rows[1:]:  # skip header row
            cells = row.cells
            date = cells[0].text.strip()
            it_operator = cells[1].text.strip()
            it_email = cells[2].text.strip()
            pa_operator = cells[3].text.strip()
            pa_email = cells[4].text.strip()
            comment = cells[5].text.strip() if len(cells) > 5 else ""
            rows.append({
                "date": date,
                "it": it_operator,
                "it_email": it_email,
                "pa": pa_operator,
                "pa_email": pa_email,
                "comment": comment
            })

    return rows

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("roster")
        if file and file.filename.endswith(".docx"):
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            rows = parse_roster(filepath)
            return render_template("index.html", rows=rows)
        else:
            return "❌ Only .docx files are allowed."
    return render_template("index.html", rows=None)

if __name__ == "__main__":
    app.run(debug=True)
