local frandom = io.open("/dev/urandom", "rb")
local d = frandom:read(4)
math.randomseed(d:byte(1) + (d:byte(2) * 256) + (d:byte(3) * 65536) + (d:byte(4) * 4294967296))

number =  math.random(0,99)
request = function()
    headers = {}
    headers["Content-Type"] = "application/json"
    body = string.format('{"fields": ["login", "name", "surname"], "value": "user%s"}', number)
    return wrk.format("POST", "/user/search/redis", headers, body)
end