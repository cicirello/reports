# Site generator for https://reports.cicirello.org/
# Copyright (c) 2024 Vincent A. Cicirello. All rights reserved.
#
# This site generator is almost certainly useless to anyone other than me.
# It is highly customized to generate one specific website. Therefore, I am
# not licensing it to others. Notice the "All rights reserved" in the
# copyright notice at the top.

import json, os
from report import Report
from page import PageBuilder

def load_bib_file(additional_info, bib_file="reports.bib"):
    """LaTeX bib file with BibTeX for the reports, including the abstracts.

    Keyword arguments:
    additional_info - additional metadata no in the bib file
    bib_file - the BibTeX file.
    """
    reports = []
    with open(bib_file, "r", encoding="utf-8") as bib:
        current = []
        for line in bib:
            if line.startswith("@techreport"):
                if len(current) > 0:
                    reports.append(Report("".join(current).strip(), additional_info))
                    current = []
            current.append(line)
        reports.append(Report("".join(current).strip(), additional_info))
    return reports

def make_dirs(reports):
    """Create any directories that we need that don't already exist.

    Keyword arguments:
    reports - An iterable of Report objects
    """
    for r in reports:
        directory = r.target_directory()
        if not os.path.isdir(directory):
            os.makedirs(directory)

def make_bib_files(reports):
    """Creates BibTeX files for all of the reports.

    Keyword arguments:
    reports - An iterable of Report objects
    """
    for r in reports:
        r.output_bibtex_file()

def make_svg_files(reports):
    """Creates svg files for all of the reports.

    Keyword arguments:
    reports - An iterable of Report objects
    """
    for r in reports:
        r.output_svg_file()

def make_web_pages(builder, reports):
    """Creates abstract pages for all of the reports.

    Keyword arguments:
    builder - the PageBuilder
    reports - An iterable of Report objects
    """
    for r in reports:
        with open(r.target_directory() + "/index.html", "w", encoding="utf-8") as f:
            f.write(builder.build_report_page(r))

def make_home_page(builder, reports):
    """Creates the site homepage.

    Keyword arguments:
    builder - the PageBuilder
    reports - An iterable of Report objects
    """
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(builder.build_home_page(reports))

def make_404(builder):
    """Creates the 404 page.

    Keyword arguments:
    builder - the PageBuilder
    """
    with open("404.html", "w", encoding="utf-8") as f:
        f.write(builder.build_404())

def load_additional():
    """Loads additional-info.json which contains additional
    report metadata not otherwise in the bib file."""
    with open(".generator/additional-info.json", "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    additional_info = load_additional()
    reports = load_bib_file(additional_info)
    reports.sort()
    make_dirs(reports)
    make_bib_files(reports)
    make_svg_files(reports)
    builder = PageBuilder()
    make_web_pages(builder, reports)
    make_home_page(builder, reports)
    make_404(builder)

if __name__ == "__main__":
    main()
    
    
    
