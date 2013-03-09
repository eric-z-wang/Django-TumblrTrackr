from django.http import HttpResponse
from django.db.models import Max
import datetime
from django.core.exceptions import ObjectDoesNotExist
from trackr.models import *
from models import *

''' Add a new blog to our tracking list.'''	
def add_blog(request):
	blog_name = request.REQUEST['blog'] # Using .REQUEST instead of .POST for testing
	if (Blog.objects.filter(host_name = blog_name).exists() != True):
		b = Blog(host_name = blog_name, timestamp = datetime.datetime.utcnow())
		b.save()
	return HttpResponse(blog_name)

''' Send trend data for some specific tumblr blog.'''
def get_blog_trends(request, blog_name):
	limit = request.GET['limit']
	order = request.GET['order']
	json = {"trending" : [], 
	        "order": order, 
	        "limit": limit} #Initializes a JSON object to track all posts liked by a blog
	if order == "Trending":
		try:
			blog_obj = Blog.objects.get(host_name = blog_name) #Gets a Blog object in database with blog_name as host_name
			blog_likes = blog_obj.likes.order_by('-note_inc')[0:limit] #QuerySet of liked posts with most note_count
			for post in blog_likes:
				trending = {"url": post.url,
				            "image": post.image,
				            "date": post.date,
				            "last_track": '{:%Y-%m-%d %H:%M:%S} EST'.format(post.last_track),
				            "last_count": post.note_count,
				            "tracking": []}
				json["trending"].append(trending)
		except ObjectDoesNotExist:
			return HttpResponse(404)
	elif order == "Recent":
		try:
			blog_obj = Blog.objects.get(host_name = blog_name) #Gets a Blog object in database with blog_name as host_name
			blog_likes = blog_obj.likes.order_by('-last_track')[0:limit] #QuerySet of liked posts with most recent tracking
			for post in blog_likes:
				trending = {"url": post.url,
				            "image": post.image,
				            "date": post.date,
				            "last_track": '{:%Y-%m-%d %H:%M:%S} EST'.format(post.last_track),
				            "last_count": post.note_count,
				            "tracking": []}
				json["trending"].append(trending)
		except ObjectDoesNotExist:
			return HttpResponse(404)
	return HttpResponse(200)
	
'''Send trends from all blogs that the user is subsribed to'''
def get_trends(request):
	''' Send trending data for all blogs.'''
	limit = request.GET.get('limit', 10)
	order = request.GET['order']
	if order == 'Trending':
		stuff = "Trending"
	elif order == "Recent":
		stuff = "Recent"
	else:
		return HttpResponse(200)
	# Fill this here in. With code.
	return HttpResponse(stuff)
	
def ping(request):
    return HttpResponse(200);


