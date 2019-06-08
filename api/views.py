import requests

from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route

from core.models import Connection, Project, Customer


class ActiveCampaignViewSet(viewsets.ViewSet):

    API_URL = '/api/3'

    def _compose_url(self, project, action):
        return project.api_url + self.API_URL + action

    def _get_connection_id(self, request, project):
        return Connection.objects.filter(project=project)[0].active_id

    def get_object(self, pk):
        try:
            return Project.objects.get(slug=pk)
        except Project.DoesNotExist:
            raise Http404

    def _check_header(self, request, project):
        if 'Auth ' + project.token != request.META.get('HTTP_PROJECTTOKEN', None):
            raise Http404

    # example /api/campaigns/{project}/orders/
    @detail_route(methods=["post"])
    def orders(self, request, pk):

        project = self.get_object(pk)

        #self._check_header(request, project)

        url = self._compose_url(project, '/ecomOrders')

        connection_id = self._get_connection_id(request, project)

        headers = {'Api-Token': project.api_key}

        # Try to see if user exists

        user_url = self._compose_url(project, '/ecomCustomers')
        external_id = request.data.pop('userid')
        email = request.data['email']
        user_payload = {
              "ecomCustomer": {
                "connectionid": connection_id,
                "externalid": external_id,
                "email": email,
                "acceptsMarketing": request.data.pop('acceptsMarketing')
            }
        }
        response = requests.post(user_url, json=user_payload, headers=headers)

        try:
            customer_id = response.json()['ecomCustomer']['id']
            customer = Customer.objects.create(
                project=project,
                active_id=customer_id,
                external_id=external_id,
                email=email
            )
        except:
            customer = Customer.objects.get(
                email=email,
                project=project
            )

        # Create order

        payload = {'ecomOrder' : None}
        payload['ecomOrder'] = request.data

        payload['ecomOrder']['connectionid'] = connection_id
        payload['ecomOrder']['customerid'] = customer.active_id

        response = requests.post(url, json=payload, headers=headers)
        return Response(response)
