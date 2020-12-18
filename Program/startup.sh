#!/bin/bash
export DATABASE_URI="mysql+pymysql://root:brendankirkby99300@35.246.19.71/FishingCompanion"
export SECRET_KEY="ssssssshhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh"
cd /opt/QA-Fundamental/Program
sudo python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 app.py