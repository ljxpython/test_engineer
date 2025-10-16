# 京东测试开发面试 - 专业知识点整理

## 测试理论基础

### 1. 测试用例设计方法
```python
# 等价类划分示例
def equivalent_class_testing():
    """
    用户年龄输入测试：18-65岁为有效等价类
    """
    valid_classes = [
        (18, "最小有效年龄"),
        (30, "中间有效年龄"), 
        (65, "最大有效年龄")
    ]
    
    invalid_classes = [
        (0, "年龄过小"),
        (17, "略低于有效范围"),
        (66, "略高于有效范围"),
        (-1, "负数年龄"),
        ("abc", "非数字输入")
    ]
    
    return valid_classes, invalid_classes

# 边界值分析示例
def boundary_value_analysis():
    """
    密码长度测试：6-20个字符
    """
    boundaries = {
        'min_minus': 5,      # 最小值-1
        'min': 6,            # 最小值
        'min_plus': 7,       # 最小值+1
        'nominal': 13,       # 中间值
        'max_minus': 19,     # 最大值-1
        'max': 20,           # 最大值
        'max_plus': 21       # 最大值+1
    }
    return boundaries
```

### 2. 测试类型和策略

#### 功能测试
- **单元测试**：函数级别的测试，使用Pytest/JUnit
- **集成测试**：模块间接口测试，使用Postman/Swagger
- **系统测试**：端到端完整业务流程测试
- **回归测试**：版本更新后的重复测试

#### 非功能测试
- **性能测试**：负载、压力、并发、稳定性
- **安全测试**：OWASP Top 10、渗透测试
- **兼容性测试**：浏览器、设备、系统版本
- **可用性测试**：用户体验、易用性

### 3. 自动化测试框架设计

```python
# 京东自动化测试框架示例
class JDTestFramework:
    def __init__(self):
        self.test_cases = []
        self.test_data = {}
        self.test_results = {}
    
    def data_driven_testing(self, test_data_file):
        """数据驱动测试"""
        """
        优点：
        1. 测试数据与脚本分离
        2. 易于维护和扩展
        3. 支持多组数据测试
        """
        test_cases = self.load_test_data(test_data_file)
        results = []
        
        for case in test_cases:
            result = self.execute_test(case)
            results.append(result)
        
        return results
    
    def keyword_driven_testing(self, keywords_file):
        """关键字驱动测试"""
        """
        优点：
        1. 非程序员也能编写测试
        2. 高度可复用
        3. 业务逻辑清晰
        """
        keywords = self.load_keywords(keywords_file)
        
        for keyword in keywords:
            self.execute_keyword(keyword)
    
    def page_object_model(self):
        """页面对象模式"""
        """
        优点：
        1. 页面元素集中管理
        2. 测试代码可维护性高
        3. 页面变化时修改成本低
        """
        class LoginPage:
            def __init__(self, driver):
                self.driver = driver
                self.username_input = "id=username"
                self.password_input = "id=password"
                self.login_button = "id=login-btn"
            
            def login(self, username, password):
                self.driver.find_element(self.username_input).send_keys(username)
                self.driver.find_element(self.password_input).send_keys(password)
                self.driver.find_element(self.login_button).click()
```

## 性能测试专项

### 1. 性能指标定义
```python
class PerformanceMetrics:
    """京东性能测试关键指标"""
    
    def __init__(self):
        self.response_time_percentiles = {
            'p50': 0,    # 中位数响应时间
            'p90': 0,    # 90%分位响应时间
            'p95': 0,    # 95%分位响应时间
            'p99': 0     # 99%分位响应时间
        }
        
        self.throughput_metrics = {
            'tps': 0,           # 每秒事务数
            'qps': 0,           # 每秒查询数
            'peak_tps': 0,      # 峰值TPS
            'sustained_tps': 0  # 持续TPS
        }
        
        self.resource_utilization = {
            'cpu_usage': 0,     # CPU使用率
            'memory_usage': 0,  # 内存使用率
            'disk_io': 0,       # 磁盘IO
            'network_io': 0     # 网络IO
        }
```

### 2. 京东高并发测试策略

