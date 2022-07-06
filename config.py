class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_ECHO = True

class ApplicationConfig:
    MAX_PAGE_LIMIT = 50
    ALLOWED_BOOK_SORTING_PARAMS = {'price', 'published_at', 'title'}
    ALLOWED_PUBLISHER_SORTING_PARAMS = {'title'}

