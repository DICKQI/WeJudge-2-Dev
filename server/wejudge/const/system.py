# -*- coding: utf-8 -*-
# coding:utf-8

__author__ = 'lancelrq'

WEJUDGE_ACCOUNT_SESSION = 'wejudge_account_session'
WEJUDGE_EDU_ACCOUNT_SESSION = 'wejudge_education_session'
WEJUDGE_CONTEST_ACCOUNT_SESSION = 'wejudge_contest_session'
WEJUDGE_COOKIE_HMAC_SALT = '2565ebcbfe867bacca4f77b72d63c5dbd0d8316bbb5bb7fc996c57568d8b654f'

WEJUDGE_ACCOUNT_COOKIE_TOKEN_KEY = 'wejudge_login_token'
WEJUDGE_ACCOUNT_COOKIE_SIGNATURE_KEY = 'wejudge_login_signature'
WEJUDGE_CONTEST_ACCOUNT_COOKIE_TOKEN_KEY = 'wejudge_contest_login_token'
WEJUDGE_EDU_ACCOUNT_COOKIE_TOKEN_KEY = 'wejudge_education_login_token'

WEJUDGE_CONTEST_ACCOUNT_SESSION_SIGNATURE_KEY = 'wejudge_contest_session_signature'
WEJUDGE_EDU_ACCOUNT_SESSION_SIGNATURE_KEY = 'wejudge_education_session_signature'
WEJUDGE_ACCOUNT_COOKIE_EXPIRE_TIME = 30 * 86400

WEJUDGE_EDUCATION_TERM_KEY = 'wejudge_edu_school_%s_term'
WEJUDGE_GENERAL_PENATLY_TIME = 1200

WEJUDGE_ACCOUNT_PASSWORD_SALT = '0A888E506D66D170E6DE7E2B'
WEJUDGE_ACCOUNT_LOGIN_RETRY_TOTAL = 10
WEJUDGE_ACCOUNT_LOGIN_RETRY_WAIT_TIME = 120
WEJUDGE_ACCOUNT_LOGIN_SESSION_RETRY_TIME = 'wejudge_login_retry_time'

WEJUDGE_URLS_EXPORT_EXCEPT = [

]       # URL暴露接口屏蔽项目

WEJUDGE_COMPILER_COMMAND = {
    1: 'gcc %s -o %s -ansi -fno-asm -Wall -std=c99 -lm',
    2: 'g++ %s -o %s -ansi -fno-asm -Wall -lm',
    4: 'javac -encoding utf-8 %s -d %s'
}

WEJUDGE_CODE_FILE_EXTENSION = {
    1: '.c',
    2: '.cpp',
    4: '.java',
    8: '.py',
    16: '.py'
}

WEJUDGE_PROGRAM_LANGUAGE_CALLED = {
    1: "GNU C",
    2: "GNU C++",
    4: "Java",
    8: "Python 2",
    16: "Python 3"
}

# 教学系统账户角色称呼
WEJUDGE_EDU_ACCOUNT_ROLES_CALLED = {
    0: "学生",
    1: "助教",
    2: "教师",
    3: "教务"
}

# 教学系统账户角色描述性称呼
WEJUDGE_EDU_ACCOUNT_ROLES_FRIENDLY_CALLED = {
    0: "同学",
    1: "助教",
    2: "老师",
    3: "老师"
}


# WeJudge教学系统账户角色描述
class WEJUDGE_EDU_ACCOUNT_ROLES:

    STUDENT = 0
    ASSISTANT = 1
    TEACHER = 2
    MANAGER = 3

    @staticmethod
    def exists(role):
        if int(role) in WEJUDGE_EDU_ACCOUNT_ROLES.roles():
            return True
        else:
            return False

    @staticmethod
    def roles():
        cls = WEJUDGE_EDU_ACCOUNT_ROLES
        return (
            cls.STUDENT,
            cls.ASSISTANT,
            cls.TEACHER,
            cls.MANAGER,
        )

    @staticmethod
    def call(role):
        return WEJUDGE_EDU_ACCOUNT_ROLES_CALLED.get(role, "")

    @staticmethod
    def call_friendly(role):
        return WEJUDGE_EDU_ACCOUNT_ROLES_FRIENDLY_CALLED.get(role, "")


