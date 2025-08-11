#! /usr/bin/env python3.6
"""
Python 3.6 or newer required.
"""
from flask import Flask, Blueprint, request, jsonify, make_response, render_template
import json
import os
import stripe

# This is your test secret API key.
stripe.api_key = 'sk_test_51R7Or7P75gVISV00UIXZnTiO4jXcdIikbAiJVjjb2SrtoCmlJuKDgK68oD2ceOCAow6Cf8WDDuJIY9oF7J4cxyhY00ELaAtzBZ'

# Define o blueprint para rotas da API
stripeBlueprint = Blueprint("stripeBlueprint", __name__)


def calculate_order_amount(items):
    # Replace this constant with a calculation of the order's amount
    # Calculate the order total on the server to prevent
    # people from directly manipulating the amount on the client
    return 1400


@stripeBlueprint.route('/create-payment-intent', methods=['POST'])
def create_payment():
    try:
        data = json.loads(request.data)
        # Create a PaymentIntent with the order amount and currency
        intent = stripe.PaymentIntent.create(
            amount=calculate_order_amount(data['items']),
            currency='eur',
            # In the latest version of the API, specifying the `automatic_payment_methods` parameter is optional because Stripe enables its functionality by default.
            automatic_payment_methods={
                'enabled': True,
            },
        )
        return jsonify({
            'clientSecret': intent['client_secret']
        })
    except Exception as e:
        return jsonify(error=str(e)), 403
