while true; do
    pkill python;
    pkill chrome;
    timeout 200 python3 signup.py;
done
