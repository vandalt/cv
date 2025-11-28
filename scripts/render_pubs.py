# %%
from pathlib import Path
import json
import warnings

data_dir = Path(__file__).parent.parent / "data"

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=SyntaxWarning)
    from utf8totex import utf8totex

PUB_DICT = {
    "The Astronomical Journal": "AJ",
    "Astronomy and Astrophysics": "A\\&A",
    "Publications of the Astronomical Society of the Pacific": "PASP",
}

with open(data_dir / "papers.json", "r") as f:
    pubs = json.load(f)

# %%


def process_author(author: str):
    last_name, first_name = author.split(", ")
    if len(first_name) > 1:
        first_name = first_name[0] + "."
    updated_name = f"{last_name}, {first_name}"
    if "Vandal" in author:
        updated_name = f"\\textbf{{{updated_name}}}"
    return updated_name


def dict2tex(pub: dict):
    authors = pub["authors"]
    authors = [process_author(a) for a in authors]
    if len(authors) > 3:
        first_author = authors[0]
        me_first = "Vandal" in first_author

        author_field = f"{first_author} et al."
        if not me_first:
            author_field += " (\\langen{including}\\langfr{incluant} \\textbf{Vandal, T.})"
    else:
        author_field = ", ".join(authors)

    pub_name = PUB_DICT.get(pub["pub"], pub["pub"])
    pub_field = ", ".join([pub_name, pub["volume"], pub["page"]])
    if len(pub["doi"]) > 0:
        pub_field = f"\\href{{https://doi.org/{pub['doi'][0]}}}{{{pub_field}}}"
    pub_field += "."
    title_tex = utf8totex(pub["title"])
    title_field = f"\\textit{{{title_tex}}}."
    year_field = pub["year"] + ","
    cv_item = " ".join([author_field, title_field, year_field, pub_field])
    cv_item = f"\\cvitem{{}}{{{cv_item}}}"
    return cv_item


pubs = sorted(pubs, key=lambda p: p["pubdate"], reverse=True)
first_pubs = [pub for pub in pubs if "Vandal" in pub["authors"][0]]
other_pubs = [pub for pub in pubs if "Vandal" not in pub["authors"][0]]
pubs = first_pubs + other_pubs
tex_pubs = [dict2tex(pub) for pub in pubs]

output_file = data_dir / "pubs.tex"
with open(output_file, "w") as f:
    f.write("\n".join(tex_pubs))
