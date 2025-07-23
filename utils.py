from docx import Document

def parse_roster(filepath):
    doc = Document(filepath)
    rows = []

    for table in doc.tables:
        for i in range(1, len(table.rows)):
            cells = table.rows[i].cells
            if len(cells) < 5:
                continue
            date = cells[0].text.strip()
            it = cells[1].text.strip()
            it_email = cells[2].text.strip()
            pa = cells[3].text.strip()
            pa_email = cells[4].text.strip()
            comment = cells[5].text.strip() if len(cells) > 5 else ""

            rows.append({
                "date": date,
                "it": it,
                "it_email": it_email if "@" in it_email else None,
                "pa": pa,
                "pa_email": pa_email if "@" in pa_email else None,
                "comment": comment
            })
    return rows
