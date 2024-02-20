from django.contrib import admin
from clean_energy_deals.models import Project, Deal, ProjectDealThroughModel

# Register your models here.

admin.site.register(Project)
admin.site.register(Deal)
admin.site.register(ProjectDealThroughModel)




