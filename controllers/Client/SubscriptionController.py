import json
from flask import request, make_response, jsonify, g
from helpers.QueryHelper import QueryHelper
from helpers.SubscriptionHelper import SubscriptionHelper

from models.Subscription import Subscription
from models.SubscriptionIcon import SubscriptionIcon

from validator.StoreSubscription import validate_StoreSubscription
from validator.UpdateSubscription import validate_UpdateSubscription

from config import db


class SubscriptionController:
    def index():
        subscriptions = Subscription.query.order_by(
            Subscription.name.asc())
        data = request.args
        if data:
            data = {k: v for k, v in data.items() if v != ""}
            subscriptions = QueryHelper.checkQueryLimit(
                subscriptions, data)
            subscriptions = QueryHelper.checkQueryOffset(
                subscriptions, data)
        subscriptions = subscriptions.all()
        return jsonify([c.serialize for c in subscriptions])

    def show(id):
        subscription = Subscription.query.filter_by(
            id=id).first()
        if not subscription:
            return make_response({
                'message':
                'Nenhuma inscrição com este identificador está cadastrada.'
            }), 400
        return {
            **subscription.serialize,
            **{
                'icon': subscription.icon.serialize if subscription.icon else None
            }
        }

    def store():
        auth_user = g.current_user
        try:
            requestData = request.form.to_dict()
        except Exception as e:
            print(e)
           
            return make_response({'message': e}), 500
            
        print(requestData)
        subscription_data = json.loads(requestData['data'])
        if subscription_data:
            subscription_data = {k: v for k, v in subscription_data.items() if v != ""}

        errors = validate_StoreSubscription(subscription_data)
        if errors:
            return make_response(errors), 400

        try:
            subscription_data['client_id'] = auth_user.client.user_id
            subscription = Subscription(subscription_data)
            db.session.add(subscription)
            db.session.commit()
            db.session.refresh(subscription)
            icon = request.files.get('image')
            if icon:
                SubscriptionHelper.updateIcon(icon, subscription)
            print(subscription)
            return subscription.serialize
        except Exception as e:
            print(e)
            db.session.rollback()
            return make_response({'message': e}), 500

    def update(id):
        auth_user = g.current_user
        subscription = Subscription.query.filter_by(
            id=id).first()

        if not subscription or subscription.client_id != auth_user.client.user_id:
            return make_response({'message': 'Não autorizado.'}), 401

        requestData = request.form.to_dict()
        subscriptionData = json.loads(requestData['data'])
        if subscriptionData:
            subscriptionData = {
                k: None if v == "" else v
                for k, v in subscriptionData.items()
            }

        errors = validate_UpdateSubscription(subscriptionData)
        if errors:
            return make_response(errors), 400

        subscription = Subscription.query.filter_by(id=id)
        icon = request.files.get('image')
        try:
            subscription.update(dict(subscriptionData))
            db.session.commit()
            subscription = subscription.first()  #updated subscription
            if icon:
                SubscriptionHelper.updateIcon(icon, subscription)
        except Exception as e:
            print(e)
            db.session.rollback()
            return make_response({'message': e}), 500
        return subscription.serialize

    def destroy(id):
        subscription = Subscription.query.filter_by(
            id=id).first()
        if not subscription:
            return make_response({
                'message':
                'Nenhuma inscrição com este identificador está cadastrada.'
            }), 400

        iconOnly = request.args.get('iconOnly')
        try:
            icon = subscription.icon
            if not iconOnly:
                Subscription.query.filter_by(id=id).delete()
            if icon:
                SubscriptionHelper.removeIcon(icon)
                SubscriptionIcon.query.filter_by(
                    subscription_id=subscription.id).delete()
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return make_response({'message': e}), 500

        return make_response(), 200
