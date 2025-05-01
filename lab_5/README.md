## Лабораторная работа №5
### Вариант №5 ("Мессенджер")

Задание:
1. Для данных, хранящихся в реляционной базе PotgreSQL реализуйте шаблон сквозное чтение и сквозная запись (Пользователь/Клиент …);
2. В качестве кеша – используйте Redis
3. Замерьте производительность запросов на чтение данных с и без кеша с использованием утилиты wrk https://github.com/wg/wrk изменяя количество потоков из которых производятся запросы (1, 5, 10)
4. Актуализируйте модель архитектуры в Structurizr DSL
5. Ваши сервисы должны запускаться через docker-compose командой dockercompose up (создайте Docker файлы для каждого сервиса)

### Результаты wrk:
```shell
      1 thread:
Without redis:
Running 10s test @ http://localhost:8000
  1 threads and 10 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   131.00ms   24.98ms 179.53ms   72.94%
    Req/Sec    81.96     31.45   131.00     67.90%
  Latency Distribution
     50%  130.77ms
     75%  149.54ms
     90%  159.20ms
     99%  161.66ms
  754 requests in 10.01s, 529.91KB read
Requests/sec:     75.29
Transfer/sec:     52.91KB
With redis:
Running 10s test @ http://localhost:8000
  1 threads and 10 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    57.94ms   10.22ms  89.76ms   78.12%
    Req/Sec   172.89     39.25   240.00     74.00%
  Latency Distribution
     50%   50.27ms
     75%   60.20ms
     90%   75.32ms
     99%   79.99ms
  1723 requests in 10.01s, 302.87KB read
Requests/sec:    172.12
Transfer/sec:     30.26KB
      5 threads:
Without redis:
Running 10s test @ http://localhost:8000
  5 threads and 10 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   127.84ms   29.27ms 209.61ms   73.09%
    Req/Sec    17.21      5.61    40.00     62.27%
  Latency Distribution
     50%  130.51ms
     75%  149.71ms
     90%  159.34ms
     99%  209.37ms
  784 requests in 10.10s, 137.81KB read
Requests/sec:     77.62
Transfer/sec:     13.64KB
With redis:
Running 10s test @ http://localhost:8000
  5 threads and 10 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    62.77ms   11.41ms  99.92ms   55.40%
    Req/Sec    31.76      9.05    40.00     66.47%
  Latency Distribution
     50%   60.05ms
     75%   69.93ms
     90%   79.82ms
     99%   89.82ms
  1592 requests in 10.10s, 281.06KB read
Requests/sec:    157.63
Transfer/sec:     27.83KB
      10 threads:
Without redis:
Running 10s test @ http://localhost:8000
  10 threads and 10 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   125.34ms   30.25ms 170.18ms   71.84%
    Req/Sec     8.82      3.19    20.00     65.84%
  Latency Distribution
     50%  130.25ms
     75%  149.23ms
     90%  159.51ms
     99%  169.82ms
  799 requests in 10.10s, 180.90KB read
Requests/sec:     79.12
Transfer/sec:     17.91KB
With redis:
Running 10s test @ http://localhost:8000
  10 threads and 10 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    59.22ms    9.48ms  90.30ms   77.13%
    Req/Sec    16.84      4.65    20.00     68.53%
  Latency Distribution
     50%   59.92ms
     75%   60.39ms
     90%   70.16ms
     99%   80.50ms
  1692 requests in 10.10s, 298.64KB read
Requests/sec:    167.59
Transfer/sec:     29.58KB
```