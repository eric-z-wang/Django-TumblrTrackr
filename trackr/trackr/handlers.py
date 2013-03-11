from django.http import HttpResponse
from django.db.models import Max
import datetime, json
from django.core.exceptions import ObjectDoesNotExist
from trackr.models import *
import tracker


def add_blog(request):
	''' Add a new blog to our tracking list.''' 
	
	blog_name = request.REQUEST['blog'] # Using .REQUEST instead of .POST for testing
	if (not Blog.objects.filter(host_name = blog_name).exists()):
		b = Blog(host_name = blog_name)
		b.save()
	# We track a blog for the first time as soon as an add blog request
	# is made for that particular blog.
	tracker.request_likes(blog_name)
	
	return HttpResponse(content=blog_name, status=200)

def get_trends(request, blog_name=None):
	''' Send trend data for some specific tumblr blog ,
	or all blogs if blog_name=None.'''
	
	limit = request.GET.get('limit', 10)
	# Order must be specified.
	order = request.GET.get('order')
	if order == None:
		return HttpResponse(content="Order not specified.", status=404)	
	
	#Initialize a JSON object that will contain trends.
	result = {order.lower() : [], 
	        "order": order, 
	        "limit": limit}
	
	if order == "Trending":
		orderby = '-note_inc'
	elif order == "Recent":
		orderby = '-date'
	else:
		return HttpResponse(content=order + " is not a valid order.", status=404)	
	
	if blog_name:
		# Get liked posts for this specific blog.
		blog_obj = Blog.objects.get(host_name = blog_name)
		posts = blog_obj.likes.order_by(orderby)[0:limit]
	else:	
		# Get liked posts for all blogs.
		posts = Post.objects.all().order_by(orderby)[0:limit]
	
	# QuerySet of liked posts with sorted by either '-note_inc' or 'date',
	# depending on order parameter.
	for post in posts:
		p = {"url": post.url,
		     "image": post.image,
		     "text": post.text,
		     "date": '{:%Y-%m-%d %H:%M:%S %Z}'.format(post.date),
		     "last_track": '{:%Y-%m-%d %H:%M:%S} EST'.format(post.last_track),
		     "last_count": post.note_count,
		     "tracking": get_timestamps(post)}
		result[order.lower()].append(p)

	return HttpResponse(content=json.dumps(result), status=200)

def get_timestamps(post):
	'''Return a list of timestamp dicts.'''
	
	lst = []
	for t in Tracking.objects.filter(post = post.id):
		tdict = {"timestamp" : '{:%Y-%m-%d %H:%M:%S %Z}'.format(t.timestamp),
		         "sequence" : t.sequence,
		         "increment" : post.note_inc,
		         "count" : post.note_count}
		lst.append(tdict)
		
	# Return timestamps sorted by descending sequence number
	return sorted(lst, key=lambda k: k['sequence'], reverse=True) 
	
def ping(request):
	return HttpResponse(content="PING!", status=200);


