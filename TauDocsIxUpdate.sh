#!/bin/sh
#ssh ix mkdir -p  hold-tau-docs

cp installguide/installguide.pdf ./tau-installguide.pdf
cp usersguide/usersguide.pdf ./tau-usersguide.pdf
cp referenceguide/referenceguide.pdf ./tau-referenceguide.pdf
#scp installguide/installguide.pdf ix:~/hold-tau-docs/tau-installguide.pdf
#scp usersguide/usersguide.pdf ix:~/hold-tau-docs/tau-usersguide.pdf
#scp referenceguide/referenceguide.pdf ix:~/hold-tau-docs/tau-referenceguide.pdf
scp -r ./tau-installguide.pdf ./tau-usersguide.pdf ./tau-referenceguide.pdf newguide/newguide-chunked/ ix:~/hold-tau-docs/
#scp -r referenceguide/referenceguide-chunked/* ix:~/hold-tau-docs/newguide-chunked
ssh ix "cp -r /research/paraducks/tauwww/docs/newguide hold-tau-docs/newguide.bak.$(date +%Y%m%d_%H%M%S); cp -r hold-tau-docs/newguide-chunked/* /research/paraducks/tauwww/docs/newguide; cp -r hold-tau-docs/*.pdf /research/paraducks/tauwww/"

echo "Don't forget to update ix:/research/paraducks/tauwww/docs.php"


