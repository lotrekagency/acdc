import requests
import json
import secrets
import hashlib
from urllib.parse import urlparse
from huey.contrib.djhuey import db_task
from requests.auth import HTTPBasicAuth
from core.models import Request, Customer

def create_product(project, data): 
    root = 'https://{}.api.mailchimp.com/3.0/'.format(urlparse(project.api_url).netloc.split('.')[0])
    endpoint = 'ecommerce/stores/{}/products/'.format(project.token)
    product_id = secrets.token_urlsafe(32)
    
    payload = {
        **data,
        'id': product_id,
        'variants': [{
            'id': 'default',
            'title': data['title'],
            'price': data['price']
        }]
    }
    response = requests.post(root + endpoint, json=payload, auth=HTTPBasicAuth('', project.api_key))
    
    return product_id

@db_task()
def task_execute_save_order(project, data):
    root = 'https://{}.api.mailchimp.com/3.0/'.format(urlparse(project.api_url).netloc.split('.')[0])
    endpoint = 'ecommerce/stores/{}/orders/'.format(project.token)

    requests.delete('{}{}{}'.format(root, endpoint, data['id']), auth=HTTPBasicAuth('', project.api_key))

    if not 'id' in data['customer']:
        data['customer']['id'] = data['customer']['email_address']

    Request.objects.create(
        email=data['customer']['email_address'],
        payload=json.dumps(data, indent=4, sort_keys=True),
        project=project,
        category=Request.NEWORDER
    )

    Customer.objects.get_or_create(
        project=project,
        email=data['customer']['email_address']
    )

    lines_reloaded = []
    for line in data['lines']:
        product_id = create_product(project, line['product'])
        lines_reloaded.append({
            **line,
            'id': secrets.token_urlsafe(32),
            'product_id': product_id,
            'product_variant_id': 'default'
        })
    data['lines'] = lines_reloaded

    response = requests.post(root + endpoint, json=data, auth=HTTPBasicAuth('', project.api_key))
    if not response.ok:
        print(response.json())

@db_task()
def task_execute_remove_cart(project, cart_id):
    root = 'https://{}.api.mailchimp.com/3.0/'.format(urlparse(project.api_url).netloc.split('.')[0])
    endpoint = 'ecommerce/stores/{}/carts/{}'.format(project.token, cart_id)

    requests.delete(root + endpoint, auth=HTTPBasicAuth('', project.api_key))

@db_task()
def task_execute_save_cart(project, data):
    root = 'https://{}.api.mailchimp.com/3.0/'.format(urlparse(project.api_url).netloc.split('.')[0])
    endpoint = 'ecommerce/stores/{}/carts/'.format(project.token)

    requests.delete('{}{}{}'.format(root, endpoint, data['id']), auth=HTTPBasicAuth('', project.api_key))

    if not 'id' in data['customer']:
        data['customer']['id'] = data['customer']['email_address']

    Request.objects.create(
        email=data['customer']['email_address'],
        payload=json.dumps(data, indent=4, sort_keys=True),
        project=project,
        category=Request.ABANDONEDCART
    )

    Customer.objects.get_or_create(
        project=project,
        email=data['customer']['email_address']
    )

    lines_reloaded = []
    for line in data['lines']:
        product_id = create_product(project, line['product'])
        lines_reloaded.append({
            **line,
            'id': secrets.token_urlsafe(32),
            'product_id': product_id,
            'product_variant_id': 'default'
        })
    data['lines'] = lines_reloaded

    response = requests.post(root + endpoint, json=data, auth=HTTPBasicAuth('', project.api_key))
    if not response.ok:
        print(response.json())

@db_task()
def task_execute_subscribe_list(project, data):
    root = 'https://{}.api.mailchimp.com/3.0/'.format(urlparse(project.api_url).netloc.split('.')[0])
    endpoint = 'lists/{}/members/'.format(project.list.unique_id)

    email_hash = hashlib.md5(data['email_address'].encode()).hexdigest()
    r = requests.delete('{}{}{}'.format(root, endpoint, email_hash), auth=HTTPBasicAuth('', project.api_key))

    Request.objects.create(
        email=data['email_address'],
        payload=json.dumps(data, indent=4, sort_keys=True),
        project=project,
        category=Request.SUBSCRIBENL
    )

    Customer.objects.get_or_create(
        project=project,
        email=data['email_address']
    )
    
    response = requests.post(root + endpoint, json=data, auth=HTTPBasicAuth('', project.api_key))
    if not response.ok:
        print(response.json())
