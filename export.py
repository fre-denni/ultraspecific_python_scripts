#!/usr/bin/env python
import sys
import re
import subprocess
import os

# Read input file
with open(sys.argv[1], 'r', encoding='utf-8') as f:
    content = f.read()

# Replace Obsidian-style citation links -> [[]] to []
content = re.sub(r'\[\[@(.*?)\]\]', r'[@\1]', content)

# Write temp file
with open('temp.md', 'w', encoding='utf-8') as f:
    f.write(content)

# Run Pandoc
try:
  subprocess.run([
      'pandoc', 'temp.md',
      '--citeproc',
      '--bibliography', '_bibliographies/Biblioteca personale.bib',
      '-o', 'docx/'+ sys.argv[2] + '.docx'
  ], check=True)
finally:
  if os.path.exists('temp.md'):
     os.remove('temp.md')