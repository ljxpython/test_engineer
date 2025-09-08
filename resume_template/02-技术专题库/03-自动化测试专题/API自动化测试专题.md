# API自动化测试专题

## 专题概述
本专题涵盖RESTful API、GraphQL、WebSocket等接口自动化测试的核心技术和最佳实践，是高级测试开发工程师的重要技能领域。

**核心技能点**：
- RESTful API测试设计与实现
- API测试框架和工具使用
- 接口契约测试（Contract Testing）
- API性能和安全测试
- Mock服务设计与应用
- 微服务测试策略

---

## 题目列表

### ⭐⭐⭐ RESTful API测试的完整方法论
**难度**：⭐⭐⭐  
**频率**：🔥🔥🔥

**标准答案**：
**RESTful API测试层次**：
1. **功能测试**：验证API的业务逻辑正确性
2. **数据验证测试**：检查输入输出数据的准确性
3. **错误处理测试**：验证异常情况的处理机制
4. **安全测试**：认证授权、数据加密、输入验证
5. **性能测试**：响应时间、吞吐量、并发处理
6. **兼容性测试**：版本兼容、客户端兼容

**Python API测试实现**：
```python
import requests
import pytest
import json
from jsonschema import validate
import time

class APITestFramework:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.auth_token = None
    
    def authenticate(self, username, password):
        """用户认证"""
        auth_url = f"{self.base_url}/auth/login"
        payload = {"username": username, "password": password}
        
        response = self.session.post(auth_url, json=payload)
        assert response.status_code == 200
        
        self.auth_token = response.json().get("token")
        self.session.headers.update({"Authorization": f"Bearer {self.auth_token}"})
        return self
    
    def get(self, endpoint, params=None):
        """GET请求封装"""
        url = f"{self.base_url}{endpoint}"
        response = self.session.get(url, params=params)
        return APIResponse(response)
    
    def post(self, endpoint, data=None, json_data=None):
        """POST请求封装"""
        url = f"{self.base_url}{endpoint}"
        response = self.session.post(url, data=data, json=json_data)
        return APIResponse(response)
    
    def put(self, endpoint, data=None, json_data=None):
        """PUT请求封装"""
        url = f"{self.base_url}{endpoint}"
        response = self.session.put(url, data=data, json=json_data)
        return APIResponse(response)
    
    def delete(self, endpoint):
        """DELETE请求封装"""
        url = f"{self.base_url}{endpoint}"
        response = self.session.delete(url)
        return APIResponse(response)

class APIResponse:
    def __init__(self, response):
        self.response = response
        self.status_code = response.status_code
        self.headers = response.headers
        self.text = response.text
        
        try:
            self.json_data = response.json()
        except ValueError:
            self.json_data = None
    
    def assert_status_code(self, expected_code):
        """断言状态码"""
        assert self.status_code == expected_code, \
            f"Expected {expected_code}, got {self.status_code}. Response: {self.text}"
        return self
    
    def assert_json_schema(self, schema):
        """断言JSON schema"""
        assert self.json_data is not None, "Response is not JSON"
        validate(instance=self.json_data, schema=schema)
        return self
    
    def assert_response_time(self, max_time_ms):
        """断言响应时间"""
        response_time = self.response.elapsed.total_seconds() * 1000
        assert response_time <= max_time_ms, \
            f"Response time {response_time}ms exceeds limit {max_time_ms}ms"
        return self
    
    def extract_value(self, json_path):
        """提取JSON值"""
        import jsonpath_ng
        jsonpath_expr = jsonpath_ng.parse(json_path)
        matches = jsonpath_expr.find(self.json_data)
        return matches[0].value if matches else None

# 测试用例示例
class TestUserAPI:
    @classmethod
    def setup_class(cls):
        cls.api = APITestFramework("https://api.example.com")
        cls.api.authenticate("admin", "password123")
        
        # JSON Schema定义
        cls.user_schema = {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
                "email": {"type": "string", "format": "email"},
                "status": {"type": "string", "enum": ["active", "inactive"]}
            },
            "required": ["id", "name", "email", "status"]
        }
    
    def test_get_user_list(self):
        """测试获取用户列表"""
        response = self.api.get("/users", params={"page": 1, "size": 10})
        
        (response
         .assert_status_code(200)
         .assert_response_time(2000)
         .assert_json_schema({
             "type": "object",
             "properties": {
                 "users": {
                     "type": "array",
                     "items": self.user_schema
                 },
                 "total": {"type": "integer"},
                 "page": {"type": "integer"}
             }
         }))
    
    def test_create_user(self):
        """测试创建用户"""
        new_user = {
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123"
        }
        
        response = self.api.post("/users", json_data=new_user)
        
        (response
         .assert_status_code(201)
         .assert_json_schema(self.user_schema))
        
        # 提取创建的用户ID用于后续测试
        user_id = response.extract_value("$.id")
        assert user_id is not None
        
        return user_id
    
    def test_user_data_validation(self):
        """测试数据验证"""
        invalid_users = [
            {"name": "", "email": "invalid-email"},  # 无效邮箱
            {"email": "test@example.com"},           # 缺少必填字段
            {"name": "a" * 256, "email": "test@example.com"}  # 字段长度超限
        ]
        
        for invalid_user in invalid_users:
            response = self.api.post("/users", json_data=invalid_user)
            response.assert_status_code(400)
```

