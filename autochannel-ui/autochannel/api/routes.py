import os
import logging
import requests
from flask import Flask, session, request, url_for, render_template, redirect, \
 jsonify, flash, abort, Response, Blueprint
from flask import current_app as app
from flask_bootstrap import Bootstrap
from requests_oauthlib import OAuth2Session
from itsdangerous import JSONWebSignatureSerializer
"""
App imports
"""
from autochannel.lib.decorators import login_required
from autochannel.lib import discordData

"""
Api imports
"""
from autochannel.api import api_functions

LOG = logging.getLogger(__name__)

mod_api = Blueprint('mod_api', __name__)

@mod_api.route('/login')
def login():
    # scope = request.args.get(
    #     'scope',
    #     'identify email connections guilds guilds.join')
    scope = ['identify', 'email', 'guilds', 'connections', 'guilds.join']
    discord = api_functions.make_session(scope=scope)
    authorization_url, state = discord.authorization_url(
        app.config['AUTHORIZATION_BASE_URL'],
        # access_type="offline"
    )
    session['oauth2_state'] = state
    return redirect(authorization_url) 

@mod_api.route('/callback')
def callback():
    if request.values.get('error'):
        return request.values['error']
    discord = api_functions.make_session(state=session.get('oauth2_state'))
    discord_token = discord.fetch_token(
        app.config['TOKEN_URL'],
        client_secret=app.config['OAUTH2_CLIENT_SECRET'],
        authorization_response=request.url)
    if not discord_token:
        return redirect(url_for('ohno'))

    session['oauth2_token'] = discord_token

# Fetch the user
    user = api_functions.get_user(discord_token)
    # if not user:
    #     return redirect(url_for('logout'))
    # Generate api_key from user_id
    serializer = JSONWebSignatureSerializer(app.config['SECRET_KEY'])
    api_key = str(serializer.dumps({'user_id': user['id']}))
    # Store api_token in client session
    api_token = {
        'api_key': api_key,
        'user_id': user['id']
    }
    session.permanent = True
    session['api_token'] = api_token
    #return redirect(url_for('.me'))
    return redirect(url_for('mod_site.dashboard', user_id=session['api_token']['user_id']))