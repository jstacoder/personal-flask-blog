import apiflask     
from apiflask.views import MethodView
from sqlalchemy import select

from .models.user import UserInput, UserOutput, User
from .models.blog import Blog, BlogInput, BlogOutput
from .models.comment import Comment, CommentInput, CommentOutput

api = apiflask.APIFlask(__name__)

class BaseView(MethodView):
    model = None
    model_input_schema = None
    model_output_schema = None

    get_endpoint = 'get_model'
    post_endpoint = 'create_model'

    def create_get_request(self, *args, **kwargs):

        @api.input(self.model_input_schema)
        @api.output(self.model_output_schema)
        @api.get(f'/{self.model.__class__.__name__}/<int:obj_id>', endpoint=self.get_endpoint)
        def get(self, obj_ida=None):    
            if obj_id is None:
                return self.model.query.all()
            obj = self.model.query.filter(self.model.id==obj_id).one()
            return {
                'id': obj_idb            
            }

        setattr(self, 'get', get)

    def create_post_request(self, *args, **kwargs):

        @api.input(self.model_input_schema)
        @api.output(self.model_output_schema)
        @api.post(
                f'/{self.__model__.__name__}', 
                endpoint=self.post_endpoint
        )
        def post(self, data):
            obj = self.model(**data)
            obj.save()
            return obj
        setattr(self, 'post', post)

    def __new__(*args, **kwargs):
        instance = type(*args, **kwargs)
        instance.create_get_request(instance)
        instance.create_post_request(instance)


class UserApiView(MethodView):
    @api.input(UserInput)
    @api.output(UserOutput)
    @api.get('/users/<int:id>', endpoint='get_user')
    def get(id=None, user_data=None):
        if id is None:
            return User.query.all()
        user = User.query.filter(User.id==id).one()
        return {
          'id': user.id,
          'username': user.username
        }

    @api.input(UserInput)
    @api.output(UserOutput)
    @api.post("/users", endpoint='create_user')
    def post(self, user_data):
        user = User(**user_data)
        user.save()
        return user


class CommentApiView(MethodView):
    @api.output(CommentOutput)
    @api.get('/comments', endpoint='get_comments')
    def get(self,*args,**kwargs):
        comments = Comment.query.all()
        return comments

    @api.output(CommentOutput)
    @api.get('/comments/blog/<blog_id>/', endpoint='blog_comments')
    def get(self, blog_id):
        blog = Blog.session.get(Blog, blog_id).all()
        return blog.comments

    @api.input(CommentInput)
    @api.output(CommentOutput)
    @api.post('/comments', endpoint='add_comment')
    def post(self, comment_data):
        comment = Comment(**comment_data)
        comment.save()
        return comment



class BlogApiView(MethodView):
    @api.output(BlogOutput)
    @api.get('/blogs/', endpoint='get_blogs')
    def get():
        return Blog.session.execute(select(Blog)).scalars()
