import xadmin

# Register your models here.
from .models import *

xadmin.site.register(Problem)
xadmin.site.register(ProblemSet)
xadmin.site.register(AccountProblemVisited)
xadmin.site.register(ProblemSetItem)
xadmin.site.register(ProblemSetSolution)
xadmin.site.register(JudgeStatus)
xadmin.site.register(TCGeneratorStatus)
xadmin.site.register(CodeDrafts)
