from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(EduAccount)
admin.site.register(EduAcademy)
admin.site.register(EduSchool)
admin.site.register(EduDepartment)
admin.site.register(EduMajor)
admin.site.register(EduYearTerm)
admin.site.register(Course)
admin.site.register(Arrangement)
admin.site.register(Asgn)
admin.site.register(AsgnVisitRequirement)
admin.site.register(Solution)
admin.site.register(AsgnReport)
admin.site.register(AsgnProblem)
admin.site.register(AsgnAccessControl)
admin.site.register(JudgeStatus)
admin.site.register(Repository)
# admin.site.register(RepositoryFS)