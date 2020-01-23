from django.http import Http404
from core.models import Project
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from .tasks import task_execute_save_order, task_execute_save_cart, task_execute_subscribe_list, task_execute_remove_cart

class MailchimpViewSet(viewsets.ViewSet):

    def get_object(self, pk):
        try:
            return Project.objects.get(slug=pk)
        except Project.DoesNotExist:
            raise Http404

    @detail_route(methods=["post"])
    def order(self, request, pk):
        project = self.get_object(pk)

        task_execute_save_order(project, request.data)

        return Response({'status' : 'Request queued'})

    @detail_route(methods=["post"])
    def cart(self, request, pk):
        project = self.get_object(pk)

        task_execute_save_cart(project, request.data)

        return Response({'status' : 'Request queued'})

    @detail_route(methods=["delete"], url_name='cart', url_path='cart/(?P<cart_id>.+)')
    def delete_cart(self, request, pk, cart_id=None):
        project = self.get_object(pk)

        task_execute_remove_cart(project, cart_id)

        return Response({'status' : 'Request queued'})

    @detail_route(methods=["post"])
    def subscribe(self, request, pk):
        project = self.get_object(pk)

        task_execute_subscribe_list(project, request.data)

        return Response({'status' : 'Request queued'})
