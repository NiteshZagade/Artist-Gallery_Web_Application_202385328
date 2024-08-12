from flask import Blueprint, request, jsonify
from .models import db, Payment
import stripe
from .config import Config

stripe.api_key = Config.STRIPE_SECRET_KEY

payment_bp = Blueprint('payment_bp', __name__)

@payment_bp.route('/create-payment-intent', methods=['POST'])
def create_payment_intent():
    data = request.get_json()
    try:
        intent = stripe.PaymentIntent.create(
            amount=data['amount'],  # amount in cents
            currency='gbp',
            payment_method_types=['card']
        )
        return jsonify({
            'clientSecret': intent['client_secret'],
            'payment_intent_id': intent['id']
        })
    except Exception as e:
        return jsonify(error=str(e)), 403

@payment_bp.route('/confirm-payment-intent', methods=['POST'])
def confirm_payment_intent():
    data = request.get_json()
    try:
        intent = stripe.PaymentIntent.confirm(
            data['payment_intent_id'],
            payment_method=data['payment_method_id']
        )
        return jsonify(intent)
    except stripe.error.CardError as e:
        return jsonify(error=str(e)), 403

@payment_bp.route('/confirm-payment', methods=['POST'])
def confirm_payment():
    data = request.get_json()
    try:        
        # Assuming payment is successful and creating a record in the database
        payment = Payment(            
            order_id=data['order_id'],
            amount=data['amount'],
            currency=data['currency'],
            status=data['status'],
            stripe_charge_id=data['payment_intent_id'],
            created_by=data['created_by']
        )
        db.session.add(payment)
        db.session.commit()
        
        return jsonify({'message': 'Payment successful'})
    except Exception as e:
        return jsonify({'message': 'Payment failed', 'error': str(e)}), 400

@payment_bp.route('/webhook', methods=['POST'])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('Stripe-Signature')
    endpoint_secret = 'your_webhook_secret'

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return jsonify({'error': 'Invalid payload'}), 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return jsonify({'error': 'Invalid signature'}), 400

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']  # contains a stripe.PaymentIntent
        print('Payment for {} succeeded'.format(payment_intent['amount']))
        # Fulfill the purchase, update your database, etc.

    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']  # contains a stripe.PaymentIntent
        print('Payment for {} failed'.format(payment_intent['amount']))

    return jsonify({'status': 'success'}), 200