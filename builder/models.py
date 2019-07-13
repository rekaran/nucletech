from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.db import models
from home.models import User

import hashlib
import string
import random

randomPool = string.ascii_uppercase + string.ascii_lowercase + string.digits


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    api_key = models.TextField(_('API Access Key'), blank=True)
    is_company = models.BooleanField(_('Company'), default=False)
    coupon = models.CharField(_('Coupon'), max_length=30, blank=True)


class Ipaddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ipaddress = models.CharField(_('Ipaddress'), max_length=30, blank=True)
    user_agent = models.TextField(_('User Agent'), blank=True)
    browser = models.CharField(_('Browser'), max_length=200, blank=True)
    os = models.CharField(_('Operating System'), max_length=200, blank=True)
    platform = models.CharField(_('Platform'), max_length=200, blank=True)
    is_bot = models.BooleanField(_('Bot'), default=False)
    geo_location = models.TextField(_('Geo Location'), blank=True)


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_name = models.CharField(_('Project Name'), max_length=50, blank=False)
    project_id = models.CharField(_('Project Id'), max_length=50, blank=False, unique=True) # Combination of ProjectName_userIdRandom10CharHex
    project_hash = models.CharField(_('Project Hash'), max_length=129, blank=False, unique=True) # Encrypted ProjectId
    project_key = models.TextField(_('Project Access Key'), blank=False) # key to encrypt and decrypt data in DM
    bson_key = models.TextField(_('BSON Key'), blank=True)
    builder_auth = models.BooleanField(_('Builder Authorization'), default=True) # Project level authorization
    human_auth = models.BooleanField(_('Human Authorization'), default=False)
    analatics_auth = models.BooleanField(_('Analytics Authorization'), default=False)
    resource = models.TextField(_('Resource List'), blank=True)
    is_live = models.BooleanField(_('Live'), default=False)
    is_debug = models.BooleanField(_('Debug'), default=True)
    is_cached = models.BooleanField(_('Cached'), default=True)
    is_active = models.BooleanField(_('Active'), default=True) # False if bot deleted by user.
    language = models.TextField(_('Language'), blank=False)
    timezone = models.TextField(_('Timezone'), blank=False)
    wss = models.BooleanField(_('WSS'), default=False)
    user_limit = models.IntegerField(_('User Limit'), default=1000)
    retrain_date = models.DateTimeField(_('Retrain Date'), auto_now_add=True)
    voice = models.BooleanField(_('Voice'), default=True)
    voice_out = models.CharField(_('Voice Output'), max_length=150, blank=True)
    human_takeover = models.BooleanField(_('Human Take Over'), default=False)
    date_created = models.DateTimeField(_('Date Created'), auto_now_add=True)
    billing_amount = models.CharField(_('Billing Amount'), max_length=30, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)


# Query this Model to retrive all projects related to a user
class ProjectAuth(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    builder_view = models.BooleanField(_('Builder Authorization'), default=False) # User level authorization
    human_view = models.BooleanField(_('Human Authorization'), default=False)
    analytics_view = models.BooleanField(_('Analytics Authorization'), default=False)
    builder_edit = models.BooleanField(_('Buileder Edit Authorization'), default=False)
    human_chat = models.BooleanField(_('Human Chatting Authorization'), default=False)
    analytics_download = models.BooleanField(_('Analytics Download Authorization'), default=False)
    is_creator = models.BooleanField(_('Creator of Project'), default=False)
    date_created = models.DateTimeField(_('Date Created'), auto_now_add=True)


class ChangeLog(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ipaddress = models.ForeignKey(Ipaddress, on_delete=models.CASCADE)
    date_added = models.DateTimeField(_('Date Added'), auto_now_add=True)
    change = models.TextField(_('Changes Made'), blank=False)


class Billing(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.CharField(_('Type of Plan'), max_length=30, blank=True)
    plan_amount = models.CharField(_('Price of Plan'), max_length=30, blank=True)
    payment_duration = models.CharField(_('Plan Duration'), max_length=30, blank=True)
    auto_renew = models.BooleanField(_('Auto Renew'), default=True)


class BillingMode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_mode = models.TextField(_('Mode of Payment'), blank=True)
    detail = models.TextField(_('Deatils of Payment Mode'), blank=True)


class BillingHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.CharField(_('Type of Plan'), max_length=30, blank=False)
    date = models.DateTimeField(_('Billing Date'), auto_now_add=True)
    url = models.TextField(_('PDF Url of the Bill'), blank=False)
    mode = models.CharField(_('Mode of Billing'), max_length=30, blank=False)
    project_list = models.TextField(_('List of Projects Billed'), blank=False)

def profileCreation(sender, **kwargs):
    u = kwargs["instance"]
    if kwargs["created"]:
        p = Profile()
        p.user = u
        suplimentKey = ''.join(random.choice(randomPool) for _ in range(32))
        email = "{}{}".format(u.email, suplimentKey)
        digest = hashlib.md5(email.encode()).digest()
        whirlpool = hashlib.new('whirlpool')
        whirlpool.update(digest)
        hashKey = whirlpool.hexdigest()
        p.api_key = hashKey
        p.save()

post_save.connect(profileCreation, sender=User)