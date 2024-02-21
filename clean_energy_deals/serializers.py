from rest_framework import serializers
from django.db.models import Sum, F
from decimal import Decimal
from clean_energy_deals.models import Project, Deal, ProjectDealThroughModel

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class ProjectDealThroughWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectDealThroughModel
        fields = ['project','tax_credit_transfer_rate']

class ProjectDealThroughRetrieveSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()

    class Meta:
        model = ProjectDealThroughModel
        fields = ['project','tax_credit_transfer_rate']

class DealRetrieveSerializer(serializers.ModelSerializer):
    projects = serializers.SerializerMethodField()
    total_tax_credit_transfer_amount = serializers.SerializerMethodField()

    class Meta:
        model = Deal
        fields = '__all__'
    
    def get_projects(self, instance):
        return ProjectDealThroughRetrieveSerializer(instance.projectdealthroughmodel_set.all(), many=True).data
    
    def get_total_tax_credit_transfer_amount(self, instance):
        return ProjectDealThroughModel.objects.filter(deal=instance).\
                aggregate(total_tax_credit_transfer_amount=Sum(F('project__fmv')*Decimal(0.3)*F('tax_credit_transfer_rate')))['total_tax_credit_transfer_amount'] or 0

class DealCreateUpdateDeleteSerializer(serializers.ModelSerializer):
    projects = ProjectDealThroughWriteSerializer(many=True, write_only=True)

    class Meta:
        model = Deal
        fields = '__all__'

    def create(self, validated_data):
        projects_data = validated_data.pop('projects')
        deal = Deal.objects.create(**validated_data)
        for project_data in projects_data:
            print("project_data", project_data)
            ProjectDealThroughModel.objects.create(deal=deal, **project_data)
        return deal

    def update(self,instance,validated_data):
        instance.name = validated_data.pop('name', instance.name) 
        instance.save()
        instance.projectdealthroughmodel_set.all().delete()
        projects_data = validated_data.pop('projects')
        for project_data in projects_data:
            ProjectDealThroughModel.objects.create(deal=instance,**project_data)
        return instance

