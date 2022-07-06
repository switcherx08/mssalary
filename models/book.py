from config import ApplicationConfig
from models import db, Genre, UserBookState
from .book_genre import book_genres

import math


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(2048), nullable=False)
    publisher_id = db.Column(db.Integer, db.ForeignKey('publishers.id'), nullable=False)
    publisher = db.relationship('Publisher', back_populates='books', lazy='joined', innerjoin=True)
    published_at = db.Column(db.DateTime, nullable=True)
    price = db.Column(db.Integer, nullable=True)
    genres = db.relationship('Genre', secondary=book_genres, backref=db.backref('books', lazy='dynamic'))
    like_count = db.Column(db.Integer, nullable=False, default=0)
    user_state = db.relationship('UserBookState', backref=db.backref('book', lazy=True), uselist=False)

    @classmethod
    def find_all(cls, by, order, page, limit, user_id, **kwargs):
        query = cls.query  # .options(db.contains_eager(cls.genres))
        query = cls.apply_filters(query, **kwargs)
        query = query.options(db.selectinload(cls.genres))
        query = cls.join_state(query, user_id)

        if by not in ApplicationConfig.ALLOWED_BOOK_SORTING_PARAMS:
            by = 'published_at'

        sort_field = getattr(cls, by)
        if order == 'desc':
            sort_field = sort_field.desc()  # ПОСМОТРЕТЬ
        else:
            sort_field = sort_field.asc()
        query = query.order_by(sort_field)

        limit = min(limit, ApplicationConfig.MAX_PAGE_LIMIT)
        query = query.limit(limit)
        query = query.offset(limit * (page - 1))

        return query.all()

    @classmethod
    def count_pages(cls, limit, **kwargs):
        query = cls.query.with_entities(db.func.count(cls.id))
        query = cls.apply_filters(query, **kwargs)

        book_count = query.scalar()
        return math.ceil(book_count / limit)

    @classmethod
    def find(cls, id, user_id=None):
        # SELECT * FROM books AS b LEFT JOIN user_book_states AS ubs ON b.id = ubs.book_id AND ubs.user_id = :user_id WHERE b.id = :id
        query = cls.query.filter_by(id=id)
        query = cls.join_state(query, user_id)
        return query.first()

    @classmethod
    def join_state(cls, query, user_id):
        if user_id is None:
            return query.options(db.noload(cls.user_state))

        else:
            return query.options(
                db.joinedload(cls.user_state),
                db.with_loader_criteria(UserBookState, UserBookState.user_id == user_id)
            )

    @classmethod
    def apply_filters(cls, query, title, publisher_id, genres, **_):
        if title:
            query = query.filter(cls.title.like(f'%{title}%'))

        if publisher_id:
            query = query.filter_by(publisher_id=publisher_id)

        if len(genres) > 0:
            subq = cls.query.with_entities(cls.id).join(cls.genres).filter(Genre.id.in_(genres)).subquery()
            query = query.filter(cls.id.in_(subq))

        return query
