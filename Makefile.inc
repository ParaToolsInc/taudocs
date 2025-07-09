# Makefile for the tutorial hands-on guide
# $Id: Makefile.inc,v 1.24 2009/11/12 18:33:12 scottb Exp $
#
# WARNING:  Please read the README before using this!

##### ----- CHANGE ONLY WHEN TOOL VERSIONS REQUIRE IT ----- #####
# Setup the XSL reference trees

TOOLS = $(ROOT)/tools
DXSL_BASE = docbook-xsl
#DXSL_VER = -1.74.0
DXSL_VER = -1.69.1
DXSL_DIR = $(TOOLS)/$(DXSL_BASE)$(DXSL_VER)
DXSL_SRC = $(DXSL_BASE)$(DXSL_VER).tar.gz

# Default place to look for admonition and callout images.
# Can be overridden on command line to produce HTML referencing images dir
# located somewhere else.
# NOTE: final "/" required by Java tools is added below
IMAGE_ROOT = $(DXSL_DIR)/images

# XSLT processor Saxon with Xerces parser instead of buggy internal parser
# -Xmx required to boost maximum size of memory pool

SAX_CMD = java -Xmx512m \
        -classpath "$(TOOLS)/saxon.jar:$(DXSL_DIR)/extensions/saxon651.jar:$(TOOLS)/xercesImpl.jar:$(DXSL_DIR)/extensions/xalan2.jar" \
	-Djavax.xml.parsers.DocumentBuilderFactory=org.apache.xerces.jaxp.DocumentBuilderFactoryImpl \
	-Djavax.xml.parsers.SAXParserFactory=org.apache.xerces.jaxp.SAXParserFactoryImpl \
	-Dorg.apache.xerces.xni.parser.XMLParserConfiguration=org.apache.xerces.parsers.XIncludeParserConfiguration \
		com.icl.saxon.StyleSheet < /dev/null

# XSLT-FO processor
#
# Unfortunately, fop.sh is a bit stupid in terms of how it goes about
# finding java.  So it turns out not to be sufficient for java to be
# in your path.  You must either have JAVACMD set to the
# fully-qualified path to the 'java' command (because the script does
# a -x $JAVACMD test), or set JAVA_HOME to the root of the JDK
# installation tree.

JAVACMD = $(shell which java)

#FOP_CMD = env JAVACMD=$(JAVACMD) $(TOOLS)/fop.sh

FOP_VERSION = 2.11
#FOP_DIR = $(TOOLS)/fop-$(FOP_VERSION)/fop
FOP_TARBALL = fop-$(FOP_VERSION)-bin.tar.gz
FOP_URL = https://dlcdn.apache.org/xmlgraphics/fop/binaries/$(FOP_TARBALL)

#FOP_CMD = env JAVACMD=$(JAVACMD) $(FOP_DIR)/fop

#FOP_CMD = $(FOP_DIR)/fop

# The top-level directory that gets created when unzipping
FOP_INSTALL_DIR = $(TOOLS)/fop-$(FOP_VERSION)

# The full, explicit path to the FOP executable script
FOP_CMD = $(FOP_INSTALL_DIR)/fop/fop

# Rule to create the FOP directory by downloading and unzipping
$(FOP_CMD):
	@echo "--- FOP not found. Downloading from Apache... ---"
	curl -L -o $(TOOLS)/$(FOP_TARBALL) $(FOP_URL)
	tar -xzf $(TOOLS)/$(FOP_TARBALL) -C $(TOOLS)
	rm $(TOOLS)/$(FOP_TARBALL)

##### ----- XSLT STYLESHEET PARAMETER SETTINGS ----- #####

# Parameter settings for XSLT stylesheets
#
# Probably want to add admonition graphics and maybe navigation
# graphics at some point.  Check what is needed to relocate the output
# if start using such images.

XSLT_PARAM = use.extensions=1 \
	callouts.extension=1 \
	admon.graphics=1 \
        section.autolabel=1 \
        chapter.autolabel=1 \
	section.label.includes.component.label=1 \
	use.role.for.mediaobject=1

# In this case, the file is generated in the main directory, so
# path to images is directly DXSL_DIR

XSLT_PARAM_HTML = callout.graphics.path=images/ \
	admon.graphics.path=images/ \
	img.src.path=images/ \
        preferred.mediaobject.role="html" \
        profile.condition="html" \
	refentry.xref.manvolnum="0"

