import sys,json
from migrate import Store
store=Store(sys.argv[1])
for line in sys.stdin:
    print(json.dumps(store.apply(json.loads(line))),flush=True)
