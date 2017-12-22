import xadmin
from .models import *
# Register your models here.

xadmin.site.register(EduAccount)
xadmin.site.register(EduAcademy)
xadmin.site.register(EduSchool)
xadmin.site.register(EduDepartment)
xadmin.site.register(EduMajor)
xadmin.site.register(EduYearTerm)
xadmin.site.register(Course)
xadmin.site.register(Arrangement)
xadmin.site.register(Asgn)
xadmin.site.register(AsgnVisitRequirement)
xadmin.site.register(Solution)
xadmin.site.register(AsgnReport)
xadmin.site.register(AsgnProblem)
xadmin.site.register(AsgnAccessControl)
xadmin.site.register(JudgeStatus)
xadmin.site.register(Repository)
# admin.site.register(RepositoryFS)