# Need to find a way to get DOCTYPE generated in single-file HTML.
# This doesn't work:
#	chunker.output.doctype-public="-//W3C//DTD HTML 4.01 Transitional//EN"


# These will work only in ESXLT-enabled processors
# In this case, graphics are up-and-over relative to where files are generated
XSLT_PARAM_CHUNKEDHTML = chunk.fast=1 \
	chunker.output.indent="yes" \
	callout.graphics.path=$(IMAGE_ROOT)/callouts/ \
	admon.graphics.path=$(IMAGE_ROOT)/ \
	chunker.output.doctype-public="-//W3C//DTD HTML 4.01 Transitional//EN" \
        preferred.mediaobject.role="html" \
        profile.condition="html" \
	refentry.xref.manvolnum="0"

#collect.xref.targets="yes"
XSLT_PARAM_FO = fop1.extensions=1 \
	table.omit.header.at.break=1 \
	callout.graphics.path=$(IMAGE_ROOT)/callouts/ \
	admon.graphics.path=$(IMAGE_ROOT)/ \
        preferred.mediaobject.role="fo" \
        profile.condition="fo" \
	refentry.xref.manvolnum="0" \
	draft.mode="no" indent="yes"


##### ----- USER BUILD STUFF ----- #####

# Stuff to build
#
# Should probably add included files too.  I wonder if there's a
# 'makedepend' for XInclude?
#
# NOTE: For pattern rules to work properly, the main XML file
# (guide.xml) must be first in this list!

.phony: validate $(TARGET)-chunked clean realclean \
	html html-chunked xhtml pdf text man ps

##### ----- These are the main things we want ----- #####

all: validate html-chunked pdf 

##### ----- Shorthands for a bunch of possible targets ----- #####

html: $(TARGET).html
html-chunked: $(TARGET)-chunked
xhtml: $(TARGET).xhtml
pdf: $(TARGET).pdf
ps: $(TARGET).ps
text: $(TARGET).txt

link:
	xsltproc --stringparam collect.xref.targets "only" \
	$(DXSL_DIR)/html/html.xsl $(HEAD).xml

link-chunked:
	xsltproc --stringparam collect.xref.targets "yes" \
	$(DXSL_DIR)/html/html.xsl $(HEAD).xml

##### ----- The real targets ----- #####

man: $(XML_SRCS) $(DXSL_DIR)
	xsltproc --output tmp.xml \
	--stringparam profile.condition "man" \
		$(DXSL_DIR)/profiling/profile.xsl $<
	$(SAX_CMD) tmp.xml $(DXSL_DIR)/manpages/docbook.xsl profile.condition="man"
	rm -f tmp.xml


# Unpack the XSL tree
$(DXSL_DIR): $(TOOLS)/$(DXSL_SRC)
	cd $(TOOLS) ; gunzip -c $(DXSL_SRC) | tar -x
	touch $(DXSL_DIR)

# Validate using xsltproc
validate: $(XML_SRCS)
	xmllint --debug --noout --xinclude --postvalid $(HEAD).xml

$(HEAD).fo: $(XML_SRCS) $(DXSL_DIR)

# Single file containing everything
$(TARGET).html: $(XML_SRCS) $(DSXL_DIR)

# Chunked (chapter-per-file) rendering
$(TARGET)-chunked: $(TARGET)-chunked/index.html
# $(TARGET)-chunked/index.html: $(XML_SRCS) $(DXSL_DIR)
# 	-mkdir $(@D)
# 	$(SAX_CMD) $< $(DXSL_DIR)/html/profile-chunk.xsl \
# 		$(XSLT_PARAM) $(XSLT_PARAM_CHUNKEDHTML) \
# 		base.dir=$(TARGET)-chunked/ 


$(TARGET)-chunked/index.html: $(XML_SRCS) $(DXSL_DIR)
	-mkdir -p $(@D)
	$(SAX_CMD) $< $(TOOLS)/html_chunked_custom.xsl \
		$(XSLT_PARAM) $(XSLT_PARAM_CHUNKEDHTML) \
		base.dir=$(TARGET)-chunked/ 
	cd $(@D) ; ./../$(TOOLS)/create_html_redirects.sh ; 
	
