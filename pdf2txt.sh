#!/bin/bash

for file in $1/*
do
  pdftotext "$file";
done
