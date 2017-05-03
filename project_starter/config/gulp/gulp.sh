#!/usr/bin/env bash

cd ./PROJECT_NAME/gulp
if [ ! -d "node_modules" ]; then
    npm install
    gulp vendors
fi
gulp watch