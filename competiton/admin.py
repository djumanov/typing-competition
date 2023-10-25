from django.contrib import admin
from . import models


admin.site.register((
    models.Profession,
    models.Teacher,
    models.Group,
    models.Student,
    models.Stage,
    models.Result
))

