# 京东测试开发面试 - 测试场景算法题

def analyze_log_times(log_lines):
    """
    分析日志时间戳，统计每小时的日志数量
    京东面试常考：日志分析相关算法
    """
    from collections import defaultdict
    import re
    
    # 存储每小时日志数量
    hourly_count = defaultdict(int)
    
    # 时间戳正则表达式
    time_pattern = r'(\d{4}-\d{2}-\d{2} \d{2}):\d{2}:\d{2}'
    
    for line in log_lines:
        match = re.search(time_pattern, line)
        if match:
            hour = match.group(1)
            hourly_count[hour] += 1
    
    return dict(hourly_count)

def find_error_patterns(log_lines):
    """
    查找错误日志模式
    统计不同类型的错误出现频次
    """
    from collections import defaultdict
    import re
    
    error_patterns = {
        'NullPointerException': r'NullPointerException',
        'ArrayIndexOutOfBounds': r'ArrayIndexOutOfBoundsException',
        'FileNotFound': r'FileNotFoundException',
        'SQLException': r'SQLException',
        'Timeout': r'TimeoutException|timeout'
    }
    
    error_count = defaultdict(int)
    
    for line in log_lines:
        for error_type, pattern in error_patterns.items():
            if re.search(pattern, line, re.IGNORECASE):
                error_count[error_type] += 1
                break
    
    return dict(error_count)

def generate_boundary_test_cases(min_val, max_val):
    """
    生成边界值测试用例
    测试开发常考：测试用例设计算法
    """
    test_cases = []
    
    # 边界值分析
    # 最小值、略高于最小值、正常值、略低于最大值、最大值
    boundary_values = [
        min_val,                    # 最小值
        min_val + 1,                # 略高于最小值
        (min_val + max_val) // 2,   # 正常值
        max_val - 1,                # 略低于最大值
        max_val                     # 最大值
    ]
    
    # 边界外值（用于异常测试）
    invalid_cases = [
        min_val - 1,                # 低于最小值
        max_val + 1                 # 高于最大值
    ]
    
    return {
        'valid_boundary_cases': boundary_values,
        'invalid_cases': invalid_cases
    }

def validate_data_format(data_list, expected_format):
    """
    验证数据格式
    测试数据校验算法
    """
    validation_results = []
    
    for i, data in enumerate(data_list):
        result = {
            'index': i,
            'data': data,
            'is_valid': True,
            'errors': []
        }
        
        # 格式验证
        if expected_format == 'email':
            import re
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, data):
                result['is_valid'] = False
                result['errors'].append('Invalid email format')
        
        elif expected_format == 'phone':
            import re
            phone_pattern = r'^1[3-9]\d{9}$'
            if not re.match(phone_pattern, data):
                result['is_valid'] = False
                result['errors'].append('Invalid phone format')
        
        elif expected_format == 'date':
            try:
                from datetime import datetime
                datetime.strptime(data, '%Y-%m-%d')
            except ValueError:
                result['is_valid'] = False
                result['errors'].append('Invalid date format, expected YYYY-MM-DD')
        
        validation_results.append(result)
    
    return validation_results

def performance_test_analysis(response_times):
    """
    性能测试结果分析
    计算性能指标
    """
    if not response_times:
        return {}
    
    import statistics
    
    analysis = {
        'total_requests': len(response_times),
        'min_response_time': min(response_times),
        'max_response_time': max(response_times),
        'avg_response_time': statistics.mean(response_times),
        'median_response_time': statistics.median(response_times),
        'p90_response_time': statistics.quantiles(response_times, n=10)[8],  # 90分位数
        'p95_response_time': statistics.quantiles(response_times, n=20)[18], # 95分位数
        'p99_response_time': statistics.quantiles(response_times, n=100)[98], # 99分位数
    }
    
    # 计算TPS (Transactions Per Second)
    total_time = sum(response_times) / 1000  # 转换为秒
    if total_time > 0:
        analysis['tps'] = len(response_times) / total_time
    
    return analysis

# 测试用例
def test_scenario_algorithms():
    print("=== 测试场景算法测试 ===")
    
    # 测试1：日志时间分析
    print("\n1. 日志时间分析测试")
    log_lines = [
        "2024-01-15 14:23:45 INFO User login successful",
        "2024-01-15 14:24:12 ERROR Database connection failed",
        "2024-01-15 14:25:30 INFO Order processed successfully",
        "2024-01-15 15:10:22 ERROR TimeoutException: Request timeout",
        "2024-01-15 15:11:45 INFO User logout successful"
    ]
    hourly_stats = analyze_log_times(log_lines)
    print(f"每小时日志统计: {hourly_stats}")
    
    # 测试2：错误模式分析
    print("\n2. 错误模式分析测试")
    error_logs = [
        "java.lang.NullPointerException at com.example.UserService.getUser",
        "java.io.FileNotFoundException: config.properties not found",
        "SQLException: Connection timeout after 30 seconds",
        "ArrayIndexOutOfBoundsException: Index 10 out of bounds for length 5",
        "TimeoutException: Request timeout after 5000ms"
    ]
    error_stats = find_error_patterns(error_logs)
    print(f"错误类型统计: {error_stats}")
    
    # 测试3：边界值测试用例生成
    print("\n3. 边界值测试用例生成")
    boundary_cases = generate_boundary_test_cases(1, 100)
    print(f"边界值测试用例: {boundary_cases}")
    
    # 测试4：数据格式验证
    print("\n4. 数据格式验证测试")
    emails = ["user@example.com", "invalid.email", "test@gmail.com"]
    email_validation = validate_data_format(emails, 'email')
    print(f"邮箱验证结果: {email_validation}")
    
    # 测试5：性能分析
    print("\n5. 性能测试结果分析")
    response_times = [100, 150, 200, 120, 180, 300, 250, 160, 140, 220]  # 毫秒
    performance_stats = performance_test_analysis(response_times)
    print(f"性能分析结果:")
    for key, value in performance_stats.items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    test_scenario_algorithms()