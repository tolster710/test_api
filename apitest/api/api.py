#api/api.py


from django.contrib.auth.models import User
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.resources import Resource, ModelResource, ALL, ALL_WITH_RELATIONS
import cPickle as pickle
from models import Entry
from redis import ConnectionPool, StrictRedis
from tastypie.serializers import Serializer

pool = ConnectionPool(max_connections=100, db=0, host='127.0.0.1', port=6379)


class UserResource(ModelResource):
	class Meta:
		queryset = User.objects.all()
		resource_name = 'user'
		excludes=['is_staff', 'is_superuser', 'password', 'date_joined', 'is_active', 'email']
		allowed_methods=['get']
		filtering = {'username' : ALL,}

class EntryResource(ModelResource):
	user = fields.ForeignKey(UserResource, 'user')
	class Meta:
		queryset = Entry.objects.all()
		resource_name = 'entry'
		authorization=Authorization()
		filtering = {
			'user': ALL_WITH_RELATIONS,
			'pub_date': ['exact', 'lt', 'lte', 'gte', 'gt'],
		}

class testResource(Resource):
	class Meta:
		resource_name = 'test'
		allowed_methods = 'post'
		default_format = "application/json"
		serializer = Serializer(formats=['json'])

	def obj_create(self, bundle, **kwargs):
		response = {
					'status': False,
					'data': None,
					'errors': None
					}
		return response


class RedisResource(Resource):

	class Meta:
		resource_name='redis'
		#fields = ['value']
		allowed_methods=['get']

	def detail_uri_kwargs(self, bundle_or_obj, **kwargs):
		kwargs = {}
		try:
			kwargs['rkey'] = bundle_or_obj.data
		except Exception as e:
			raise(e)
		if type(bundle_or_obj) == type(object):
			kwargs['pk'] = bundle_or_obj.key
		else:
			kwargs['pk'] = 't3'
		return kwargs

	def get_object_list(self, request):
		conn=self.get_connection()
		li=conn.keys('*')
		res=[]
		for i in li:
			res.append(self.obj_get(request, i))
		return res

	def obj_get_list(self, request=None, **kwargs):
		conn=self.get_connection()
		li=conn.keys('*')
		return 'obj_get_list'
		#return [self.obj_get()]

	def obj_get(self, request=None, key=None, **kwargs):
		something['id']= kwargs['pk']
		something=RedisObject({'key':key})
		something.value = 'something'
		something.k2 = 'not a key'
		return something

	def get_connection(self):
		"""It will return redis connection object from pool.
		Args:
			self (object): It is a object method. 
		"""
		return StrictRedis(connection_pool=pool)
	def _serialize(self, string):
		return pickle.dumps(string)


class RedisObject(object):
	def __init__(self, initial=None):
		self.__dict__['rdict'] = {}
		if initial:
			self.update(initial)
			#self.redis_sync()


	def __getattr__(self, name):
		return self._data.get(name, None)

	def __setattr__(self, name, value):
		self.__dict__['rdict'][name] = value

	def update(self,other):
		for k in other:
			self.__setattr__(k, other[k])

	def to_dict(self):
		return self.rdict

	def redis_sync(self):
		conn = self.get_connection()
		res=self.unserialize(conn.hget( self.__getattr__('key'), 'data'))
		self.update(res)

	def get_connection(self):
		"""It will return redis connection object from pool.
		Args:
			self (object): It is a object method. 
		"""
		return StrictRedis(connection_pool=pool)

	def unserialize(self, string):
		return pickle.loads(string)

		

