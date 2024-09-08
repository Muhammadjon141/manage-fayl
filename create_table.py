from database import ENGINE, Base
from models import User, Messages, PostTags, Tags, Followers, Likes, Comments, Post

Base.metadata.create_all(bind=ENGINE)