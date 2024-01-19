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
