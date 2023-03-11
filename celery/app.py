from tasks import add,add_sleep

res = add.delay(8,45641)
print(res.get(timeout=1))

print(add_sleep.delay(4,8).get(timeout=88))