```python
class JDHighConcurrencyTest:
    """京东高并发测试方案"""
    
    def seckill_scenario_test(self):
        """秒杀场景测试"""
        test_strategy = {
            'concurrent_users': 100000,    # 10万并发用户
            'test_duration': 300,            # 5分钟测试时长
            'ramp_up_period': 60,            # 60秒逐步加压
            'peak_hold_time': 180,         # 180秒峰值保持
            
            'test_phases': [
                {
                    'phase': '预热阶段',
                    'duration': 60,
                    'users': 1000,
                    'actions': ['浏览商品', '查看详情']
                },
                {
                    'phase': '加压阶段', 
                    'duration': 60,
                    'users': 50000,
                    'actions': ['加入购物车', '获取库存']
                },
                {
                    'phase': '秒杀阶段',
                    'duration': 60,
                    'users': 100000,
                    'actions': ['秒杀下单', '支付确认']
                },
                {
                    'phase': '恢复阶段',
                    'duration': 120,
                    'users': 10000,
                    'actions': ['查询订单', '查看物流']
                }
            ],
            
            'success_criteria': {
                'response_time_p99': '< 3秒',
                'success_rate': '> 99.9%',
                'throughput': '> 50000 TPS',
                'no_overselling': True,  # 不允许超卖
                'inventory_accuracy': '100%'
            }
        }
        return test_strategy
    
    def flash_sale_test(self):
        """限时抢购测试"""
        return {
            'test_type': 'flash_sale',
            'key_challenges': [
                '瞬时高并发访问',
                '库存扣减准确性',
                '订单生成一致性',
                '支付流程稳定性',
                '系统资源利用率'
            ],
            'monitoring_metrics': [
                '实时QPS监控',
                '数据库连接池状态',
                'Redis缓存命中率',
                '消息队列积压情况',
                '应用服务器负载'
            ]
        }
```

## 安全测试要点

### 1. Web安全测试
```python
class JDSecurityTesting:
    """京东安全测试重点"""
    
    def sql_injection_test(self, input_fields):
        """SQL注入测试"""
        sql_payloads = [
            "' OR '1'='1",
            "' UNION SELECT * FROM users--",
            "'; DROP TABLE users;--",
            "' OR 1=1#",
            "' OR '1'='1' /*"
        ]
        
        vulnerable_fields = []
        for field in input_fields:
            for payload in sql_payloads:
                if self.test_sql_vulnerability(field, payload):
                    vulnerable_fields.append({
                        'field': field,
                        'payload': payload,
                        'severity': 'HIGH'
                    })
        
        return vulnerable_fields
    
    def xss_test(self, input_params):
        """XSS跨站脚本测试"""
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "javascript:alert('XSS')",
            "<svg onload=alert('XSS')>",
            "' onmouseover='alert(1)"
        ]
        
        return self.test_xss_vulnerabilities(input_params, xss_payloads)
    
    def csrf_test(self, sensitive_operations):
        """CSRF跨站请求伪造测试"""
        """
        京东支付、订单操作等需要重点测试CSRF防护
        """
        test_cases = [
            {
                'operation': 'modify_address',
                'csrf_token_required': True,
                'test_method': 'direct_request'
            },
            {
                'operation': 'payment',
                'csrf_token_required': True,
                'test_method': 'forged_request'
            }
        ]
        return test_cases
```

### 2. 业务安全测试
```python
def business_security_test():
    """业务逻辑安全测试"""
    test_scenarios = {
        'price_manipulation': {
            'description': '价格篡改测试',
            'test_cases': [
                '修改前端价格参数',
                '拦截并修改支付请求',
                '优惠券重复使用',
                '负价格商品下单'
            ]
        },
        'account_security': {
            'description': '账户安全测试',
            'test_cases': [
                '暴力破解密码',
                '短信验证码绕过',
                '会话固定攻击',
                '权限提升测试'
            ]
        },
        'order_security': {
            'description': '订单安全测试',
            'test_cases': [
                '越权查看他人订单',
                '订单状态非法修改',
                '重复提交订单',
                '取消他人订单'
            ]
        }
    }
    return test_scenarios
```

## 移动端测试

### 1. App专项测试
```python
class JDMobileTesting:
    """京东移动端测试要点"""
    
    def app_performance_test(self):
        """App性能测试指标"""
        performance_metrics = {
            'startup_time': {
                'cold_start': '< 3秒',
                'warm_start': '< 1.5秒',
                'hot_start': '< 0.5秒'
            },
            'memory_usage': {
                'peak_memory': '< 500MB',
                'average_memory': '< 200MB',
                'memory_leak': '无内存泄漏'
            },
            'battery_consumption': {
                'background': '< 2%/小时',
                'foreground': '< 8%/小时',
                'heavy_usage': '< 15%/小时'
            },
            'network_usage': {
                'data_compression': '> 30%',
                'request_optimization': '合并请求',
                'cache_hit_rate': '> 80%'
            }
        }
        return performance_metrics
    
    def compatibility_test(self):
        """兼容性测试矩阵"""
        compatibility_matrix = {
            'android': {
                'versions': ['9', '10', '11', '12', '13'],
                'brands': ['华为', '小米', 'OPPO', 'vivo', '三星'],
                'resolutions': ['720p', '1080p', '2K', '4K'],
                'chipsets': ['高通', '联发科', '麒麟', '三星']
            },
            'ios': {
                'versions': ['14', '15', '16', '17'],
                'devices': ['iPhone 8', 'iPhone X', 'iPhone 12', 'iPhone 14'],
                'screens': ['4.7寸', '5.5寸', '6.1寸', '6.7寸']
            }
        }
        return compatibility_matrix
```

