之后会用到的

{% include "nav.html" %}

import mongoengine
class Student(mongoengine.Document):
    name = mongoengine.StringField(max_length=16)
    age = mongoengine.IntField(default=1)

settings.py
# 将原来的DataBases置空
DATABASES = {
    'default': {
        'ENGINE': None,
    }
}

from mongoengine import connect
connect("xxx")   


# 获取所有name="老王"的数据
res = models.Student.objects.filter(name="老王")

小心mongoengin的坑，版本用的0.13.0