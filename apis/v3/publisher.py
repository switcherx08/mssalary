from flask_restx import Namespace, Resource, fields, reqparse

from apis.v3 import resp_model, publisher_model
from config import ApplicationConfig
from models import Publisher as MPub, db

ns = Namespace('publisher')


publisher_response_model = ns.inherit('PublisherResponseModel', resp_model, {
    'publisher': fields.Nested(publisher_model, skip_none=True)
})
publisher_response_list_model = ns.inherit('PublisherResponseList', resp_model, {
    'publishers': fields.List(fields.Nested(publisher_model))
})

parser = reqparse.RequestParser()
parser.add_argument('title', required=True, type=str)

get_parser = reqparse.RequestParser()
get_parser.add_argument('title', required=False, type=str, location='args')
get_parser.add_argument('page', required=False, type=int, location='args', default=1)
get_parser.add_argument('by', required=False, type=str, location='args')
get_parser.add_argument('order', required=False, type=str, location='args')
get_parser.add_argument('limit', required=False, type=int, location='args', default=5)



@ns.route('/')
class PublisherList(Resource):
    @ns.marshal_with(publisher_response_list_model, skip_none=True)
    def get(self):
        # publishers = MPub.query.all()
        # return {'publishers': publishers}
        args = get_parser.parse_args()
        query = MPub.query

        if args.title:
            query = query.filter(MPub.title.like(f'%{args.title}%'))
        if args.by not in ApplicationConfig.ALLOWED_PUBLISHER_SORTING_PARAMS:
            args.by = 'title'
        sort_field = getattr(MPub, args.by)
        if args.order == 'desc':
            sort_field = sort_field.desc()  # ПОСМОТРЕТЬ
        else:
            sort_field = sort_field.asc()
        query = query.order_by(sort_field)

        def pagination(query, limit):
            query = query.limit(limit)
            query = query.offset(limit * (args.page - 1))
            return query

        limit = min(args.limit, ApplicationConfig.MAX_PAGE_LIMIT)

        query = pagination(query, limit)

        publishers = query.all()
        return {'publishers': publishers}



    @ns.marshal_with(publisher_response_model)
    def post(self):
        args = parser.parse_args()
        publisher = MPub(**args)
        db.session.add(publisher)
        db.session.commit()
        return {'publisher': publisher}


@ns.route('/<int:id>')
class Publisher(Resource):
    @ns.marshal_with(publisher_response_model, skip_none=True)  # НЕ СРАБАТЫВАЕТ SKIP_NONE , ПРОВЕРИТЬ.
    def get(self, id):
        publisher = MPub.query.get(id)
        if publisher is None:
            return {'msg': 'Could not found'}, 404
        return {'publisher': publisher}

    def put(self, id):
        pass

    @ns.marshal_with(publisher_response_model)
    def delete(self, id):
        publisher = MPub.query.get(id)
        if publisher is None:
            return {'message': f'There is no publisher with id {id}'}
        db.session.delete(publisher)
        db.session.commit()
        return {'publisher': publisher}


@ns.route('/<int:id>/books/')
class PublisherBooks(Resource):
    def get(self):
        pass