# 教学系统账户角色称呼
WEJUDGE_CONTEST_ACCOUNT_ROLES_CALLED = {
    0: "参赛者",
    1: "裁判",
    2: "总管理员"
}

# 教学系统账户角色描述性称呼
WEJUDGE_CONTEST_ACCOUNT_ROLES_FRIENDLY_CALLED = {
    0: "",
    1: "(裁判)",
    2: "(管理员)",
}


# WeJudge比赛系统账户角色描述
class WEJUDGE_CONTEST_ACCOUNT_ROLES:

    CONTESTANT = 0
    REFEREE = 1

    @staticmethod
    def exists(role):
        if int(role) in WEJUDGE_CONTEST_ACCOUNT_ROLES.roles():
            return True
        else:
            return False

    @staticmethod
    def roles():
        cls = WEJUDGE_CONTEST_ACCOUNT_ROLES
        return (
            cls.CONTESTANT,
            cls.REFEREE
        )

    @staticmethod
    def call(role):
        return WEJUDGE_CONTEST_ACCOUNT_ROLES_CALLED.get(role, "")

    @staticmethod
    def call_friendly(role):
        return WEJUDGE_CONTEST_ACCOUNT_ROLES_FRIENDLY_CALLED.get(role, "")


# WeJudge编译语言描述
class WEJUDGE_PROGRAM_LANGUAGE_SUPPORT:

    GCC = 1
    GCC_CPP = 2
    JAVA = 4
    PYTHON2 = 8
    PYTHON3 = 16

    @staticmethod
    def exists(lang):
        if int(lang) in WEJUDGE_PROGRAM_LANGUAGE_SUPPORT.langs():
            return True
        else:
            return False

    @staticmethod
    def langs():
        cls = WEJUDGE_PROGRAM_LANGUAGE_SUPPORT
        return (
            cls.GCC,
            cls.GCC_CPP,
            cls.JAVA,
            cls.PYTHON2,
            cls.PYTHON3
        )


# 分页按钮默认数量
WEJUDGE_PAGINATION_BTN_COUNT = 11
# 题目集分页显示题目的单页数量
WEJUDGE_PROBLEMSET_LIST_VIEWLIMIT = 50

WEJUDGE_ACCOUNT_MODEL_NAME = {
    'education': 'apps.educations.models.EduAccount',
    'master': 'apps.account.models.Account',
}

# 题目类型：正常模式
WEJUDGE_JUDGE_TYPE_NORMAL = 0
# 题目类型：填空模式
WEJUDGE_JUDGE_TYPE_FILL = 1
# 特殊评测：禁用
WEJUDGE_SPECIAL_JUDGE_DISABLED = 0
# 特殊评测：检查模式
WEJUDGE_SPECIAL_JUDGE_CHECKER = 1
# 特殊评测：交互模式
WEJUDGE_SPECIAL_JUDGE_INTERACTIVE = 2

# WeJudge存储路径
class WEJUDGE_STORAGE_ROOT:

    PROBLEMS_DATA = '/data/problems'                    # 题目配置数据存放点 （nfs挂载为r）

    TEMP_DIR = '/data/temp'                             # 程序运行输出数据临时存放点 (nfs不挂载)

    JUDGE_RESULT = '/data/judge_result'                 # 判题输出结果存放点，定期清理 (nfs挂载为rw)

    CODE_SUBMIT = '/data/code_submit'                   # 用户上传代码数据存放点 （nfs挂载为r）

    REPOSITORY_ROOT_DIR = '/data/resource/repositories'            # 课程资料库数据存放点 （nfs不挂载）

    CKEDITOR_UPLOAD_IMAGE_DIR = '/data/resource/imgupload'         # CkEditor上传照片数据存放点 （nfs不挂载）

    CKEDITOR_UPLOAD_FILE_DIR = '/data/resource/fileupload'         # CkEditor上传文件数据存放点 （nfs不挂载）

    EXPORT_TEMP_DIR = '/data/resource/export_temp'                 # 数据导出临时存放点 （nfs不挂载）

    IMPORT_TEMP_DIR = '/data/resource/import_temp'                 # 数据导入临时存放点 （nfs不挂载）

    PUBLIC_DOWNLOAD_DIR = '/data/resource/download'                # 公共资源存放点 （nfs不挂载）

    USER_HEADIMAGE_DIR = '/data/resource/headimg'                  # 用户头像位置（nfs不挂载）

    PROBLEMSET_THUMBS_DIR = '/data/resource/problemset_thumbs'     # 题目集的封面存储

    EDUCATION_ASGN_ATTACHMENT = '/data/resource/asgns_attachments'  # 作业附件存储

    CONTEST_STORAGE = '/data/contest'                              # 比赛数据存储

    EDUCATION_STORAGE = '/data/education'                          # 教学系统数据存储

    ROOT_DATA = '/data'


