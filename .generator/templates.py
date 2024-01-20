# Site generator for https://reports.cicirello.org/
# Copyright (c) 2024 Vincent A. Cicirello. All rights reserved.
#
# This site generator is almost certainly useless to anyone other than me.
# It is highly customized to generate one specific website. Therefore, I am
# not licensing it to others. Notice the "All rights reserved" in the
# copyright notice at the top.

url_root = "https://reports.cicirello.org/"

bibtex_web_template = """@techreport{{{0},
  title = {{{1}}},
  author = {{{2}}},
  year = {{{3}}},
  month = {{{4}}},
  number = {{{5}}},
  institution = {{{6}}},
  url = {{{7}}}
}}
"""

bibtex_file_template = """@techreport{{{0},
  title = {{{1}}},
  author = {{{2}}},
  year = {{{3}}},
  month = {{{4}}},
  number = {{{5}}},
  institution = {{{6}}},
  url = {{{7}}},
  abstract = {{{8}}}
}}
"""

title_image_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="672" viewBox="0 0 1280 672">
<rect fill="#bfd9bf" stroke="#4CAF50" stroke-width="80" width="1200" height="592" x="40" y="40"/>
<g font-size="110pt" font-family="Verdana,Geneva,DejaVu Sans,sans-serif"
text-rendering="geometricPrecision">
{2}
<text x="1467" y="1311" lengthAdjust="spacingAndGlyphs" textLength="{1}" text-anchor="middle"
transform="scale(0.436)" fill="#305030">{0}</text>
</g>
<rect fill="#305030" stroke="#305030" width="800" height="20" x="240" y="494"/>
<g transform="translate(98,494)"><svg width="80" height="80" viewBox="0 0 32 32"><rect
style="fill:#f6f0bb;stroke:#862d2d;stroke-width:1.5;" width="30.5" height="30.5" x="0.75" y="0.75"
rx="4"/><text x="50%" y="35%" dominant-baseline="central" text-anchor="middle" font-size="20px"
fill="#862d2d">VC</text><text x="50%" y="65%" dominant-baseline="central" text-anchor="middle"
font-size="20px" fill="#862d2d">A</text></svg></g>
</svg>
"""

title_line = """<text x="1280" y="{0}" lengthAdjust="spacingAndGlyphs" textLength="{2}" text-anchor="middle"
transform="scale(0.500)" fill="#862d2d">{1}</text>"""
