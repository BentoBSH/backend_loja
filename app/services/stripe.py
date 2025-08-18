#! /usr/bin/env python3.6
"""
Python 3.6 or newer required.
"""
from flask import Flask, Blueprint, request, jsonify
import json
import os
import stripe
from app.controllers.produto_controller import ProdutoController

# This is your test secret API key.
stripe.api_key = 'sk_test_51R7Or7P75gVISV00UIXZnTiO4jXcdIikbAiJVjjb2SrtoCmlJuKDgK68oD2ceOCAow6Cf8WDDuJIY9oF7J4cxyhY00ELaAtzBZ'

# Define o blueprint para rotas da API
stripeBlueprint = Blueprint("stripeBlueprint", __name__)


def calculate_order_amount(lista_IDs_quantidade):
  
    # cria duas listas: uma dos ids e outras das quantidades 
    lista_IDs = [p['id'] for p in lista_IDs_quantidade]
    lista_quantidades = [p['quantidade'] for p in lista_IDs_quantidade]

    # requere os produtos na base de dados com base na lista de IDs
    lista_produtos = ProdutoController.obter_por_lista(lista_IDs)

    # Cria a lista de preços dos produtos que vieram da base de dados  
    lista_precos = [p['preco'] for p in lista_produtos]

    # Obtem uma lista com o total por item
    total_por_item = [preco * quantidade for preco, quantidade in zip(lista_precos, lista_quantidades)]

    # obtem o total geral
    total_geral = sum(total_por_item)
    #print(total_por_item)

    return total_por_item


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
