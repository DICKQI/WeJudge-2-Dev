from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Problem)
admin.site.register(ProblemSet)
admin.site.register(AccountProblemVisited)
admin.site.register(ProblemSetItem)
admin.site.register(ProblemSetSolution)
admin.site.register(JudgeStatus)
admin.site.register(TCGeneratorStatus)
admin.site.register(CodeDrafts)
