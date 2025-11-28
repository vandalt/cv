all: fr en

SOURCES = cv.tex data/pubs.tex

fr: $(SOURCES)
	latexmk -jobname=cv_fr -pdf -pdflatex='pdflatex %O -interaction=nonstopmode -synctex=1 "\newif\ifen\newif\ifpt\pttrue\input{%S}"' cv

en: $(SOURCES)
	latexmk -jobname=cv_en -pdf -pdflatex='pdflatex %O -interaction=nonstopmode -synctex=1 "\newif\ifen\newif\ifpt\entrue\input{%S}"' cv

clean:
	rm -f *.aux *.bbl *.bcf *.blg *.fdb_latexmk *.fls *.log *.xml *.gz