**API测试数据管理**：
```python
import yaml
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class TestData:
    """测试数据类"""
    valid_users: list
    invalid_users: list
    api_endpoints: dict
    
    @classmethod
    def load_from_yaml(cls, file_path):
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
        return cls(**data)

# test_data.yaml
"""
valid_users:
  - name: "John Doe"
    email: "john@example.com"
    role: "user"
  - name: "Jane Admin"  
    email: "jane@example.com"
    role: "admin"

invalid_users:
  - name: ""
    email: "invalid"
    expected_error: "VALIDATION_ERROR"
  - name: null
    email: "test@example.com"
    expected_error: "MISSING_FIELD"

api_endpoints:
  users:
    list: "/api/v1/users"
    create: "/api/v1/users"
    update: "/api/v1/users/{id}"
    delete: "/api/v1/users/{id}"
"""

class DataDrivenAPITest:
    def setup_method(self):
        self.test_data = TestData.load_from_yaml('test_data.yaml')
        self.api = APITestFramework("https://api.example.com")
    
    @pytest.mark.parametrize("user_data", lambda: self.test_data.valid_users)
    def test_create_valid_users(self, user_data):
        """数据驱动的有效用户创建测试"""
        response = self.api.post(self.test_data.api_endpoints['users']['create'], 
                               json_data=user_data)
        response.assert_status_code(201)
    
    @pytest.mark.parametrize("invalid_user", lambda: self.test_data.invalid_users)
    def test_create_invalid_users(self, invalid_user):
        """数据驱动的无效用户创建测试"""
        response = self.api.post(self.test_data.api_endpoints['users']['create'],
                               json_data=invalid_user)
        response.assert_status_code(400)
        assert invalid_user['expected_error'] in response.json_data['error_code']
```

---

### ⭐⭐⭐ API契约测试（Contract Testing）实践
**难度**：⭐⭐⭐  
**频率**：🔥🔥

**标准答案**：
**契约测试原理**：
验证服务提供者和消费者之间的API契约，确保接口变更不会破坏系统集成。主要包括消费者驱动契约测试（CDC）和提供者契约验证。

