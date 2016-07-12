#!/bin/sh
pushd referenceguide
make pdf
popd
pushd usersguide
make pdf
popd
pushd installguide
make pdf
popd

pushd newguide
make html html-chunked
popd
