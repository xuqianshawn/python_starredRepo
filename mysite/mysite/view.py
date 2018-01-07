from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from .models import Project
from django.core import serializers
import json
import urllib
import urllib2
from urlparse import urlparse

client_id='4dd383dc69b00b4eaf8f'
client_secret='fd4273228dac263b546653b468eeff4b0a47f22b'
github_resolve_url='https://github.com/login/oauth/access_token'
github_star_url='https://api.github.com/users/{}/starred'
github_user_url='https://api.github.com/user'
def index(request):
    return render(request,'login.html')

def handleCallback(request):
    code=request.GET.get('code')
    url = github_resolve_url # Set destination URL here
    post_fields = {'client_id': client_id,'client_secret':client_secret,'code':code,
                  'accept':'json' }     # Set POST fields here
    #get access token
    data = urllib.urlencode(post_fields)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    resp = response.read()
    access_token = (resp).split('&')[0].split('=')[1]

    #retrieve info by token
    url=github_user_url+"?access_token="+access_token
    response = urllib2.urlopen(url)
    resp = response.read()
    username=json.loads(resp)['login']

    #retrieve starred repo by username
    starlist=[]
    url=github_star_url.format(username)
    response = urllib2.urlopen(url)
    resp = response.read()

    starredrepos=json.loads(resp)
    for repo in starredrepos:
        project=Project()
        project.fullname=repo["full_name"]
        project.url=repo["html_url"]
        project.stargazers_count=repo["stargazers_count"]
        project.forks_count=repo["forks"]
        project.pushed_at=repo["pushed_at"]
        project.language=repo["language"]
        starlist.append(project)
    return render(request, 'RepoList.html', {'repo_list': starlist})
