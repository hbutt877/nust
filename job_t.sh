while true; do
    pkill python;
    pkill chrome;
    timeout 300 python3 t.py;
done
