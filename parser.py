from docx import Document

def parse_roster(filepath):
    doc = Document(filepath)
    rows = []

    for table in doc.tables:
        headers = [cell.text.strip().lower() for cell in table.rows[0].cells]
        if not any("i.t." in h or "p.a." in h or "date" in h for h in headers):
            continue  # Skip unrelated tables

        for i, row in enumerate(table.rows[1:]):
            cells = [cell.text.strip() for cell in row.cells]
            if len(cells) < 5:
                continue  # Skip incomplete rows

            date = cells[0]
            it_name = cells[1]
            pa_name = cells[3]

            # Only add if there's a date AND at least one name
            if date and (it_name or pa_name):
                rows.append({
                    "date": date,
                    "it": it_name if it_name else "",
                    "pa": pa_name if pa_name else ""
                })

    return rows
