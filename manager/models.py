from django.db import models


# Create your models here.

class PluginManage(models.Model):

    plugin_num = models.CharField(max_length=50)
    plugin_belong_net = models.CharField(max_length=50)
    plugin_name = models.CharField(max_length=50)
    plugin_status = models.CharField(max_length=50)
    produce = models.CharField(max_length=50)


