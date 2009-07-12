from google.appengine.ext import db


class UserEntity(db.Model):
    name = db.StringProperty(required=True) 
    id = db.StringProperty(required=True)


class TopicEntity(db.Model):
    id = db.StringProperty(required=True)



