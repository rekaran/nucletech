# Generated by Django 2.2.1 on 2019-06-12 17:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=50, verbose_name='Project Name')),
                ('project_id', models.CharField(max_length=50, unique=True, verbose_name='Project Id')),
                ('project_hash', models.CharField(max_length=129, unique=True, verbose_name='Project Hash')),
                ('project_key', models.TextField(verbose_name='Project Access Key')),
                ('bson_key', models.TextField(verbose_name='BSON Key')),
                ('builder_auth', models.BooleanField(default=True, verbose_name='Builder Authorization')),
                ('human_auth', models.BooleanField(default=False, verbose_name='Human Authorization')),
                ('analatics_auth', models.BooleanField(default=False, verbose_name='Analytics Authorization')),
                ('resource', models.TextField(blank=True, verbose_name='Resource List')),
                ('is_live', models.BooleanField(default=False, verbose_name='Live')),
                ('is_debug', models.BooleanField(default=True, verbose_name='Debug')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('language', models.TextField(verbose_name='Language')),
                ('timezone', models.TextField(verbose_name='Timezone')),
                ('wss', models.BooleanField(default=True, verbose_name='WSS')),
                ('retrain_date', models.DateTimeField(auto_now_add=True, verbose_name='Billing Date')),
                ('voice', models.BooleanField(default=True, verbose_name='Voice')),
                ('voice_out', models.CharField(blank=True, max_length=30, verbose_name='Voice Output')),
                ('human_takeover', models.BooleanField(default=False, verbose_name='Human Take Over')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('billing_amount', models.CharField(blank=True, max_length=30, verbose_name='Billing Amount')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectAuth',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('builder_view', models.BooleanField(default=False, verbose_name='Builder Authorization')),
                ('human_view', models.BooleanField(default=False, verbose_name='Human Authorization')),
                ('analytics_view', models.BooleanField(default=False, verbose_name='Analytics Authorization')),
                ('builder_edit', models.BooleanField(default=False, verbose_name='Buileder Edit Authorization')),
                ('human_chat', models.BooleanField(default=False, verbose_name='Human Chatting Authorization')),
                ('analytics_download', models.BooleanField(default=False, verbose_name='Analytics Download Authorization')),
                ('is_creator', models.BooleanField(default=False, verbose_name='Creator of Project')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='builder.Project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_key', models.TextField(blank=True, verbose_name='API Access Key')),
                ('is_company', models.BooleanField(default=False, verbose_name='Company')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ipaddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ipaddress', models.CharField(blank=True, max_length=30, verbose_name='Ipaddress')),
                ('user_agent', models.TextField(blank=True, verbose_name='User Agent')),
                ('browser', models.CharField(blank=True, max_length=200, verbose_name='Browser')),
                ('os', models.CharField(blank=True, max_length=200, verbose_name='Operating System')),
                ('platform', models.CharField(blank=True, max_length=200, verbose_name='Platform')),
                ('is_bot', models.BooleanField(default=False, verbose_name='Bot')),
                ('geo_location', models.TextField(blank=True, verbose_name='Geo Location')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ChangeLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='Date Added')),
                ('change', models.TextField(verbose_name='Changes Made')),
                ('ipaddress', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='builder.Ipaddress')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='builder.Project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BillingMode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_mode', models.TextField(blank=True, verbose_name='Mode of Payment')),
                ('detail', models.TextField(blank=True, verbose_name='Deatils of Payment Mode')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BillingHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.CharField(max_length=30, verbose_name='Type of Plan')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Billing Date')),
                ('url', models.TextField(verbose_name='PDF Url of the Bill')),
                ('mode', models.CharField(max_length=30, verbose_name='Mode of Billing')),
                ('project_list', models.TextField(verbose_name='List of Projects Billed')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Billing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan', models.CharField(blank=True, max_length=30, verbose_name='Type of Plan')),
                ('plan_amount', models.CharField(blank=True, max_length=30, verbose_name='Price of Plan')),
                ('payment_duration', models.CharField(blank=True, max_length=30, verbose_name='Plan Duration')),
                ('auto_renew', models.BooleanField(default=True, verbose_name='Auto Renew')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
