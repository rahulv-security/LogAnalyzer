import re

pattern = re.compile(r'(?i)\b(error|warn|warning)\b')
report = ["=" * 60, "LOG ERROR & WARNING AGGREGATED REPORT", "=" * 60, ""]
total_matches = 0

for file_path, buffer_id, index, view in notepad.getFiles():
    notepad.activateBufferID(buffer_id)
    content = editor.getText()
    matches_found = []
    
    for line_num, line in enumerate(content.splitlines(), start=1):
        if pattern.search(line):
            matches_found.append("Line {0:5d}: {1}".format(line_num, line.strip()))
            
    if matches_found:
        report.append("\n[FILE] {0}".format(file_path))
        report.append("-" * 60)
        report.extend(matches_found)
        total_matches += len(matches_found)

report.append("\n\nTotal findings: {0}".format(total_matches))

notepad.new()
editor.setText("\n".join(report))
editor.setSavePoint()