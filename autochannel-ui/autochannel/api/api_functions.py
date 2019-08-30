import os
import logging
import requests
from flask import Flask, session, request, url_for, render_template, redirect, \
 jsonify, flash, abort, Response
from flask import current_app as app
from requests_oauthlib import OAuth2Session
from itsdangerous import JSONWebSignatureSerializer
from autochannel.lib import discordData

"""
Channel types:
0 = text
1 = dm channel
2 = voice
3 = group DM
4 = category
5 = news
6 = store
"""

LOG = logging.getLogger(__name__)

def get_guild_categories(server_id):
    headers = {'Authorization': 'Bot '+app.config['AC_TOKEN']}
    r = requests.get(app.config['API_BASE_URL']+'/guilds/{}/channels'.format(server_id),
                     headers=headers)
    if r.status_code == 200:
        channels = r.json() 
        categories = list(filter(lambda c: c['type'] == 4, channels))
        categories = discordData.parsed_categories(categories)
        return categories
    
    return None

def get_guild_channels(server_id, voice=True, text=True):
    headers = {'Authorization': 'Bot '+app.config['AC_TOKEN']}
    r = requests.get(app.config['API_BASE_URL']+'/guilds/{}/channels'.format(server_id),
                     headers=headers)
    if r.status_code == 200:
        channels = r.json() 
        if not voice:
            channels = list(filter(lambda c: c['type'] != 2, channels))
        if not text:
            channels = list(filter(lambda c: c['type'] != 0, channels))
        return channels
    return None

def get_managed_guilds():
    LOG.info(session)
    token = session['oauth2_token']
    user = get_user(token)
    guilds = get_user_guilds(token)
    user_servers = sorted(
        get_user_managed_servers(user, guilds),
        key=lambda s: s['name'].lower()
    )
    guild_data = discordData.parse_managed_guilds(user_servers)
    #return jsonify(managedGuilds=user_servers)
    #return jsonify(managedGuilds=guild_data)
    return guild_data

def get_user(token):
    if 'user' in session:
        return session['user']

    discord = make_session(token=token)
    try:
        req = discord.get(app.config['API_BASE_URL'] + '/users/@me')
    except Exception:
        return None

    if req.status_code != 200:
        abort(req.status_code)

    user = req.json()
    # Saving that to the session for easy template access
    session['user'] = user
    return user

def get_user_guilds(token):
    # If it's an api_token, go fetch the discord_token
    if token.get('api_key'):
        user_id = token['user_id']
    else:
        user_id = get_user(token)['id']

    discord = make_session(token=token)

    req = discord.get(app.config['API_BASE_URL'] + '/users/@me/guilds')
    if req.status_code != 200:
        abort(req.status_code)

    guilds = req.json()
    return guilds

def get_user_managed_servers(user, guilds):
    return list(
        filter(
            lambda g: (g['owner'] is True) or
            bool((int(g['permissions']) >> 5) & 1),
            guilds)
    )

def make_session(token=None, state=None, scope=None):
    return OAuth2Session(
        client_id=app.config['OAUTH2_CLIENT_ID'],
        token=token,
        state=state,
        scope=scope,
        redirect_uri=app.config['OAUTH2_REDIRECT_URI'],
        auto_refresh_kwargs={
            'client_id': app.config['OAUTH2_CLIENT_ID'],
            'client_secret': app.config['OAUTH2_CLIENT_SECRET'],
        },
        auto_refresh_url=app.config['TOKEN_URL'],
        token_updater=token_updater)

def token_updater(token):
    session['oauth2_token'] = token