import requests

from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route

from core.models import Connection, Project, Customer

from .tasks import task_execute_store_order, task_execute_store_abandoned_cart

class ActiveCampaignViewSet(viewsets.ViewSet):


    def get_object(self, pk):
        try:
            return Project.objects.get(slug=pk)
        except Project.DoesNotExist:
            raise Http404

    def _check_header(request, project):
        if 'Auth ' + project.token != request.META.get('HTTP_PROJECTTOKEN', None):
            raise Http404

    # example /api/campaigns/{project}/orders/
    @detail_route(methods=["post"])
    def orders(self, request, pk):

        project = self.get_object(pk)

        task_execute_store_order(request.data, project)

        #self._check_header(request, project)

        return Response({'status' : 'Request queued'})


    @detail_route(methods=["post"])
    def abandoned_cart(self, request, pk):

        project = self.get_object(pk)

        task_execute_store_abandoned_cart(request.data, project)

        #self._check_header(request, project)

        return Response({'status' : 'Request queued'})