## 质量保障体系建设

### 1. CI/CD集成测试
```python
class JDCIPipeline:
    """京东持续集成测试流水线"""
    
    def automated_pipeline(self):
        """自动化测试流水线"""
        pipeline_stages = {
            'code_commit': {
                'trigger': '代码提交',
                'actions': ['静态代码扫描', '单元测试'],
                'tools': ['SonarQube', 'Pytest'],
                'gate': '代码覆盖率>80%'
            },
            'integration': {
                'trigger': '代码合并',
                'actions': ['接口测试', '集成测试'],
                'tools': ['Postman', 'REST Assured'],
                'gate': '通过率100%'
            },
            'regression': {
                'trigger': '版本构建',
                'actions': ['回归测试', '兼容性测试'],
                'tools': ['Selenium', 'Appium'],
                'gate': '关键路径无阻塞'
            },
            'performance': {
                'trigger': '预发布部署',
                'actions': ['性能测试', '安全扫描'],
                'tools': ['JMeter', 'OWASP ZAP'],
                'gate': '性能下降<10%'
            },
            'production': {
                'trigger': '生产发布',
                'actions': ['监控验证', '健康检查'],
                'tools': ['Prometheus', 'Grafana'],
                'gate': '核心指标正常'
            }
        }
        return pipeline_stages
```

### 2. 质量度量指标
```python
def quality_metrics_dashboard():
    """质量指标仪表盘"""
    metrics = {
        'test_coverage': {
            'unit_test': '> 85%',
            'integration_test': '> 90%',
            'api_test': '> 95%',
            'ui_test': '> 80%'
        },
        'defect_metrics': {
            'defect_density': '< 0.5个/KLOC',
            'defect_leakage': '< 2%',
            'defect_removal': '> 98%',
            'mean_time_to_fix': '< 4小时'
        },
        'test_effectiveness': {
            'test_pass_rate': '> 99%',
            'automation_coverage': '> 80%',
            'test_execution_time': '< 30分钟',
            'false_positive_rate': '< 5%'
        },
        'release_quality': {
            'release_success_rate': '> 99%',
            'rollback_rate': '< 1%',
            'customer_satisfaction': '> 4.5/5',
            'production_incidents': '< 0.1个/天'
        }
    }
    return metrics
```

## 面试常见问题

### 1. 测试设计相关问题
```python
# 面试问题：如何测试一个搜索功能？
def search_function_testing():
    """搜索功能测试要点"""
    test_dimensions = {
        'functional': [
            '关键词搜索准确性',
            '搜索结果排序',
            '筛选条件组合',
            '搜索结果分页',
            '搜索建议功能'
        ],
        'performance': [
            '搜索响应时间<2秒',
            '并发搜索支持',
            '大数据量搜索',
            '索引更新延迟'
        ],
        'usability': [
            '搜索框易用性',
            '结果展示清晰度',
            '无结果提示友好',
            '搜索历史记录'
        ],
        'compatibility': [
            '不同浏览器搜索',
            '移动端搜索体验',
            '多语言搜索支持',
            '特殊字符处理'
        ]
    }
    return test_dimensions

# 面试问题：发现偶现bug如何处理？
def intermittent_bug_handling():
    """偶现bug处理流程"""
    process = {
        'step1_reproduce': [
            '收集复现条件',
            '记录操作步骤',
            '保存环境信息',
            '获取日志文件'
        ],
        'step2_isolate': [
            '简化复现步骤',
            '排除干扰因素',
            '确定触发条件',
            '分析影响范围'
        ],
        'step3_investigate': [
            '代码逻辑分析',
            '并发时序分析',
            '资源竞争检查',
            '异常路径验证'
        ],
        'step4_fix_verify': [
            '制定修复方案',
            '回归测试验证',
            '稳定性测试',
            '监控上线表现'
        ]
    }
    return process
```