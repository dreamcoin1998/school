# Generated by Django 2.2.13 on 2020-10-05 19:12

from django.db import migrations, models
import utils.getImagePath


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=25, verbose_name='标题')),
                ('content', models.TextField(verbose_name='反馈内容')),
                ('status', models.PositiveIntegerField(choices=[(0, '待处理'), (1, '已完成')], verbose_name='状态')),
                ('user', models.CharField(max_length=255, null=True, verbose_name='点赞用户ID')),
                ('platform', models.CharField(max_length=10, null=True, verbose_name='平台')),
            ],
            options={
                'verbose_name': '用户反馈',
                'verbose_name_plural': '用户反馈',
            },
            bases=(models.Model, utils.getImagePath.GetImagePath),
        ),
    ]
