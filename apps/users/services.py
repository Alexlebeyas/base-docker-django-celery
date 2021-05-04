import requests
import json
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

# MAILCHIMP CODE API
def get_subscribers():
    endpoint_url = settings.MAILCHIMP_API_ENDPOINT.format("lists/{}/members/".format(settings.MAILCHIMP_USER_LIST))
    result = requests.get(endpoint_url, headers={'Authorization': 'Basic '.join(settings.MAILCHIMP_API_KEY)})
    return result.json()


def add_subscribers(email):
    endpoint_url = settings.MAILCHIMP_API_ENDPOINT.format("lists/{}/members/".format(settings.MAILCHIMP_USER_LIST))

    if email:
        member_data = {
            "email_address": email,
            "email_type": "html",
            "status": "subscribed",
            "merge_fields": {},
            "interests": {},
            "language": "",
            "vip": False,
            "location": {"latitude": 0, "longitude": 0},
            "marketing_permissions": [],
            "ip_signup": "",
            "timestamp_signup": "",
            "ip_opt": "",
            "timestamp_opt": "",
            "tags": [],
        }

        data = json.dumps(member_data)
        result = requests.post(endpoint_url, auth=(settings.MAILCHIMP_USER, settings.MAILCHIMP_API_KEY),
                               data=data)

        results = result.json()
        if results.get('detail'):
            if results['detail'].find('Use PUT to insert') != -1:
                return _('You already subscribed to our newsletter')
            else:
                return results['detail']
        else:
            return _('You have been added to our newsletter')

    else:
        return False
