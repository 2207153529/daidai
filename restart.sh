pid=$(netstat -tunlp | grep 8800 | awk '{print $7}')
pid=${pid%/*}
kill -9 $pid
sleep 3
python3 bot.py
