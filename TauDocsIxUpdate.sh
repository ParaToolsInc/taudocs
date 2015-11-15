#!/bin/sh
ssh ix mkdir -p  hold-tau-docs
scp installguide/installguide.pdf ix:~/hold-tau-docs/tau-installguide.pdf
scp usersguide/usersguide.pdf ix:~/hold-tau-docs/tau-usersguide.pdf
scp referenceguide/referenceguide.pdf ix:~/hold-tau-docs/tau-referenceguide.pdf
scp -r newguide/newguide-chunked/ ix:~/hold-tau-docs/
ssh ix cp -r /research/paraducks/tauwww/docs/newguide hold-tau-docs/newguide.bak.$(date +%Y%m%d_%H%M%S)
ssh ix cp -r hold-tau-docs/newguide-chunked/* /research/paraducks/tauwww/docs/newguide




