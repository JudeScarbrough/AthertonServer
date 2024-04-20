import stripe
from flask import Flask, jsonify, request
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, db
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)

appUrl = "application.athertonmarketing.com"

# Initialize Stripe and Firebase
stripe.api_key = 'sk_test_51P4q7Q03wq2Gsl4MTB58bOnclwVEEHDl8e54tUo6OnEoUhGwcvm13fEXSbAZd2wvVPZLHdu9X9W0qmS8KtD6cQmb00bfiDuw7J'
cred = credentials.Certificate('fb_key.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://atherton-marketing-default-rtdb.firebaseio.com/'
})

@app.route('/')
def hello():
    return '<h1>Halo Management</h1>'

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    data = request.get_json()
    user_email = data.get('email', '')
    user_id = data.get('user_id', '')
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            mode='subscription',
            line_items=[{
                'price': 'price_1P58jv03wq2Gsl4MgfnqWpQq',
                'quantity': 1,
            }],
            customer_email=user_email,
            success_url=f'https://{appUrl}',
            cancel_url=f'https://{appUrl}',
        )


        return jsonify({'sessionId': checkout_session['id'], 'url': checkout_session.url})
    except Exception as e:
        logging.error(f'Error creating checkout session: {str(e)}')
        return jsonify(error=str(e)), 403


from flask import Flask, request, jsonify
import stripe
from firebase_admin import db
import logging



@app.route('/check-payer-by-email', methods=['GET'])
def check_payer_by_email():
    email = request.args.get('email', '')
    user_id = request.args.get('user_id', '')
    if not email:
        return jsonify({'error': 'Email is required'}), 400

    try:
        # Search for customers in Stripe by email
        customers = stripe.Customer.list(email=email)
        
        # Check if any customer exists with that email
        if not customers.data:
            return jsonify({'message': 'No customer found with this email', 'is_paying': False})

        # Loop through found customers to check for active subscriptions
        for customer in customers.data:
            # Set the Stripe customer ID in the database
            stripe_ref = db.reference(f'/users/{user_id}/stripe_id')
            stripe_ref.set(customer.id)

            subscriptions = stripe.Subscription.list(customer=customer.id, status='active')
            if subscriptions.data:
                # If any active subscriptions are found, update the payment status and return True
                ref = db.reference(f'/users/{user_id}/paid')
                ref.set("Yes")
                return jsonify({'message': 'Customer is a paying subscriber', 'is_paying': True, 'stripe_id': customer.id})

        # If no active subscriptions found for any customers
        return jsonify({'message': 'Customer exists but has no active subscriptions', 'is_paying': False})
    except Exception as e:
        logging.error(f'Error retrieving customer information: {str(e)}')
        return jsonify({'error': str(e)}), 404


@app.route('/create-customer-portal-session', methods=['POST'])
def create_customer_portal_session():
    try:
        data = request.get_json()
        user_id = data.get('user_id', '')

        # Retrieve Stripe customer ID from your database
        ref = db.reference(f'/users/{user_id}/stripe_id')
        stripe_customer_id = ref.get()

        if not stripe_customer_id:
            logging.error(f'Stripe customer ID not found for user {user_id}')
            return jsonify({'error': 'Stripe customer ID not found'}), 404

        # Create a session for the customer portal
        session = stripe.billing_portal.Session.create(
            customer=stripe_customer_id,
            return_url=f'https://{appUrl}/settings',
        )

        return jsonify({'url': session.url})
    except Exception as e:
        logging.error(f'Error creating customer portal session: {str(e)}')
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    context = ('/etc/letsencrypt/live/athertonmarketing.halomanagementserver.com/fullchain.pem',
               '/etc/letsencrypt/live/athertonmarketing.halomanagementserver.com/privkey.pem')
    app.run(host='0.0.0.0', port=443, ssl_context=context)


