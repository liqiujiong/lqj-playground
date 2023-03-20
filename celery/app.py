from tasks import add,add_sleep,fetch_ip

res = fetch_ip.delay()
print(res.get())
# print(res.get(timeout=10))

# res = add.delay(1,2)
# print(res.get(timeout=10))

# print(add_sleep.delay(4,8).get(timeout=88))