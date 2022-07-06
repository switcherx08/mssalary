from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user_book_state import UserBookState
from .user import User
from .genre import Genre
from .book import Book
from .publisher import Publisher



