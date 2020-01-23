import requests
from urllib.parse import urlparse
from requests.auth import HTTPBasicAuth

def register_store(project):
    if not project.api_url:
        return False, 'You did not provide any API url'
    
    root = 'https://{}.api.mailchimp.com/3.0/'.format(urlparse(project.api_url).netloc.split('.')[0])
    endpoint = 'ecommerce/stores/'

    payload = {
        'id': project.token,
        'list_id': project.list.unique_id,
        'name': project.name,
        'currency_code': project.list.currency_code
    }

    if not project.pk:
        response = requests.post(root + endpoint, json=payload, auth=HTTPBasicAuth('', project.api_key))
    else:
        response = requests.patch(root + endpoint + str(project.token), json=payload, auth=HTTPBasicAuth('', project.api_key))    

    if response.ok:
        return True, ''
    return False, response.json()['detail']

def delete_store(project):
    root = 'https://{}.api.mailchimp.com/3.0/'.format(urlparse(project.api_url).netloc.split('.')[0])
    endpoint = 'ecommerce/stores/'

    response = requests.delete(root + endpoint + str(project.token), auth=HTTPBasicAuth('', project.api_key))

    if response.ok:
        return True, ''
    return False, response.json()['detail']