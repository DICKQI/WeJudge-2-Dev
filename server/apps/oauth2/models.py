from django.db import models

# Create your models here.

ACCOUNT_TYPE = (
    ('wejudge', 'WeJudge Master Account'),
    ('education', "Education Account"),
    ('Contest', "Contest Account")
)


# 授权的APP客户
class Client(models.Model):

    # 客户账号
    username = models.CharField(max_length=50, null=True, blank=True)
    # 客户密码
    password = models.CharField(max_length=100, null=True, blank=True)
    # 商家简介
    description = models.CharField(max_length=100, null=True, blank=True)
    # 客户显示名称
    appname = models.CharField(max_length=20, null=True, blank=True)
    # 客户商标
    avatar = models.CharField(max_length=100, null=True, blank=True)
    # APP_ID
    app_id = models.CharField(max_length=100, unique=True)
    # APP密钥
    app_secret = models.CharField(max_length=100, null=True, blank=True)
    # AccessToken过期时间(s)
    at_expires_time = models.IntegerField(default=7200)             # 2小时
    # 刷新后AccessToken的过期时间的长度(s)
    # 使用RefreshToken后AccessToken的有效期将会以当前时间为准延后client.rf_rxpires_time个单位
    # 使用过后RefreshToken会自动更新
    # RefreshToken 和 AccessToken 时效相同
    rt_expires_time = models.IntegerField(default=604800)           # 7天
    # 授权回调地址
    redirect_uris = models.TextField(default='')
    # 授权取消后回调地址
    cancel_redirect_uri = models.TextField(default='')

    def __str__(self):
        return 'name=%s;app_id=%s' % (self.appname, self.app_id)


class OauthUser(models.Model):
    # APP
    client = models.ForeignKey('Client')
    # 所属子系统
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE, default='wejudge')
    # 所属用户
    account_id = models.IntegerField(default=0)
    # 是否允许该客户端进行访问
    is_allow = models.BooleanField(default=False)
    # OpenID    （SHA1(Client.appid + Account.user_id))
    open_id = models.CharField(max_length=100, blank=True, db_index=True)
    # AuthCode （一个Client一个用户只能存在唯一1个）
    auth_code = models.CharField(max_length=100, blank=True, null=True, unique=True)
    # AuthCode 过期时间
    auth_code_expires_at = models.IntegerField(default=0)
    # Tokens
    tokens = models.ManyToManyField("Tokens", blank=True)

    def __str__(self):
        return 'client=(%s);account=(%s at %s);is_allow=%s;open_id=%s' % (
            self.client, self.account_id, self.account_type, self.is_allow, self.open_id
        )


# 令牌存储
class Tokens(models.Model):
    # AccessToken
    access_token = models.CharField(max_length=100, unique=True)
    # RefreshToken
    refresh_token = models.CharField(max_length=100, unique=True)
    # AccessToken过期时间戳
    expires_at = models.IntegerField(default=0)

    def __str__(self):
        return 'access_token=(%s);expires_at=%s' % (self.access_token, self.expires_at)