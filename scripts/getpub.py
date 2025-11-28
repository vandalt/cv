# Using this as reference: https://github.com/dfm/cv/blob/main/scripts/update-astro-pubs
import json
from pathlib import Path
import ads
from ads.search import Article

query = ads.SearchQuery(
    author="Vandal, T",
    fl=[
        "first_author",
        "author",
        "title",
        "bibcode",
        "doctype",
        "year",
        "pubdate",
        "read_count",
        "citation_count",
        "property",
        "identifier",
        "doi",
        "pub",
        "orcid_pub",
        "orcid_user",
        "orcid_other",
        "page",
        "volume",
        "aff",
    ],
    max_pages=100,
    sort="date",
)
# Convert to a list for ease of use
papers: list[Article] = list(query)

# I share my name with someone else... Need to do some filtering
my_papers = []
software = []
datasets = []
rejected_papers = []
for paper in papers:
    # First do a cut based on year: 100% sure not my paper if before 2020
    year = paper.year
    if year.isdigit() and year < "2020":
        continue

    # Remove doctypes that won't be used anyways: they add noise to selection
    if paper.doctype in ["dataset", "software", "abstract", "techreport"]:
        if paper.doctype == "software":
            software.append(paper)
        elif paper.doctype == "dataset":
            datasets.append(paper)
        continue

    # Only keep affiliations that match MONTréal
    good_aff = any(map(lambda a: "mont" in a.lower(), paper.aff))
    if not good_aff:
        rejected_papers.append(paper)
        continue

    # Papers that passed filters are mine
    my_papers.append(paper)


# Save everything as JSON
def article2dict(article: Article) -> dict:
    return {
        "doctype": article.doctype,
        "authors": article.author,
        "year": article.year,
        "pubdate": article.pubdate,
        "doi": article.doi,
        "title": article.title[0],
        "pub": article.pub,
        "volume": article.volume,
        "page": article.page[0] if article.page is not None else None,
        "citations": article.citation_count or 0,
        "url": "https://ui.adsabs.harvard.edu/abs/" + article.bibcode,
    }


all_dicts = dict(
    papers=list(map(article2dict, my_papers)),
    software=list(map(article2dict, software)),
    datasets=list(map(article2dict, datasets)),
    rejected=list(map(article2dict, rejected_papers)),
)

data_dir = Path(__file__).parent.parent / "data"
data_dir.mkdir(exist_ok=True)

for key, val in all_dicts.items():
    output_file = data_dir / f"{key}.json"
    with open(output_file, "w") as f:
        json.dump(val, f, indent=2)
