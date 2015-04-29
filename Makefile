# top level makefile


PDF_DIRECTORIES = oldguide ktau paraprof APIs taucompiler perfdmf tutorial taudocs \
perfexplorer tautracereader tautracewriter referenceguide usersguide

HTML_DIRECTORIES = $(PDF_DIRECTORIES) newguide

all: validate pdf html-chunked

deploy:
	@for DIR in referenceguide usersguide ; do \
		echo "building in $$DIR" ; cd $$DIR ; make pdf ; \
		scp $$DIR.pdf ix:/cs/www/hosts/www/Research/tau/tau-$$DIR.pdf ; \
		cd .. ; \
	done;
	@for DIR in newguide ; do \
		echo "building in $$DIR" ; cd $$DIR ; make html-chunked ; cd .. ; \
	done;
	./upload-to-website.sh newguide ix:/cs/www/hosts/www/Research/tau/docs/.

validate:
	@for DIR in $(HTML_DIRECTORIES); do \
		echo "building in $$DIR" ; cd $$DIR ; make validate ; cd .. ; \
	done;

pdf:
	@for DIR in $(PDF_DIRECTORIES); do \
		echo "building in $$DIR" ; cd $$DIR ; make pdf ; cd .. ; \
	done;


html:
	@for DIR in $(HTML_DIRECTORIES); do \
		echo "building in $$DIR" ; cd $$DIR ; make html ; cd .. ; \
	done;

xhtml:
	@for DIR in $(HTML_DIRECTORIES); do \
		echo "building in $$DIR" ; cd $$DIR ; make xhtml ; cd .. ; \
	done;

html-chunked:
	@for DIR in $(HTML_DIRECTORIES); do \
		echo "building in $$DIR" ; cd $$DIR ; make html-chunked ; cd .. ; \
	done;

text:
	@for DIR in $(HTML_DIRECTORIES); do \
		echo "building in $$DIR" ; cd $$DIR ; make text ; cd .. ; \
	done;

clean:
	@for DIR in $(HTML_DIRECTORIES); do \
		echo "building in $$DIR" ; cd $$DIR ; make clean ; cd .. ; \
	done;
