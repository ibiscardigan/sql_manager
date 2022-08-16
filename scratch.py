import commonsql.classes as classes
from inspect import getmembers

test = classes.field("test", "INT")

expected_keys = getmembers(classes.field.__init__)[0][1]

print(type(expected_keys))

for key in expected_keys:
    print(key)