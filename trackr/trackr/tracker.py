from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
import datetime
import project_vars as pv
import requests
from models import Blog, Post

#################################
# Retrieving the likes for posts:
#################################

#### Process starts here ####
def track(request):
    ''' Used to manually start the tracking process for testing'''
    blog_name = request.REQUEST.get('blog', '')
    if blog_name:
        # Used for tracking a single blog_name for testing
        response = [_request_likes(blog_name)]
    else:
        # Used for starting the massive blog tracking batch job
        response = retrieve_all_likes()

    return HttpResponse(_response_list_to_str(response))


# Send AJAX request to tumblr.com to get da likes
def retrieve_all_likes():
    ''' Retrieve a list of liked posts:

    Method: GET api.tumblr.com/v2/blog/{base-hostname}/likes?api_key={key}
    Parameters:
        - api_key: The authentication key we get when we register an app with tumblr.
        - base-hostname: The name of the host we are tracking.
    Reponse: A JSON with:
        - like_posts: An array of post objects.
        - liked_count: Total number of liked posts.'''      

    response_list = []

    # For each blog in Blogs:
    for blog in Blog.objects.all():
        # Send AJAX request to tumblr.com to get da likes
        response = _request_likes(blog.host_name)        
        response_list.append(response)  
            
    return response_list

def _request_likes(blog_host_name):
    ''' Helper for retreiving likes from tumblr. 
        Given a base blog, makes the request.'''

    response = requests.get(_likes_request_str(blog_host_name))
    json=response.json()    
    ret = json['meta']['status']
    # Check for valid response

    if (ret)==200:
        # Response OK, so parse json for juicy goodness
        _parse_likes_json(blog_host_name, json)
        
    return (blog_host_name, ret)

def _parse_likes_json(blog_host_name, likes_json):
    ''' Parse the json reply from tumblr, call retrieve_post_details for each post, 
        and add all of the liked posts  to the blog_host_name's db entry.'''

    # Get the count
    # Necessary? Probably not, but here it is just in case.
    likes_count = likes_json['response']['liked_count']

    # Find the blog in the database, and start updating it:
    # Necessary? Only if we need to modify the blog here.
    try:
        blog_obj = Blog.objects.get(host_name=blog_host_name)
    except ObjectDoesNotExist:
        return (blog_host_name, 'Blog Does Not Exist')

    # For each post in the 'likes', extract its json object and handle it:
    for liked_post in likes_json['response']['liked_posts']:
        _parse_post_json(blog_host_name, liked_post)
    
    return

def _likes_request_str(blog_host_name):
    ''' Returns a string with the request for gettin' likes, baby. For example:
    http://api.tumblr.com/v2/blog/artgalleryofontario.tumblr.com/likes?api_key=
        UVsuuWUK99CX70DXIKylXXoCVo1QPvYzYPxKzN0GLTVxyd26bx'''
    return  pv.tumblr_url + 'blog/' + blog_host_name + \
            '/likes?api_key=' + pv.api_key 

#################################
# Some helpers for output stuffs
#################################       
def _response_to_str(response):
    ''' Takes a response tuple and formats it for english.'''
    return str(response[0]) + ' request got: ' + str(response[1]) + '\n'

def _response_list_to_str(response_list):
    ''' Takes a list of responses and returns a formatted english string.'''
    return ''.join([_response_to_str(response) for response in response_list])
    
                    
        
################################
# Retrieving details for posts
################################
def retrieve_post_details(post):
    ''' Retrieve details for some post.'''
    # Fill this here in. With code. 
    return

def _parse_post_json(blog_host_name, liked_post):
    ''' Takes the json from a post and extracts all its juicy goodness, then
        makes a database entry for it, if necessary.'''
    return

def _post_request_str(blog_host_name, post_id):
    ''' Returns a string with the request for gettin' a post.
        For example:
        http://api.tumblr.com/v2/blog/artgalleryofontario.tumblr.com/posts?api_key=
        UVsuuWUK99CX70DXIKylXXoCVo1QPvYzYPxKzN0GLTVxyd26bx&id=23'''
    return  pv.tumblr_url + 'blog/' + blog_host_name + \
            '/posts?api_key=' + pv.api_key + '&id=' + post_id

