from  flask import jsonify
from flask_restful import abort, Resource
from werkzeug.security import generate_password_hash

from . import db_session
from users import User
from reqparse_user import parser


def abort_if_users_not_found(user_id):
    session = db_session.create_session()
    users = session.query(User).get(user_id)
    if not users:
        abort(404, message=f'User {user_id} not found')


def set_password(password):
    return generate_password_hash(password)


class UserResource(Resource):
    def get(self, user_id):
        abort_if_users_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify(
            {'user': users.to_dict(only=('name', 'surname',
                                         'age', 'address',
                                         'email', 'position',
                                         'speciality',
                                         'hashed_password'))

             }
        )

    def delete(self, user_id):
        abort_if_users_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(User)
        session.commit()
        return jsonify({'success': 'OK'})


class UserListResource(Resource):
    def get(self):
        session = db_session.create_session()
        user = session.query(User).all()
        return jsonify(
            {'user': users.to_dict(only=('name', 'surname',
                                         'age', 'address',
                                         'email', 'position',
                                         'speciality',
                                         'hashed_password'))

             }
        )

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            title=args['title'],
            content=args['content'],
            user_id=args['user_id'],
            is_published=args['is_published'],
            is_private=args['is_private']
        )
        session.add(user)
        session.commit()
        return jsonify(
            {'user': users.to_dict(only=('name', 'surname',
                                         'age', 'address',
                                         'email', 'position',
                                         'speciality',
                                         'hashed_password'))

             }
        )