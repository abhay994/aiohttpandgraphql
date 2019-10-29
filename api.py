from aiohttp import web
import json
from bson import json_util
import graphene
from graphene import relay
import model as UserModel
from graphene_mongo.fields import MongoengineConnectionField
from mongoengine import  connect
from graphene_mongo import MongoengineObjectType
import django_filters.fields as fieldss
async def mongo(request):
    connect('creaxt', host='127.0.0.1', port=27017)
    class Users(MongoengineObjectType):
            class Meta:
                model = UserModel.User
                # interfaces = (relay.Node,)

    class User(MongoengineObjectType):
            class Meta:
                model = UserModel.User
                interfaces = (relay.Node,)

    class Activity(MongoengineObjectType):
        class Meta:
            model = UserModel.activity
            # interfaces = (relay.Node,)

    class Query(graphene.ObjectType):
            # users = MongoengineConnectionField(User)

            users = graphene.List(Users,types=graphene.String(),ids=graphene.String())

            def resolve_users(self, info,types,ids):
                objects = UserModel.User.objects.filter(type=types,uid=ids)

                # objects = objects.filter(UserModel.activity.cid==ids)

                return objects



            singleuser = graphene.List(Users, ids=graphene.String())

            def resolve_singleuser(self, info, ids):
                objects = UserModel.User.objects.filter(uid=ids)
                return objects


            user = MongoengineConnectionField(User)
            activity = graphene.List(Activity)
            def resolve_activity(self, info):
                objects = UserModel.activity.objects.all()

                # objects = objects.filter(UserModel.activity.cid==ids)

                return objects




    schema = graphene.Schema(query=Query,types=[UserModel.User,UserModel.activity])
    query = request.query['query']
    # query = '''query
    # {
    #     users(first: 10,type:"guardian")
    #     {
    #
    #
    #           edges { node {  name } }
    #
    #     }
    # }'''
    res = query
    print(res)
    result = schema.execute(res)

    return web.Response(text=json.dumps(result.data),status=200)

app = web.Application()
app.router.add_get('/mongo',mongo)
web.run_app(app)