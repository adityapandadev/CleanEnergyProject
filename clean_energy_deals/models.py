from django.db import models
from decimal import Decimal

# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=100)
    fmv = models.DecimalField(max_digits=10, decimal_places=2)


    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def __str__(self) -> str:
        return f"{self.name}({self.fmv})"

class Deal(models.Model):
    name = models.CharField(max_length=100, unique=True)
    projects = models.ManyToManyField(Project, through='ProjectDealThroughModel')

    class Meta:
        verbose_name = 'Deal'
        verbose_name_plural = 'Deals'

    def __str__(self) -> str:
        return f"{self.name}"

class ProjectDealThroughModel(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE)
    tax_credit_transfer_rate = models.DecimalField(max_digits=4, decimal_places=2)
    
    class Meta:
        verbose_name = 'Project and Deal'
        verbose_name_plural = 'Projects and Deals'

    def __str__(self) -> str:
        return f"{self.deal.name}-{self.project.name}-{self.tax_credit_transfer_rate}"