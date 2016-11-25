#!/usr/bin/env bash

cd  ~/workspace/

FILES=`find ./modules/ -type f -name "*.py"`
for f in './app.py' './config.py' $FILES
do
    yapf $f --style='{based_on_style: pep8, indent_width: 2}' -i
done