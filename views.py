import logging
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext import db

from utils.utils import Debug
from models import UserEntity



class Base(webapp.RequestHandler):

	def get(self):	
		template_values = {}
		self.response.out.write(template.render('templates/base.html', template_values))


class User(webapp.RequestHandler):

  def get(self):
    user = self.get_user()
    template_values = {'user': user, "debug":Debug()}
    self.response.out.write(template.render('templates/user.html', template_values))

# AND RESET CACHE USING TOUCH SERVICE

  def get_user(self):
    from methods import NewUser
    user_name = self.request.path.split('/')[-1]	
    this_user = UserEntity.get_by_key_name(user_name)
    if not this_user:
      new_user = NewUser(user_name)
      this_user = new_user.create()
    return this_user
	       
  # add topic for user 
  def post(self):
    from methods import NewTopicForUser
    new_topic = NewTopicForUser(self.request.get('user_name'))
    new_topic.add_topic(
    self.request.get('topic_id'),
    self.request.get('topic_name'))
    self.response.out.write("OK")
