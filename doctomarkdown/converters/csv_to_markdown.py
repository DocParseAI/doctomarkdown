import csv
from typing import BinaryIO


def csv_to_markdown(file_stream: BinaryIO, encoding="utf-8", header_row=False) -> str:
    # Read the CSV content
    content = file_stream.read().decode(encoding)
    reader = csv.reader(content.splitlines())
    rows = list(reader)
    if not rows:
        return ""
    # Build markdown table

    if header_row:  # If user wants first row to be a header
        header = "| " + " | ".join(rows[0]) + " |"
        separator = "| " + " | ".join(["---"] * len(rows[0])) + " |"
        data_rows = ["| " + " | ".join(row) + " |" for row in rows[1:]]
        return "\n".join([header, separator] + data_rows)
    else:  # If user does not specify
        data_rows = ["| " + " | ".join(row) + " |" for row in rows]
        return "\n".join(data_rows)


# Example usage:
# with open("data.csv", "rb") as f:
#     markdown = csv_to_markdown(f)
#     print(markdown)
