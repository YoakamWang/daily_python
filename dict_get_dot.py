class DotDict(dict):
    def __init__(self, *args, **kwargs):
        super(DotDict, self).__init__(*args, **kwargs)

    def __getattr__(self, key):
        value = self[key]
        if isinstance(value, dict):
            value = DotDict(value)
        return value

info={
    "student":{
        "name":"zhangsan",
        "age":20,
        "male":"man"
    },
    "teacher":{
        "name":"Mr Wang",
        "age":25,
        "male":"woman",
        "course":{
            "math":"Friday",
            "english":"Monday"
        }
    }
}

dot_info=DotDict(info)
print(dot_info.student)
print(dot_info.student.name)
print(dot_info.teacher.name)
print(dot_info.teacher.course.math)