**Pact契约测试实现**：
```python
# 消费者端契约定义
import pytest
from pact import Consumer, Provider, Like, Term, Format
import requests

# 定义消费者契约
pact = Consumer('UserService').has_pact_with(Provider('UserAPI'))

class TestUserServiceContract:
    def setup_method(self):
        pact.start()
    
    def teardown_method(self):
        pact.stop()
    
    def test_get_user_contract(self):
        """定义获取用户的契约"""
        # 期望的交互
        expected_interaction = {
            'description': 'A request for user data',
            'request': {
                'method': 'GET',
                'path': '/users/123',
                'headers': {
                    'Accept': 'application/json',
                    'Authorization': Term(
                        r'Bearer [A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+',
                        'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
                    )
                }
            },
            'response': {
                'status': 200,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': {
                    'id': Like(123),
                    'name': Like('John Doe'),
                    'email': Format().email,
                    'created_at': Format().iso8601_datetime,
                    'status': Term(r'active|inactive', 'active')
                }
            }
        }
        
        # 设置契约交互
        pact.given('User 123 exists').upon_receiving(
            expected_interaction['description']
        ).with_request(
            expected_interaction['request']['method'],
            expected_interaction['request']['path'],
            headers=expected_interaction['request']['headers']
        ).will_respond_with(
            expected_interaction['response']['status'],
            headers=expected_interaction['response']['headers'],
            body=expected_interaction['response']['body']
        )
        
        # 执行实际请求验证契约
        with pact:
            response = requests.get(
                f"{pact.uri}/users/123",
                headers={
                    'Accept': 'application/json',
                    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
                }
            )
            
            assert response.status_code == 200
            user_data = response.json()
            assert user_data['id'] == 123
            assert user_data['name'] == 'John Doe'
            assert '@' in user_data['email']
    
    def test_create_user_contract(self):
        """定义创建用户的契约"""
        new_user_request = {
            'name': Like('Jane Doe'),
            'email': Format().email,
            'role': Term(r'admin|user', 'user')
        }
        
        created_user_response = {
            'id': Like(456),
            'name': Like('Jane Doe'),
            'email': Format().email,
            'role': Like('user'),
            'created_at': Format().iso8601_datetime,
            'status': Like('active')
        }
        
        (pact
         .given('Valid user data provided')
         .upon_receiving('A request to create a user')
         .with_request('POST', '/users',
                      headers={'Content-Type': 'application/json'},
                      body=new_user_request)
         .will_respond_with(201, 
                          headers={'Content-Type': 'application/json'},
                          body=created_user_response))
        
        with pact:
            response = requests.post(
                f"{pact.uri}/users",
                headers={'Content-Type': 'application/json'},
                json={
                    'name': 'Jane Doe',
                    'email': 'jane@example.com',
                    'role': 'user'
                }
            )
            
            assert response.status_code == 201
            created_user = response.json()
            assert created_user['name'] == 'Jane Doe'
            assert created_user['status'] == 'active'

# 提供者端契约验证
from pact import Verifier

class TestUserAPIContractVerification:
    def test_verify_user_api_contract(self):
        """验证用户API是否满足契约"""
        verifier = Verifier(provider='UserAPI',
                          provider_base_url='http://localhost:8080')
        
        # 设置提供者状态
        verifier.set_state('User 123 exists', setup_user_123)
        verifier.set_state('Valid user data provided', setup_valid_environment)
        
        # 验证契约
        success, logs = verifier.verify_pacts('./pacts/userservice-userapi.json')
        
        assert success, f"Contract verification failed: {logs}"

def setup_user_123():
    """设置测试数据：用户123存在"""
    # 在测试数据库中创建用户123
    test_db.create_user({
        'id': 123,
        'name': 'John Doe',
        'email': 'john@example.com',
        'status': 'active'
    })

def setup_valid_environment():
    """设置有效的测试环境"""
    # 清理数据库，确保测试环境干净
    test_db.cleanup()
```

**OpenAPI规范驱动测试**：
```python
import openapi3
from jsonschema import validate
import yaml

class OpenAPIContractTest:
    def __init__(self, openapi_spec_path):
        with open(openapi_spec_path, 'r') as f:
            self.spec = openapi3.OpenAPI(yaml.safe_load(f))
        self.base_url = self.spec.servers[0].url
    
    def test_endpoint_against_spec(self, method, path, **kwargs):
        """根据OpenAPI规范测试端点"""
        # 获取路径规范
        path_spec = self.spec.paths.get(path)
        if not path_spec:
            pytest.fail(f"Path {path} not found in OpenAPI spec")
        
        operation_spec = getattr(path_spec, method.lower())
        if not operation_spec:
            pytest.fail(f"Method {method} not defined for path {path}")
        
        # 执行请求
        response = requests.request(method, f"{self.base_url}{path}", **kwargs)
        
        # 验证响应状态码
        assert str(response.status_code) in operation_spec.responses
        
        # 验证响应格式
        response_spec = operation_spec.responses[str(response.status_code)]
        if response_spec.content:
            content_type = response.headers.get('content-type', '').split(';')[0]
            if content_type in response_spec.content:
                schema = response_spec.content[content_type].schema
                if schema and response.text:
                    validate(instance=response.json(), schema=schema.model_dump())
        
        return response
    
    def test_all_endpoints(self):
        """测试所有端点的基本契约合规性"""
        for path, path_item in self.spec.paths.items():
            for method in ['get', 'post', 'put', 'delete', 'patch']:
                operation = getattr(path_item, method)
                if operation:
                    # 根据规范生成测试数据
                    test_data = self.generate_test_data(operation)
                    self.test_endpoint_against_spec(method.upper(), path, **test_data)
```