# 评测结果代号枚举
class WEJUDGE_JUDGE_EXITCODE:

    AC = 0          # 0 Accepted
    PE = 1          # 1 Presentation Error
    TLE = 2         # 2 Time Limit Exceeded
    MLE = 3         # 3 Memory Limit Exceeded
    WA = 4          # 4 Wrong Answer
    RE = 5          # 5 Runtime Error
    OLE = 6         # 6 Output Limit Exceeded
    CE = 7          # 7 Compile Error
    SE = 8          # 8 System Error
    RJ = 9          # 9 Rejudge
    SPJERR1 = 10    # 10 Special Judger Time OUT
    SPJERR2 = 11    # 11 Special Judger ERROR
    SPJFIN = 12     # 12 Special Judger Finish Need Standard Checkup


# 特殊评测退出状态枚举
class WEJUDGE_SPECIAL_JUDGE_EXITCODE:

    CHECKER_AC = 0
    CHECKER_PE = 1
    CHECKER_WA = 4
    CHECKER_OLE = 6
    CHECK_CONVERTED = 15

# 评测状态描述文档
WEJUDGE_JUDGE_STATUS_DESC = {
    -2: {
        'title': '队列中',
        'en': 'Pending',
        'color': ''
    },
    -1: {
        'title': '评测中',
        'en': 'Judging',
        'color': ''
    },
    0: {
        'title': '完全通过(AC)',
        'en': 'Accepted',
        'color': 'green',
        'abbr': 'AC'
    },
    1: {
        'title': '格式错误(PE)',
        'en': 'Presentation Error',
        'color': 'yellow',
        'abbr': "PE"
    },
    2: {
        'title': '超过时间限制(TLE)',
        'en': 'Time Limit Exceeded',
        'color': 'red',
        'abbr': "TLE"
    },
    3: {
        'title': '超过内存限制(MLE)',
        'en': 'Memory Limit Exceeded',
        'color': 'red',
        'abbr': "MLE"
    },
    4: {
        'title': '答案错误(WA)',
        'en': 'Wrong Answer',
        'color': 'red',
        'abbr': "WA"
    },
    5: {
        'title': '运行时错误(RE)',
        'en': 'Runtime Error',
        'color': 'red',
        'abbr': "RE"
    },
    6: {
        'title': '输出内容超限(OLE)',
        'en': 'Output Limit Exceeded',
        'color': 'orange',
        'abbr': "OLE"
    },
    7: {
        'title': '编译失败(CE)',
        'en': 'Compile Error',
        'color': 'blue',
        'abbr': "CE"
    },
    8: {
        'title': '系统错误(SE)',
        'en': 'System Error',
        'color': 'brown',
        'abbr': "SE"
    },
    9: {
        'title': '等待重判',
        'en': 'Pending Rejudge',
        'color': '',
        'abbr': "RJ"
    },
    10: {
        'title': '特殊评测超时',
        'en': 'Special Judger Time OUT',
        'color': 'brown'
    },
    11: {
        'title': '特殊评测程序错误',
        'en': 'Special Judger ERROR',
        'color': 'brown'
    },
    12: {
        'title': '特殊评测完成',
        'en': 'Special Judger Finish',
        'color': 'yellow'
    },
    20: {
        'title': '等待人工评判',
        'en': 'Pending Manual Judge',
        'color': ''
    }
}