# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse

from twelb.frontend.lib.redis import Redis

import hashlib

def index(request):

    try:
        auth_hash = request.COOKIES['auth']
    except (KeyError):
        return render_to_response('frontend/login.html')

    r = Redis(db=0)
    r.set('uid:1:username', 'tim')
    r.set('uid:2:username', 'elbart')
    user_id = r.get('auth:%s' % auth_hash) or None

    if not user_id:
        return render_to_response('frontend/login.html')
            
    username = r.get('uid:%d:username' % user_id)
    return HttpResponse("Hello %s. Welcome to twelb (the twitter elbart app). <a href=\"/frontend/logout\">logout</a>" % username)

def login(request):
    #r = Redis(db=0)
    #r.set('username:elbart:id', 2)
    #r.set('username:tim:id', 1)
    #r.set('uid:1:password', 'timtest')
    #r.set('uid:2:password', 'elbarttest')
    #r.incr('global:nextPostId')
    #postId = r.get('global:nextPostId')
    return render_to_response('frontend/login.html', {'username': 'tim', 'password': 'test'})

def dologin(request):
    try:
	username, password = request.POST['username'], request.POST['password']
    except (KeyError):
	return render_to_response('frontend/login.html', {'username': 'tim', 'password': 'test', 'error_message': 'Input missing'})

    r = Redis(db=0)
    user_id = r.get('username:%s:id' % username) or None
    real_password = r.get('uid:%d:password' % user_id) or None
    if not user_id or real_password != password:
       return render_to_response('frontend/login.html', {'username': 'tim', 'password': 'test', 'error_message': 'Wrong credentials'})
    
    auth_hash = r.get('uid:%d:auth' % user_id) or None

    if not auth_hash:
        print "generating NEW HASH"
        auth_hash = hashlib.sha224().hexdigest()
        r.set('uid:%d:auth' % user_id, auth_hash)
        r.set('auth:%s' % auth_hash, user_id)
    
    print auth_hash
    response = HttpResponseRedirect(reverse('twelb.frontend.views.index')) 
    response.set_cookie('auth', auth_hash)
    return response

def logout(request):
    try:
        old_auth_hash = request.COOKIES['auth']
    except (KeyError):
        return render_to_response('frontend/login.html')

    r = Redis(db=0)
    user_id = r.get('auth:%s:id' % old_auth_hash)
    auth_hash = hashlib.sha224().hexdigest()
    r.set('uid:%s:auth' % user_id, auth_hash)
    r.set('auth:%s' % auth_hash, user_id)
    r.delete('auth:%s' % old_auth_hash)

    return render_to_response('frontend/login.html')
