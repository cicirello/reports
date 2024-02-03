# Site generator for https://reports.cicirello.org/
# Copyright (c) 2024 Vincent A. Cicirello. All rights reserved.
#
# This site generator is almost certainly useless to anyone other than me.
# It is highly customized to generate one specific website. Therefore, I am
# not licensing it to others. Notice the "All rights reserved" in the
# copyright notice at the top.

url_root = "https://reports.cicirello.org/"
site_title = "Cicirello.org Technical Reports"
site_description = """This site is a collection of Technical Reports from
the research of Vincent A. Cicirello. It includes preprints of publications,
some of which may also appear on arXiv; reports on research results not
otherwise used in published works but which may be of use to other researchers;
among other technical research content.
"""

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
<g font-size="110pt" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" text-rendering="geometricPrecision">
{2}
<text x="1467" y="1311" lengthAdjust="spacingAndGlyphs" textLength="{1}" text-anchor="middle" transform="scale(0.436)" fill="#305030">{0}</text>
</g>
<rect fill="#305030" stroke="#305030" width="800" height="20" x="240" y="494"/>
<g transform="translate(98,494)"><svg width="80" height="80" viewBox="0 0 32 32">
<rect style="fill:#f6f0bb;stroke:#862d2d;stroke-width:1.5;" width="30.5" height="30.5" x="0.75" y="0.75" rx="4"/>
<text x="50%" y="35%" dominant-baseline="central" text-anchor="middle" font-size="20px" fill="#862d2d">VC</text>
<text x="50%" y="65%" dominant-baseline="central" text-anchor="middle" font-size="20px" fill="#862d2d">A</text>
</svg></g>
</svg>
"""

title_line = """<text x="1280" y="{0}" lengthAdjust="spacingAndGlyphs" textLength="{2}" text-anchor="middle" transform="scale(0.500)" fill="#862d2d">{1}</text>"""

page_head_start = """<meta charset=utf-8>
<link rel="canonical" href="{CANONICAL}">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none';{OBJECTSRC} img-src 'self'; style-src '{STYLEHASH}'; base-uri 'none'; form-action 'none';">
<meta name="referrer" content="strict-origin-when-cross-origin">
<title>{TITLE}</title>
<meta name="title" content="{TITLE}">
<meta name="description" content="{DESCRIPTION}">
<link rel="icon" href="/images/favicon.svg" sizes="any" type="image/svg+xml">
<meta property="og:url" content="{CANONICAL}">
<meta property="og:title" content="{TITLE}">
<meta property="og:image" content="{SOCIALPREVIEW}">
<meta property="og:image:width" content="1280">
<meta property="og:image:height" content="672">
<meta property="og:description" content="{DESCRIPTION}">
"""

citation_tags = """<meta name="citation_title" content="{TITLE}">
{AUTHORS}
<meta name="citation_publication_date" content="{YEAR}">
<meta name="citation_date" content="{YEAR}">
<meta name="citation_technical_report_institution" content="{INSTITUTION}">
<meta name="citation_technical_report_number" content="{REPORT_NUM}">
<meta name="citation_pdf_url" content="{PDF_URL}">
<meta name="citation_abstract_html_url" content="{CANONICAL}">
"""

citation_author = """<meta name="citation_author" content="{AUTHOR}">"""

content_header = """<body>
<header id="siteheader">
<h2><img src="{HEADER_SVG}" alt="{PAGE_TITLE}" width="1280" height="672" class="respimg"></h2>
<nav id="topNav">
<input type="checkbox" id="toggle">
<label for="toggle" id="menu-icon">&#9776;</label>
<div><a href="/"{ACTIVE}>Cicirello.org Technical Reports</a></div>
<div><a href="https://www.cicirello.org/">Vincent A. Cicirello</a></div>
<div><a href="https://www.cicirello.org/publications/">All Publications</a></div>
</nav>
</header>
"""

home_page_content = """<article class="publist">
<h2 id="top">Technical Reports</h2>
<p>This site is a series of Technical Reports from the research of
<a href="https://www.cicirello.org/">Vincent A. Cicirello</a>. Some of the
Technical Reports are preprints of journal articles or conference papers,
some of which may also appear on arXiv. Some such preprints may be on
research that is still in progress that I intend to publish in journals
or conferences in the future. Other Technical Reports provide research
results not otherwise used in published works but which may be of use to
other researchers. Additional Technical Reports on this site concern other
technical research content, or details of software tools I've developed.
Also see the
<a href="https://www.cicirello.org/publications/">complete list of
publications</a> on
<a href="https://www.cicirello.org/">Vincent A. Cicirello's website</a>.
You can also download a <a href="reports.bib">BibTeX file for all Technical
Reports</a>.</p>
"""

link_legend = """<details>
<summary>Link label legend</summary>
<table>
<tr><th>Link</th><th>Links To</th></tr>
<tr><td>Title</td><td>Abstract/information page</td></tr>
<tr><td>[PDF]</td><td>Full-text pdf file</td></tr>
<tr><td>[BIB]</td><td>BibTeX file</td></tr>
<tr><td>[DOI]</td><td>Persistent link to publisher's version</td></tr>
<tr><td>[PUB]</td><td>Publisher's version</td></tr>
<tr><td>[arXiv]</td><td>Preprint on arXiv.org</td></tr>
<tr><td>[CODE]</td><td>Source code repository, such as to reproduce experimental results, etc.</td></tr>
</table>
</details>
"""

report_page_content = """<article>
<header>
<h2><a href="{PDF_FILE}">{TITLE}</a></h2>
<h3>{AUTHORS}</h3>
<h4>Technical Report {REPORT_NUM}, {INSTITUTION}, {MONTH} {YEAR}.</h4>
{NOTE}</header>
<details>
<summary>Show BibTeX</summary>
<pre><code>{BIBTEX}</code></pre>
<a href="{BIB_FILE}">Download BibTeX file</a>
</details>
<section>
<h4>Abstract</h4>
<p>{ABSTRACT}</p>
<object class="pdfembed" data="{PDF_FILE}#view=FitH&pagemode=none" type="application/pdf" width="100%" height="100%">
<a href="{PDF_FILE}">Download Fulltext PDF</a>
</object>
</section>
</article>
"""

formatted_report_listing = """<li><a href="{ABSTRACT_PAGE}">{TITLE}</a>.<br>
{AUTHORS}.<br>
Technical Report {REPORT_NUM}, {INSTITUTION}, {MONTH} {YEAR}.<br>
<a href="{PDF_FILE}">[PDF]</a> <a href="{BIB_FILE}">[BIB]</a></li>"""

page_footer = """<footer>
<p><small><a rel="nofollow" href="https://www.cicirello.org/e/">Contact</a></small></p>
<p><small><a href="https://www.cicirello.org/policy/privacy/">Privacy Policy</a></small></p>
<div id="copyright"><small>Copyright &copy; 2008-{CURRENT_YEAR} <a href="https://www.cicirello.org/">Vincent A. Cicirello</a>.</small></div>
</footer>
</body>
</html>
"""
