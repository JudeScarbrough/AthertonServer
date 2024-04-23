import stripe
import json





# Initialize Stripe and Firebase
stripe.api_key = 'sk_test_51P4q7Q03wq2Gsl4MTB58bOnclwVEEHDl8e54tUo6OnEoUhGwcvm13fEXSbAZd2wvVPZLHdu9X9W0qmS8KtD6cQmb00bfiDuw7J'



def create_checkout_session(body):
    user_email = body.get('email', '')
    user_id = body.get('user_id', '')
    appUrl = body.get('appUrl', '')

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

        session_url = checkout_session.url
        return {'statusCode': 200, 'session': checkout_session, 'url': session_url, 'email': user_email}
    except Exception as e:
        return str(e)
    

#print(create_checkout_session({'email': "jude.scarbrough@gmail.com", 'appUrl': "https://athertonmarketing.com"}))
