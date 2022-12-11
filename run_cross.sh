#!/bin/bash

source venv/bin/activate
cd bestway
python bestway_runbase.py -ge -mcross
cd -
cd booker
python booker_runbase.py -bs -mcross