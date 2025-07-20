#!bin/bash

echo "Starting job scraper"

source venv/bin/activate

python3 scraper/main.py
python3 app/app.py