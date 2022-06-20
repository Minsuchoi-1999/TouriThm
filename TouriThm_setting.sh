#!/usr/bin/bash

sudo apt update
sudo apt install python3-pip
pip--version
sudo apt install python-is-python3
pip install bs4
pip install html_table_parser
pip install pandas
pip install openpyxl
pip install nltk
pip install elasticsearch
pip install flask
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.2.0-linux-x86_64.tar.gz
tar xvzf elasticsearch-8.2.0-linux-x86_64.tar.gz
cd elasticsearch-8.2.0/
./bin/elastic/search
