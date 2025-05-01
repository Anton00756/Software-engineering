echo "      1 thread:"
echo "Without redis:"
wrk -d 10 -t 1 -c 10 --latency -s wrk/get_without_redis.lua http://localhost:8000
echo "With redis:"
wrk -d 10 -t 1 -c 10 --latency -s wrk/get.lua http://localhost:8000
echo "      5 threads:"
echo "Without redis:"
wrk -d 10 -t 5 -c 10 --latency -s wrk/get_without_redis.lua http://localhost:8000
echo "With redis:"
wrk -d 10 -t 5 -c 10 --latency -s wrk/get.lua http://localhost:8000
echo "      10 threads:"
echo "Without redis:"
wrk -d 10 -t 10 -c 10 --latency -s wrk/get_without_redis.lua http://localhost:8000
echo "With redis:"
wrk -d 10 -t 10 -c 10 --latency -s wrk/get.lua http://localhost:8000