---

### ⭐⭐ Mock服务设计与测试隔离
**难度**：⭐⭐  
**频率**：🔥🔥🔥

**标准答案**：
**Mock服务的价值**：
1. **测试隔离**：隔离外部依赖，确保测试稳定性
2. **并行开发**：前后端独立开发，提高开发效率
3. **边界测试**：模拟各种异常场景和边界条件
4. **性能测试**：控制响应时间和数据量

**Mock服务实现方案**：
```python
# 使用responses库进行HTTP Mock
import responses
import requests
import json

class APIMockService:
    def __init__(self):
        self.mock_data = {
            'users': [
                {'id': 1, 'name': 'John Doe', 'email': 'john@example.com'},
                {'id': 2, 'name': 'Jane Smith', 'email': 'jane@example.com'}
            ],
            'products': [
                {'id': 101, 'name': 'Product A', 'price': 99.99},
                {'id': 102, 'name': 'Product B', 'price': 149.99}
            ]
        }
    
    @responses.activate
    def setup_user_api_mocks(self):
        """设置用户API的Mock响应"""
        # GET /users - 获取用户列表
        responses.add(
            responses.GET,
            'https://api.example.com/users',
            json={'users': self.mock_data['users'], 'total': 2},
            status=200
        )
        
        # POST /users - 创建用户
        def create_user_callback(request):
            user_data = json.loads(request.body)
            new_user = {
                'id': len(self.mock_data['users']) + 1,
                'name': user_data['name'],
                'email': user_data['email'],
                'created_at': '2023-01-01T00:00:00Z'
            }
            self.mock_data['users'].append(new_user)
            
            return (201, {}, json.dumps(new_user))
        
        responses.add_callback(
            responses.POST,
            'https://api.example.com/users',
            callback=create_user_callback
        )
        
        # GET /users/{id} - 获取特定用户
        def get_user_callback(request):
            user_id = int(request.url.split('/')[-1])
            user = next((u for u in self.mock_data['users'] if u['id'] == user_id), None)
            
            if user:
                return (200, {}, json.dumps(user))
            else:
                return (404, {}, json.dumps({'error': 'User not found'}))
        
        responses.add_callback(
            responses.GET,
            re.compile(r'https://api\.example\.com/users/\d+'),
            callback=get_user_callback
        )
        
        # 模拟网络延迟
        responses.add(
            responses.GET,
            'https://api.example.com/slow-endpoint',
            json={'message': 'This is slow'},
            status=200,
            adding_headers={'X-Response-Time': '5000ms'}
        )
        
        # 模拟服务器错误
        responses.add(
            responses.GET,
            'https://api.example.com/error-endpoint',
            json={'error': 'Internal Server Error'},
            status=500
        )
    
    def setup_dynamic_mocks(self):
        """设置动态Mock响应"""
        # 基于请求参数返回不同响应
        def dynamic_search_callback(request):
            query = request.params.get('q', '')
            results = [user for user in self.mock_data['users'] 
                      if query.lower() in user['name'].lower()]
            
            return (200, {}, json.dumps({'results': results, 'count': len(results)}))
        
        responses.add_callback(
            responses.GET,
            'https://api.example.com/search',
            callback=dynamic_search_callback
        )

# 使用WireMock进行高级Mock
import wiremock
from wiremock.constants import Config

class WireMockService:
    def __init__(self):
        Config.base_url = 'http://localhost:8080/__admin'
        self.server = wiremock
    
    def setup_advanced_mocks(self):
        """设置高级Mock场景"""
        
        # 1. 状态化Mock - 模拟有状态的API
        self.server.stubbing.stub_for(
            wiremock.get('/api/counter')
            .in_scenario('Counter')
            .when_scenario_state_is('Started')
            .will_return(wiremock.aResponse().with_status(200).with_body('{"count": 0}'))
            .will_set_state_to('FirstCall')
        )
        
        self.server.stubbing.stub_for(
            wiremock.get('/api/counter')
            .in_scenario('Counter') 
            .when_scenario_state_is('FirstCall')
            .will_return(wiremock.aResponse().with_status(200).with_body('{"count": 1}'))
            .will_set_state_to('SecondCall')
        )
        
        # 2. 条件Mock - 基于请求内容
        self.server.stubbing.stub_for(
            wiremock.post('/api/users')
            .with_request_body(wiremock.containing('admin'))
            .will_return(wiremock.aResponse().with_status(201).with_body('{"role": "admin"}'))
        )
        
        self.server.stubbing.stub_for(
            wiremock.post('/api/users')
            .with_request_body(wiremock.not_matching('.*admin.*'))
            .will_return(wiremock.aResponse().with_status(201).with_body('{"role": "user"}'))
        )
        
        # 3. 延迟和故障模拟
        self.server.stubbing.stub_for(
            wiremock.get('/api/slow')
            .will_return(
                wiremock.aResponse()
                .with_status(200)
                .with_fixed_delay(5000)  # 5秒延迟
                .with_body('{"message": "slow response"}')
            )
        )
        
        # 4. 请求验证
        self.server.stubbing.stub_for(
            wiremock.post('/api/orders')
            .with_header('Authorization', wiremock.matching('Bearer .*'))
            .with_request_body(wiremock.matching_json_path('$.amount', wiremock.greater_than(0)))
            .will_return(wiremock.aResponse().with_status(201))
        )
    
    def verify_interactions(self):
        """验证Mock交互"""
        # 验证特定请求是否被调用
        self.server.verification.verify_that(
            wiremock.get_requested_for('/api/users')
            .with_header('Accept', wiremock.containing('application/json'))
        )
        
        # 验证请求次数
        self.server.verification.verify_that(
            wiremock.post_requested_for('/api/orders'),
            wiremock.exactly(3)
        )

# 测试用例中使用Mock
class TestUserServiceWithMock:
    def setup_method(self):
        self.mock_service = APIMockService()
        self.api_client = APITestFramework('https://api.example.com')
    
    @responses.activate
    def test_get_users_with_mock(self):
        """使用Mock测试获取用户列表"""
        self.mock_service.setup_user_api_mocks()
        
        response = self.api_client.get('/users')
        
        response.assert_status_code(200)
        assert len(response.json_data['users']) == 2
        assert response.json_data['users'][0]['name'] == 'John Doe'
    
    @responses.activate  
    def test_error_handling_with_mock(self):
        """使用Mock测试错误处理"""
        self.mock_service.setup_user_api_mocks()
        
        response = self.api_client.get('/error-endpoint')
        
        response.assert_status_code(500)
        assert 'error' in response.json_data
```

