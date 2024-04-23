import stripe
import json
import firebase_admin
from firebase_admin import credentials, db
from firebase_admin import _apps as firebase_apps

stripe.api_key = 'sk_test_51P4q7Q03wq2Gsl4MTB58bOnclwVEEHDl8e54tUo6OnEoUhGwcvm13fEXSbAZd2wvVPZLHdu9X9W0qmS8KtD6cQmb00bfiDuw7J'

# Firebase initialization with checking
if not firebase_apps:
    cred = credentials.Certificate('fb_key.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://atherton-marketing-default-rtdb.firebaseio.com/'
    })

def set_cors_headers():
    return {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}


def billing_session(body):
    headers = set_cors_headers()
    try:

        user_id = body.get('user_id', '')
        appUrl = body.get('appUrl')
        
        # Retrieve Stripe customer ID from your database
        ref = db.reference(f'/users/{user_id}/stripe_id')
        stripe_customer_id = ref.get()

        if not stripe_customer_id:
            return {'error': 'Stripe customer ID not found'}

        # Create a session for the customer portal
        session = stripe.billing_portal.Session.create(
            customer=stripe_customer_id,
            return_url=f'https://{appUrl}/settings',
        )

        return {
            'statusCode': 200,
            'headers': headers,
            'body': {'url': session.url}
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }