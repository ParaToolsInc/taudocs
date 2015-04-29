# taudocs
TAU documentation for user interaction and API documentation.

Here are the basic guidelines for using docbook:

See the bottom of this README for instructions on installing the documentation.

use make html-chunked to create linked web-pages.
use make pdf to create a pdf.

sometimes you need to first 'make clean' before creating documents to
make sure that the most recent changes are incorporated.

The following characters have special meaning to docbook: '<','>','&'.
To print '<', type '&lt;' , for '>' type '&gt;' and for '&' type '&amp;'.

If you wish to search and replace these characters in an entire document
first search and replace '&' for '&amp;' so the the '&' in '&lt;' or
'&gt; is not changed.



Important tags and that should be used throughout the Document:

checkout http://www.docbook.org/tdg/en/html/docbook.html for a more
complete list of available tags.

<chapter id="[chapter title]">  Denotes the beginning and end of chapters.

<sect1 id="[section title]">    Denotes the major section within a chapter.

<sect2> Denotes the beginning and end of every subsection within the
document. Use this tag often, as it will help the user find information
quickly.

<title> Every chapter, section and subsection should have one title
immediately following the <chapter>, <sect1> or <sect2> tag.

<itemizedlist> Begins a list.

<orderedlist> Begins a ordered list.

<listitem> Denotes an element of either a itemizedlist or a orderedlist.

<para> Should be used regardless of the size of paragraph, in some cases
for a single word.

<parameter> Denotes a list arguments for a function.

<literal> Used to have the text inclosed in this tag be printed without
any formating. Use for variable names, method names or numbers.

<screen> Used to print text as it would be displayed on a computer. Use
for code examples, or computer output. Any line inside a <screen> tag
must not exceed 65 charaters in length (including whitespace). If you
need to do text wrapping please follow these guidelines:

1) Shell commands that wrap should wrap in a way that preserve the
ability to cut and paste, let the last character on the line be a slash,
with the following line indented. For example:
<screen> % mpirun -np 4
Some very long winded \
    command
</screen>

2) Program output should be formatted by hand to be visibly appealing
and to not confuse the reader. For example, if we're showing output
from a help command:
<screen>
% paraprof -h
-x --exx     I'm describing some very
              long option
-h --help    This message
</screen>

3) Makefiles should be modified to be syntactically correct, which
means slashes for line continuations, except on comments, where the
next line should begin with a pound. For example:
<screen>
# This is a long Makefile
# comment
thing: thing.cpp
     $(CXX) thing.cpp -o thing $(LIB) \
     $(INCLUDE)
</screen>


-------------------------------------------------------------------
Installing the Documentation
-------------------------------------------------------------------

Here's a cheat sheet for the TAUdocs

export CVSROOT=ix.cs.uoregon.edu:/research/paraducks2/cvs-src/master
cvs co taudocs

To Make PDFs:
cd referenceguide
make pdf
cp referenceguide.pdf
cd userguide
make pdf
cp userguide.pdf

To make html (for all of the guides)
cd newguide
make html newguide-chunked
cp newguide-chunked/

The pdfs are here (on ix):
cd /cs/www/hosts/www/Research/tau

The html here (on ix):
/cs/www/hosts/www/Research/tau/docs/newguide

