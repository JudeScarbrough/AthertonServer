import json
import stripe
import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase Admin
cred = credentials.Certificate('fb_key.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://atherton-marketing-default-rtdb.firebaseio.com/'
})

stripe.api_key = 'sk_test_51P4q7Q03wq2Gsl4MTB58bOnclwVEEHDl8e54tUo6OnEoUhGwcvm13fEXSbAZd2wvVPZLHdu9X9W0qmS8KtD6cQmb00bfiDuw7J'

def lambda_handler(event, context):
    query_params = event['queryStringParameters']
    email = query_params.get('email', '')
    user_id = query_params.get('user_id', '')

    if not email:
        return {'statusCode': 400, 'body': json.dumps({'error': 'Email is required'})}

    try:
        customers = stripe.Customer.list(email=email)
        if not customers.data:
            return {'statusCode': 200, 'body': json.dumps({'message': 'No customer found with this email', 'is_paying': False})}

        for customer in customers.data:
            stripe_ref = db.reference(f'/users/{user_id}/stripe_id')
            stripe_ref.set(customer.id)

            subscriptions = stripe.Subscription.list(customer=customer.id, status='active')
            if subscriptions.data:
                ref = db.reference(f'/users/{user_id}/paid')
                ref.set("Yes")
                return {
                    'statusCode': 200,
                    'body': json.dumps({
                        'message': 'Customer is a paying subscriber',
                        'is_paying': True,
                        'stripe_id': customer.id
                    })
                }

        # If no active subscriptions found for any customers
        return {'statusCode': 200, 'body': json.dumps({'message': 'Customer exists but has no active subscriptions', 'is_paying': False})}
    except Exception as e:
        return {'statusCode': 404, 'body': json.dumps({'error': str(e)})}