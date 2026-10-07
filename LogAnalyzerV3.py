import re

# Match critical failure indicators
pattern = re.compile(
    r'(?i)\b(fatal|critical|severe|emerg(?:ency)?|alert|err(?:or)?|warn(?:ing)?|fail(?:ed|ure)?|exception|traceback|panic|deadlock|timed?[\s_-]?out|unauthorized|denied)\b'
)

# Skip false positives that pollute LLM context
exclude_pattern = re.compile(
    r'(?i)(\b0\s+errors?\b|errors?[:=]\s*0\b|\bno[\s_-]error\b|\b0\s+warnings?\b)'
)

# Regex to strip dynamic data (timestamps, UUIDs/GUIDs, memory hex, IPs) for pattern collapsing
dynamic_strip_patterns = [
    re.compile(r'\b\d{4}[-/]\d{2}[-/]\d{2}[T\s]\d{2}:\d{2}:\d{2}(?:[.,]\d+)?\b'),        # Timestamps
    re.compile(r'\b[0-9a-fA-F]{8}-(?:[0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}\b'),           # GUIDs / UUIDs
    re.compile(r'\b0x[0-9a-fA-F]+\b'),                                                   # Hex addresses
    re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b'),                                          # IPv4 addresses
]

def get_signature(line_text):
    """Normalizes the line by stripping variable parts so identical issues cluster together."""
    sig = line_text
    for p in dynamic_strip_patterns:
        sig = p.sub('<...>', sig)
    return " ".join(sig.split())  # Normalize whitespace

report = [
    "# SYSTEM LOG DIAGNOSTIC REPORT FOR AI ANALYSIS",
    "Generated from loaded files for automated triage.",
    "-" * 70
]

total_matches = 0
unique_patterns_found = 0
files_processed = 0

for file_path, buffer_id, index, view in notepad.getFiles():
    files_processed += 1
    notepad.activateBufferID(buffer_id)
    content = editor.getText()
    
    # Store aggregated events in order of appearance
    # Structure: signature -> {"first_line": int, "last_line": int, "count": int, "sample": str}
    grouped_events = {}
    ordered_signatures = []
    
    file_raw_matches = 0

    for line_num, line in enumerate(content.splitlines(), start=1):
        clean_line = line.strip()
        if not clean_line:
            continue
            
        if pattern.search(clean_line) and not exclude_pattern.search(clean_line):
            file_raw_matches += 1
            sig = get_signature(clean_line)
            
            if sig not in grouped_events:
                grouped_events[sig] = {
                    "first_line": line_num,
                    "last_line": line_num,
                    "count": 1,
                    "sample": clean_line
                }
                ordered_signatures.append(sig)
            else:
                grouped_events[sig]["count"] += 1
                grouped_events[sig]["last_line"] = line_num

    if ordered_signatures:
        report.append("\n## FILE: {0}".format(file_path))
        report.append("Total Events: {0} (Unique Clusters: {1})".format(file_raw_matches, len(ordered_signatures)))
        report.append("```")
        
        for sig in ordered_signatures:
            item = grouped_events[sig]
            if item["count"] > 1:
                line_str = "Lines {0:5d}-{1:<5d}".format(item["first_line"], item["last_line"])
                report.append("{0} | [REPEATED x{1:d}] {2}".format(line_str, item["count"], item["sample"]))
            else:
                line_str = "Line  {0:5d}      ".format(item["first_line"])
                report.append("{0} | {1}".format(line_str, item["sample"]))
                
        report.append("```")
        total_matches += file_raw_matches
        unique_patterns_found += len(ordered_signatures)

summary = [
    "-" * 70,
    "# SUMMARY METRICS",
    "- Total Files Scanned: {0}".format(files_processed),
    "- Total Raw Anomalies: {0}".format(total_matches),
    "- Deduplicated Anomalies: {0}".format(unique_patterns_found),
    "-" * 70,
    ""
]

# Insert summary at the top under the header title
final_output = report[:3] + summary + report[3:]

notepad.new()
editor.setText("\n".join(final_output))
editor.setSavePoint()