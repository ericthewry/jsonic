from ic import *

data = {
    "employee" : {
        "name": "Frank Nelson",
        "age": 28,
        "eid" : 47
    },
    "data" : {
        "eid": 47,
        "salary": 100 * 1000.0,
        "team" : "r&d"
    }
}

def pos(typ):
    return Refine(Type(typ),lambda x: x >= typ(0))

dictic = \
    Refine(
        Dict(
            employee = Dict(
                name = Type(str),
                age = pos(int),
                eid = Type(int)
            ),
            data = Dict(
                eid = Type(int),
                salary = pos(float),
                team = Enum("r&d", "hr", "csuite")
            )
        ), lambda d: d["employee"]["eid"] == d["data"]["eid"])

dictic.check(data)