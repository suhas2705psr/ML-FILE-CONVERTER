from app.core.converter import convert, get_all_conversions

r1 = convert('tmp/test.pdf', 'txt')
print(f'PDF→TXT:  {r1["status"]} in {r1["duration_ms"]}ms')

r2 = convert('tmp/test.docx', 'pdf')
print(f'DOCX→PDF: {r2["status"]} in {r2["duration_ms"]}ms')

r3 = convert('tmp/test.xlsx', 'csv')
print(f'XLSX→CSV: {r3["status"]} in {r3["duration_ms"]}ms')

r4 = convert('tmp/test.xml', 'json')
print(f'XML→JSON: {r4["status"]} in {r4["duration_ms"]}ms')

print(f'Total conversions supported: {len(get_all_conversions())}')