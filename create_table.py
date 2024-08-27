from database import ENGINE, Base
from models import User, Order, Product

Base.metadata.create_all(bind=ENGINE)