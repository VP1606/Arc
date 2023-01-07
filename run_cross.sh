#!/bin/bash
echo "DB CROSS MODE"
. venv/bin/activate
cd bestway
python bestway_runbase.py -ge -mcross
cd -
cd booker
python booker_runbase.py -bs -mcross
cd -
echo "SQL Cleanup..."
#python sql_extension.py
python extension_lite.py