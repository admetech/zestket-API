# from django.test import TestCase
import json

# get snapshot testing
from snapshottest.django import TestCase

# get graphene test client
# from graphene.test import Client as Graph_client
from graphene_django.utils.testing import GraphQLTestCase

# get django test client
from django.test import Client as Api_client

# get schema
from server.schema import schema

# get models
from django.contrib.auth import get_user_model
from users.models import UserRole, User

class UsersTestCase(GraphQLTestCase, TestCase):

    GRAPHQL_URL = '/graph'

    access_token = None

    create_user_mutation = '''
        mutation createUser($input: CreateUserInput!) {
            createUser(input: $input){
                user{
                    id
                    employeeId
                    role{
                        id
                        title
                        identifier
                        hidden
                    }
                    phone
                    store{
                        id
                        branch
                        location
                    }
                    company{
                        id
                        name
                    }
                }
            }
        }
    '''

    user1 = {
        "employeeId" : "user1",
        "name" : "User1 Owner",
        "phone" : "7894561230",
        "role" : "VXNlclJvbGVOb2RlOjI=",
        "store" : "U3RvcmVOb2RlOjE="
    }

    user2 = {
        "employeeId" : "user2",
        "name" : "User2 Manager",
        "phone" : "7894561231",
        "role" : "VXNlclJvbGVOb2RlOjM=",
        "store" : "U3RvcmVOb2RlOjE="
    }
    
    user3 = {
        "employeeId" : "user3",
        "name" : "User3 Executive",
        "phone" : "7894561232",
        "role" : "VXNlclJvbGVOb2RlOjQ=",
        "store" : "U3RvcmVOb2RlOjE="
    }

    def setUpTestData():
        # doing one time setup before running test
        client = Api_client()
        # load the initial data
        executed = client.get('/v1/business/setup/defaults')

    def setUp(self):
        # execute for every test
        print('Setting Access Token')
        client = Api_client()
        executed = client.post('/v1/user/token/',{
            'username'      : 'skywalker',
            'password'      : '9886763307'
        })
        assert executed.status_code == 200
        self.user1_token = json.loads(executed.content.decode("utf-8"))
        # print('user token', self.user1_token['access'])

    def test_create_user(self):
        userlist = [self.user1, self.user2, self.user3]

        for user in userlist: 
            # execute the query
            response = self.query(self.create_user_mutation, op_name='createUser', input_data=user, headers={"HTTP_AUTHORIZATION": f"JWT {self.user1_token['access']}"})
            # This validates the status code and if you get errors
            self.assertResponseNoErrors(response)
            # Load content
            content = json.loads(response.content)
            # test Snap shot of content
            self.assertMatchSnapshot(content)
