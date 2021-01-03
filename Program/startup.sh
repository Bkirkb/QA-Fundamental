#!/bin/bash
cd /opt/QA-Fundamental/Program
sudo python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
sudo systemctl stop fundamental.service
sudo systemctl daemon-reload
pytest --cov=application --cov-report html