---

### ⭐⭐⭐ GraphQL API测试策略
**难度**：⭐⭐⭐  
**频率**：🔥

**标准答案**：
**GraphQL测试特点**：
1. **查询灵活性**：客户端可以精确指定需要的数据
2. **类型系统**：强类型schema定义，便于验证
3. **单一端点**：所有操作通过同一个URL
4. **实时订阅**：支持subscription实时数据推送

**GraphQL测试框架**：
```python
import requests
import json
from graphql import build_schema, validate, parse

class GraphQLTestClient:
    def __init__(self, endpoint, schema_file=None):
        self.endpoint = endpoint
        self.session = requests.Session()
        
        if schema_file:
            with open(schema_file, 'r') as f:
                schema_sdl = f.read()
            self.schema = build_schema(schema_sdl)
    
    def execute_query(self, query, variables=None, operation_name=None):
        """执行GraphQL查询"""
        payload = {
            'query': query,
            'variables': variables or {},
            'operationName': operation_name
        }
        
        response = self.session.post(
            self.endpoint,
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        return GraphQLResponse(response)
    
    def validate_query(self, query):
        """验证查询语法"""
        if self.schema:
            document = parse(query)
            errors = validate(self.schema, document)
            return len(errors) == 0, errors
        return True, []

class GraphQLResponse:
    def __init__(self, response):
        self.response = response
        self.status_code = response.status_code
        self.json_data = response.json()
        
        self.data = self.json_data.get('data')
        self.errors = self.json_data.get('errors', [])
        self.extensions = self.json_data.get('extensions')
    
    def assert_no_errors(self):
        """断言没有GraphQL错误"""
        assert not self.errors, f"GraphQL errors: {self.errors}"
        return self
    
    def assert_data_exists(self, path):
        """断言指定路径的数据存在"""
        current = self.data
        for key in path.split('.'):
            assert current is not None and key in current, f"Path {path} not found"
            current = current[key]
        return self
    
    def get_data(self, path):
        """获取指定路径的数据"""
        current = self.data
        for key in path.split('.'):
            if current is None or key not in current:
                return None
            current = current[key]
        return current

# GraphQL测试用例
class TestGraphQLAPI:
    def setup_class(self):
        self.client = GraphQLTestClient(
            'https://api.example.com/graphql',
            'schema.graphql'
        )
    
    def test_user_query(self):
        """测试用户查询"""
        query = """
        query GetUser($userId: ID!) {
            user(id: $userId) {
                id
                name
                email
                posts {
                    id
                    title
                    content
                    createdAt
                }
            }
        }
        """
        
        variables = {"userId": "123"}
        
        # 验证查询语法
        is_valid, errors = self.client.validate_query(query)
        assert is_valid, f"Query validation failed: {errors}"
        
        # 执行查询
        response = self.client.execute_query(query, variables)
        
        # 验证响应
        (response
         .assert_no_errors()
         .assert_data_exists('user.id')
         .assert_data_exists('user.posts'))
        
        # 验证数据内容
        user_data = response.get_data('user')
        assert user_data['id'] == '123'
        assert len(user_data['posts']) >= 0
    
    def test_mutation(self):
        """测试GraphQL mutation"""
        mutation = """
        mutation CreatePost($input: CreatePostInput!) {
            createPost(input: $input) {
                id
                title
                content
                author {
                    id
                    name
                }
                createdAt
            }
        }
        """
        
        variables = {
            "input": {
                "title": "Test Post",
                "content": "This is a test post content",
                "authorId": "123"
            }
        }
        
        response = self.client.execute_query(mutation, variables)
        
        response.assert_no_errors()
        
        created_post = response.get_data('createPost')
        assert created_post['title'] == "Test Post"
        assert created_post['author']['id'] == "123"
        assert created_post['id'] is not None
    
    def test_subscription(self):
        """测试GraphQL subscription"""
        # Note: 实际的subscription测试需要WebSocket客户端
        subscription = """
        subscription OnPostCreated($userId: ID!) {
            postCreated(userId: $userId) {
                id
                title
                author {
                    id
                    name
                }
            }
        }
        """
        
        # 验证subscription语法
        is_valid, errors = self.client.validate_query(subscription)
        assert is_valid, f"Subscription validation failed: {errors}"
    
    def test_error_handling(self):
        """测试错误处理"""
        # 无效的查询
        invalid_query = """
        query {
            nonExistentField {
                id
            }
        }
        """
        
        response = self.client.execute_query(invalid_query)
        
        assert len(response.errors) > 0
        assert 'nonExistentField' in str(response.errors[0])
    
    def test_query_complexity(self):
        """测试查询复杂度"""
        complex_query = """
        query {
            users {
                id
                posts {
                    id
                    comments {
                        id
                        author {
                            id
                            posts {
                                id
                                comments {
                                    id
                                }
                            }
                        }
                    }
                }
            }
        }
        """
        
        response = self.client.execute_query(complex_query)
        
        # 可能被查询复杂度限制拒绝
        if response.errors:
            error_message = str(response.errors[0])
            assert 'complexity' in error_message.lower() or 'depth' in error_message.lower()
```

---

## 专题总结

API自动化测试是现代微服务架构下的核心测试技能，需要掌握：

1. **RESTful API测试**：全面的功能、数据、错误、安全、性能测试方法
2. **契约测试**：确保服务间接口的一致性和兼容性
3. **Mock服务**：实现测试隔离和并行开发
4. **GraphQL测试**：适应新兴API技术的测试策略
5. **工具使用**：熟练使用各种API测试工具和框架

**面试回答要点**：
- 展示对不同API技术的深入理解
- 强调测试策略的系统性和全面性
- 体现工程实践中的最佳实践应用
- 结合实际项目说明技术选型和解决方案