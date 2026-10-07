import re

# Match critical failure indicators
pattern = re.compile(
    r'(?i)\b(fatal|critical|severe|emerg(?:ency)?|alert|err(?:or)?|warn(?:ing)?|fail(?:ed|ure)?|exception|traceback|panic|deadlock|timed?[\s_-]?out|unauthorized|denied)\b'
)

# Skip false positives that pollute LLM context
exclude_pattern = re.compile(
    r'(?i)(\b0\s+errors?\b|errors?[:=]\s*0\b|\bno[\s_-]error\b|\b0\s+warnings?\b)'
)

report = [
    "# SYSTEM LOG DIAGNOSTIC REPORT FOR AI ANALYSIS",
    "Generated from loaded files for automated triage.",
    "-" * 70
]

total_matches = 0
files_processed = 0

for file_path, buffer_id, index, view in notepad.getFiles():
    files_processed += 1
    notepad.activateBufferID(buffer_id)
    content = editor.getText()
    matches_found = []
    
    for line_num, line in enumerate(content.splitlines(), start=1):
        clean_line = line.strip()
        if not clean_line:
            continue
            
        if pattern.search(clean_line) and not exclude_pattern.search(clean_line):
            matches_found.append("Line {0:5d} | {1}".format(line_num, clean_line))
            
    if matches_found:
        report.append("\n## FILE: {0}".format(file_path))
        report.append("Total Events: {0}".format(len(matches_found)))
        report.append("```")
        report.extend(matches_found)
        report.append("```")
        total_matches += len(matches_found)

summary = [
    "-" * 70,
    "# SUMMARY METRICS",
    "- Total Files Scanned: {0}".format(files_processed),
    "- Total Anomalies Detected: {0}".format(total_matches),
    "-" * 70,
    ""
]

# Insert summary at the top under title for fast reading by LLMs
final_output = report[:3] + summary + report[3:]

notepad.new()
editor.setText("\n".join(final_output))
editor.setSavePoint()