# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['UsersTestCase::test_create_user 1'] = {
    'data': {
        'createUser': {
            'user': {
                'company': {
                    'id': 'QnVzaW5lc3NEZXRhaWxOb2RlOjE=',
                    'name': 'aDMe'
                },
                'employeeId': 'user1',
                'id': 'VXNlck5vZGU6Mg==',
                'phone': '7894561230',
                'role': {
                    'hidden': True,
                    'id': 'VXNlclJvbGVOb2RlOjI=',
                    'identifier': 'OWNER',
                    'title': 'Owner'
                },
                'store': {
                    'branch': 'Admin Store',
                    'id': 'U3RvcmVOb2RlOjE=',
                    'location': None
                }
            }
        }
    }
}

snapshots['UsersTestCase::test_create_user 2'] = {
    'data': {
        'createUser': {
            'user': {
                'company': {
                    'id': 'QnVzaW5lc3NEZXRhaWxOb2RlOjE=',
                    'name': 'aDMe'
                },
                'employeeId': 'user2',
                'id': 'VXNlck5vZGU6Mw==',
                'phone': '7894561231',
                'role': {
                    'hidden': False,
                    'id': 'VXNlclJvbGVOb2RlOjM=',
                    'identifier': 'MANAGER',
                    'title': 'Manager'
                },
                'store': {
                    'branch': 'Admin Store',
                    'id': 'U3RvcmVOb2RlOjE=',
                    'location': None
                }
            }
        }
    }
}

snapshots['UsersTestCase::test_create_user 3'] = {
    'data': {
        'createUser': {
            'user': {
                'company': {
                    'id': 'QnVzaW5lc3NEZXRhaWxOb2RlOjE=',
                    'name': 'aDMe'
                },
                'employeeId': 'user3',
                'id': 'VXNlck5vZGU6NA==',
                'phone': '7894561232',
                'role': {
                    'hidden': False,
                    'id': 'VXNlclJvbGVOb2RlOjQ=',
                    'identifier': 'EXECUTIVE',
                    'title': 'Executive'
                },
                'store': {
                    'branch': 'Admin Store',
                    'id': 'U3RvcmVOb2RlOjE=',
                    'location': None
                }
            }
        }
    }
}
