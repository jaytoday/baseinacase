
import logging
from google.appengine.api import urlfetch
from google.appengine.ext import db

from models import TopicEntity
from models import UserEntity


BASE_NAME = "yupgrade"


class NewUser():
  
  def __init__(self, user_name):
    self.user_name = user_name

  def create(self):
    self.add_user_to_freebase()
    this_user = self.save_user()
    return this_user
    
        
  def save_user(self):
       #create new user
       this_user = UserEntity(key_name = self.user_name,
                        name = self.user_name,
                        id = self.user_id)
       db.put(this_user)
       logging.info('saved user with name %s' % self.user_name)
       return this_user
       
  def add_user_to_freebase(self):
    query = [{
          "type": "/base/" + BASE_NAME + "/user",
          "name": self.user_name,
          "id": None,
          "handle" : self.user_name,
          "create": "unless_exists" 
          }]
    fb_session = freebase_session()
    freebase_object = fb_session.mqlwrite(query)[0]
    self.user_id = freebase_object['id']
    logging.info('added user to Freebase with name %s and id %s' % 
    (self.user_name, self.user_id) )
    


class NewTopicForUser():
  
  def __init__(self, user_name):
    self.user = UserEntity.get_by_key_name( user_name )
    

  def add_topic(self, topic_id, topic_name):
    self.save_topic_to_datastore(topic_id, topic_name)
    self.save_topic_to_freebase(topic_id)
    

  def save_topic_to_datastore(self, topic_id, topic_name):
    new_topic = TopicEntity(key_name = topic_id,
                            user = self.user,
                            id = topic_id )
    db.put(new_topic)
    logging.info('saved new topic %s for user %s' %
    ( topic_name, self.user.name ))

  def save_topic_to_freebase(self, topic_id):
    
    """
    
    Add a Topic to the List of Topics for this User
    
    
    """
    query = [{
        "type": "/base/" + BASE_NAME + "/user",
        "id": self.user.id,
        "topics": {
              "connect": "insert",
              "id":      topic_id
              }
            }]

    fb_session = freebase_session()
    freebase_object = fb_session.mqlwrite(query)[0]
    logging.info('"connect_status msg %s" returned updating topic %s to \
    Freebase for user %s' % 
    (freebase_object['topics']['connect'], freebase_object['topics']['id'],
    self.user.name))
    
    




def freebase_session():
  USERNAME = 'jamslevy'
  PASSWORD = 'buttbutt'
  from utils.utils import Debug
  from freebase import HTTPMetawebSession
  if Debug():
    # use sandbox for local testing
    session = HTTPMetawebSession('sandbox.freebase.com')    
  else:
    session = HTTPMetawebSession('freebase.com')
  session.login(USERNAME, PASSWORD)
  return session    
   