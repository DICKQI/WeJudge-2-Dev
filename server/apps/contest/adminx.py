import xadmin
from .models import *
# Register your models here.

xadmin.site.register(Contest)
xadmin.site.register(ContestAccount)
xadmin.site.register(ContestProblem)
xadmin.site.register(ContestSolution)
xadmin.site.register(ContestCodeCrossCheck)
xadmin.site.register(FAQ)
xadmin.site.register(Notice)
xadmin.site.register(JudgeStatus)
