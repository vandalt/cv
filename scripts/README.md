# Scripts I use for my CV

You need to install the [`ads`](https://ads.readthedocs.io/en/latest/) package.

## Getting publications from ADS

This will fetch the publications and put them in the `data/` directory as JSON lists of dictionaries.

```bash
python getpub.py
```

## Rendering publications as LaTeX

```bash
python render_pubs.py
```
