"""
init - version info
"""
import logging
from flask import abort, redirect, request, session 
from functools import wraps

LOG = logging.getLogger(__name__)

def is_authenticated():
  #LOG.info(f'SESSION INFO: {session.get("oauth2_token")}')
  return session.get('oauth2_token')

def login_required(view):
  @wraps(view)
  def view_wrapper(*args, **kwargs):
    if is_authenticated():
      return view(*args, **kwargs)
    else:
      return redirect('/api/login')
  return view_wrapper