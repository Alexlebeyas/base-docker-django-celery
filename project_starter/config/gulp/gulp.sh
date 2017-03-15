#!/usr/bin/env bash

cd ./PROJECT_NAME/gulp
if [ ! -d "node_modules" ]; then
    npm install
    gulp styles_vendors
    gulp styles_plugins
    gulp fonts_vendors
fi
gulp watch