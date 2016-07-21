from django.db import models


class HardwareManagementConsole(models.Model):
    ip = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)




class ManagedSystem(models.Model):
    id = models.CharField(max_length=50,primary_key=True)
    name = models.CharField(max_length=50)
    machine_type = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    associated_hmc = models.CharField(max_length=50)


class LogicalPartition(models.Model):
    id = models.CharField(max_length=50,primary_key=True)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    uuid = models.CharField(max_length=50)
    associated_managed_system = models.CharField(max_length=50)
    maximum_memory = models.FloatField()
    desired_memory = models.FloatField()
    minimum_memory = models.FloatField()
    has_dedicated_processors = models.BooleanField()
    maximum_processors = models.FloatField()
    desired_processors = models.FloatField()
    minimum_processors = models.FloatField()
    maximum_processing_units = models.FloatField()
    desired_processing_units = models.FloatField()
    minimum_processing_units = models.FloatField()

class VirtualIOServer(models.Model):
    id = models.CharField(max_length=50,primary_key=True)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    uuid = models.CharField(max_length=50)
    associated_managed_system = models.CharField(max_length=50)
    maximum_memory = models.FloatField()
    desired_memory = models.FloatField()
    minimum_memory = models.FloatField()
    has_dedicated_processors = models.BooleanField()
    maximum_processors = models.FloatField()
    desired_processors = models.FloatField()
    minimum_processors = models.FloatField()
    maximum_processing_units = models.FloatField()
    desired_processing_units = models.FloatField()
    minimum_processing_units = models.FloatField()
