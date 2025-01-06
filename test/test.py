from requests.packages import target

dict_1 = {
    "a":11,
    "b":1
}

if "a" in dict_1:
    print("Y")
    print(dict_1.get("a"))
else:
    print('N')