pkill -f "master\.py"
pkill -f "map\.py [0-90000]"
pkill -f "reduce\.py [0-90000]"
python restart.py