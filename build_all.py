# -*- coding: utf-8 -*-
import os
import sys

from parts_css import CSS_CONTENT
from parts_html import HTML_CONTENT
from parts_js_core import JS_CORE
from parts_js_service import JS_SERVICE
from parts_js_ui import JS_UI

print("Assembling index.html...")

full_html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Caderno de Previsões Operacionais em Dutos</title>
  <style>
{CSS_CONTENT}
  </style>
</head>
<body>
{HTML_CONTENT}
  <script>
{JS_CORE}

{JS_SERVICE}

{JS_UI}
  </script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(full_html)

file_size = os.path.getsize("index.html")
print(f"index.html generated successfully! File size: {file_size} bytes ({file_size/1024:.2f} KB)")

