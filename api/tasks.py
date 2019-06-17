import requests
from core.models import Connection, Project, Customer

from huey.contrib.djhuey import db_task


API_URL = '/api/3'

def _compose_url(project, action):
    return project.api_url + API_URL + action

def _get_connection_id(project):
    return Connection.objects.filter(project=project)[0].active_id


@db_task()
def task_execute_store_order(request_data, project):

    url = _compose_url(project, '/ecomOrders')

    connection_id = _get_connection_id(project)

    headers = {'Api-Token': project.api_key}

    # Try to see if user exists

    user_url = _compose_url(project, '/ecomCustomers')
    external_id = request_data.pop('userid')
    email = request_data['email']
    user_payload = {
            "ecomCustomer": {
            "connectionid": connection_id,
            "externalid": external_id,
            "email": email,
            "acceptsMarketing": request_data.pop('acceptsMarketing')
        }
    }
    response = requests.post(user_url, json=user_payload, headers=headers)

    customer_id = None
    customer, created = Customer.objects.get_or_create(
        project=project,
        email=email
    )
    customer.external_id = external_id
    try:
        # Try to see if user exists in AC
        customer_id = response.json()['ecomCustomer']['id']
        customer.active_id = customer_id
    except KeyError:
        # User already exists in the system, update external values
        pass
    customer.save()
    # Create order

    payload = {'ecomOrder' : None}
    payload['ecomOrder'] = request_data

    payload['ecomOrder']['connectionid'] = connection_id
    payload['ecomOrder']['customerid'] = customer.active_id

    response = requests.post(url, json=payload, headers=headers)
