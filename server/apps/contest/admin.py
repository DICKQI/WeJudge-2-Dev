from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Contest)
admin.site.register(ContestAccount)
admin.site.register(ContestProblem)
admin.site.register(ContestSolution)
admin.site.register(ContestCodeCrossCheck)
admin.site.register(FAQ)
admin.site.register(Notice)
admin.site.register(JudgeStatus)