#current.docid=$(DOC_ID) \
#VXtarget.database.document="../olinkdb.xml" \

$(TARGET).xhtml: $(XML_SRCS) $(DXSL_DIR)

clean:
	-rm -rf $(TARGET).pdf $(HEAD).fo $(TARGET).html $(TARGET).xhtml $(TARGET).txt $(TARGET)-chunked 

realclean: clean
	-rm -rf $(DXSL_DIR) $(TARGET)-chunked

##### ----- PATTERN RULES ----- #####

# $(HEAD).fo: $(HEAD).xml $(DXSL_DIR)
# 	$(SAX_CMD) -o $@ $< $(DXSL_DIR)/fo/profile-docbook.xsl \
#                 $(XSLT_PARAM) \
# 		$(XSLT_PARAM_FO) 


$(HEAD).fo: $(HEAD).xml $(DXSL_DIR)
	$(SAX_CMD) -o $@ $< $(TOOLS)/fo_custom.xsl \
                $(XSLT_PARAM) \
		$(XSLT_PARAM_FO) 


# This target outputs a single HTML file containing the entire document.
# If you want a "chunked" (file-per-chapter) rendering, you probably
# want to collect all of them in a subdirectory, in which case you
# need a different (non-pattern) rule to build it.
# $(TARGET).html: $(HEAD).xml $(DXSL_DIR)
# 	$(SAX_CMD) -o $@ $< $(DXSL_DIR)/html/profile-docbook.xsl \
#                 $(XSLT_PARAM) \
# 		$(XSLT_PARAM_HTML)

$(TARGET).html: $(HEAD).xml $(DXSL_DIR)
	$(SAX_CMD) -o $@ $< $(TOOLS)/html_custom.xsl \
                $(XSLT_PARAM) \
		$(XSLT_PARAM_HTML)
	cat $(TARGET).html | sed -e 's@src=\"images/[^>]*/@src=\"images/@g' > .tmp.html
	mv .tmp.html $(TARGET).html


$(TARGET).xhtml: $(HEAD).xml $(DXSL_DIR)
	$(SAX_CMD) -o $@ $< $(DXSL_DIR)/xhtml/profile-docbook.xsl \
		$(XSLT_PARAM) \
		$(XSLT_PARAM_XHTML)

$(TARGET).pdf: $(HEAD).fo $(DXSL_DIR) $(FOP_CMD)
	sed 's/content-width="auto"/content-width="scale-to-fit"/g' $< | \
	sed 's/\bwidth="auto"/width="100%"/g' | \
	sed 's/keep-with-next.within-column="always"//g' | \
	sed 's/keep-together.within-column="always"/keep-together.within-column="auto"/g' | \
	sed 's/border-before-width.conditionality="retain"//g' | \
	sed 's/<fo:table-header start-indent="0pt" end-indent="0pt">/<fo:table-header start-indent="0pt" end-indent="0pt" keep-with-next.within-column="auto">/g' | \
	sed 's/<fo:table-body start-indent="0pt" end-indent="0pt">/<fo:table-body start-indent="0pt" end-indent="0pt" keep-together.within-page="auto" page-break-inside="auto">/g' \
	> $(HEAD).fo.fixed
	$(FOP_CMD) -fo $(HEAD).fo.fixed -pdf $@

$(TARGET).ps: $(HEAD).fo $(DXSL_DIR) $(FOP_CMD)
	$(FOP_CMD) -fo $< -ps $@

$(TARGET).txt: $(TARGET).html
	links -dump $(TARGET).html > $(TARGET).txt

##### ----- OUTDATED OR NON-WORKING TARGETS ----- #####

# guide.pdf: $(XML_SRCS)
# 	xmlto --skip-validation --extensions pdf guide.xml

# # CURRENTLY FAILS WITH:
# # [ERROR] org.apache.fop.apps.FOPException: fo:flow must contain block-level children
# guide2.pdf: $(XML_SRCS) $(DXSL_DIR)
# 	$(FOP_CMD) -xsl $(DXSL_DIR)/fo/docbook.xsl -xml guide.xml -pdf guide2.pdf

# # As built here, the starting point will be guide-html/index.html
# guide-html: $(XML_SRCS)
# 	-mkdir guide-html
# 	xmlto --skip-validation --extensions -o guide-html html guide.xml

