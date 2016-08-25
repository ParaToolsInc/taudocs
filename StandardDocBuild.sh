#!/bin/bash
pushd ./referenceguide/
make clean
make pdf
popd

pushd ./usersguide/
make clean
make pdf
popd

pushd ./installguide/
make clean
make pdf
popd

pushd ./newguide/
make clean
make html html-chunked
popd
