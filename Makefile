all: update render compile

SOURCES = cv.tex data/pubs.tex

update:
	python scripts/getpub.py

render:
	python scripts/render_pubs.py

compile: fr en

fr: $(SOURCES)
	latexmk -jobname=cv_fr -pdf -pdflatex='pdflatex %O -interaction=nonstopmode -synctex=1 "\newif\ifen\newif\iffr\frtrue\input{%S}"' cv

en: $(SOURCES)
	latexmk -jobname=cv_en -pdf -pdflatex='pdflatex %O -interaction=nonstopmode -synctex=1 "\newif\ifen\newif\iffr\entrue\input{%S}"' cv

clean:
	rm -f *.aux *.bbl *.bcf *.blg *.fdb_latexmk *.fls *.log *.xml *.gz
