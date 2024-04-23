import json
import create_checkout_session
import check_payer_by_email
import billing_session

def lambda_handler(event, context):
    # Check if the event has a 'body' key
    if 'body' in event:
        # Parse the JSON body
        body = json.loads(event['body'])
        
        # Check if the body has the key "call" and its value is "create-checkout-session"
        if body.get("call") == "create-checkout-session":
            # Call the specified function and return its result
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps(create_checkout_session.create_checkout_session(body))
            }
            
        if body.get("call") == "check-payer-by-email":
            # Call the specified function and return its result
            return check_payer_by_email.check_payer_by_email(body)
        


        if body.get("call") == "billing-session":
            # Call the specified function and return its result
            return billing_session.billing_session(body)

    # Default response for get requests from browser URL
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'text/html'},
        'body': '<h1>Atherton Lambda</h1>'
    }


