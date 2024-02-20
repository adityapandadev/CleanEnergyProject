from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from clean_energy_deals.models import Project, Deal
from clean_energy_deals.serializers import ProjectSerializer, DealRetrieveSerializer, DealCreateUpdateDeleteSerializer



class ProjectView(APIView):

    def get_object(self,pk):
        try:
            return Project.objects.get(id=pk)
        except Project.DoesNotExist:
            return Response({"message":"Project Not Found"}, status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request):
        project = Project.objects.all().order_by('-id')
        serializer = ProjectSerializer(project,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_202_ACCEPTED)
    
    def delete(self, request, pk):
        project = self.get_object(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

# TODO: Check Status 202 and 204 relevancy

class DealsView(APIView):

    def get_object(self,pk):
        try:
            return Deal.objects.get(id=pk)
        except Deal.DoesNotExist:
            return Response({"message":"Deal Not Found"}, status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request):
        deals = Deal.objects.all().order_by('-id')
        serializer = DealRetrieveSerializer(deals,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = DealCreateUpdateDeleteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        deal = self.get_object(pk)
        serializer = DealCreateUpdateDeleteSerializer(deal, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_202_ACCEPTED)
    
    def delete(self, request, pk):
        deal = self.get_object(pk)
        deal.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    





