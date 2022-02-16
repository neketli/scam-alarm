import requests
#parsing = str(sys.argv[1])
parsing = input()
try:

    res = requests.get(parsing)

    if res.status_code == 200:
        print(1)
    else:
        print(0)


except Exception:
    print(0)