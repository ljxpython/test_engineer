# CI/CD集成测试专题

## 专题概述
本专题涵盖持续集成和持续部署中的测试自动化实践，包括测试流水线设计、Docker容器化测试、云原生测试策略等现代DevOps测试核心技能。

**核心技能点**：
- CI/CD流水线中的测试集成
- Docker容器化测试环境
- Kubernetes测试部署策略
- 测试数据管理和环境隔离
- 监控和可观测性测试
- 基础设施即代码（IaC）测试

---

## 题目列表

### ⭐⭐⭐ CI/CD流水线中测试阶段的设计与实现
**难度**：⭐⭐⭐  
**频率**：🔥🔥🔥

**标准答案**：
**CI/CD测试流水线架构**：

```yaml
# .gitlab-ci.yml - GitLab CI/CD配置示例
stages:
  - code-quality
  - unit-test
  - integration-test
  - security-test
  - build
  - deploy-staging
  - e2e-test
  - performance-test
  - deploy-production

variables:
  DOCKER_IMAGE: "${CI_REGISTRY_IMAGE}:${CI_COMMIT_SHA}"
  POSTGRES_DB: "test_db"
  POSTGRES_USER: "test_user"
  POSTGRES_PASSWORD: "test_password"

# 代码质量检查阶段
code-quality:
  stage: code-quality
  image: sonarsource/sonar-scanner-cli:latest
  services:
    - postgres:13
  script:
    - sonar-scanner
      -Dsonar.projectKey=${CI_PROJECT_NAME}
      -Dsonar.sources=src/
      -Dsonar.host.url=${SONAR_HOST_URL}
      -Dsonar.login=${SONAR_TOKEN}
    - python -m pylint src/ --output-format=parseable --reports=no
    - python -m flake8 src/ --format=junit-xml --output-file=flake8-report.xml
    - python -m bandit -r src/ -f json -o bandit-report.json
  artifacts:
    reports:
      junit:
        - flake8-report.xml
      codequality: bandit-report.json
    paths:
      - coverage/
    expire_in: 1 day
  coverage: '/Total coverage: \d+\.\d+%/'

# 单元测试阶段
unit-test:
  stage: unit-test
  image: python:3.9
  services:
    - redis:6.2
    - postgres:13
  before_script:
    - pip install -r requirements.txt
    - pip install pytest pytest-cov pytest-xdist
  script:
    - pytest tests/unit/ 
      --cov=src/ 
      --cov-report=xml 
      --cov-report=html 
      --junitxml=unit-test-report.xml
      -n auto  # 并行执行
  artifacts:
    reports:
      junit: unit-test-report.xml
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml
    paths:
      - htmlcov/
    expire_in: 1 day
  coverage: '/Total coverage: \d+%/'

# 集成测试阶段
integration-test:
  stage: integration-test
  image: python:3.9
  services:
    - name: postgres:13
      alias: postgres
    - name: redis:6.2
      alias: redis
    - name: rabbitmq:3.9-management
      alias: rabbitmq
  variables:
    DATABASE_URL: "postgresql://test_user:test_password@postgres:5432/test_db"
    REDIS_URL: "redis://redis:6379/0"
    RABBITMQ_URL: "amqp://guest:guest@rabbitmq:5672/"
  before_script:
    - pip install -r requirements.txt
    - python manage.py migrate --settings=config.test_settings
    - python manage.py collectstatic --noinput --settings=config.test_settings
  script:
    - pytest tests/integration/ 
      --junitxml=integration-test-report.xml
      --html=integration-test-report.html
      --self-contained-html
  artifacts:
    reports:
      junit: integration-test-report.xml
    paths:
      - integration-test-report.html
    expire_in: 1 day

# 安全测试阶段
security-test:
  stage: security-test
  image: owasp/zap2docker-stable
  services:
    - name: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
      alias: app
  script:
    - mkdir -p /zap/wrk/
    - zap-baseline.py -t http://app:8000 -g gen.conf -r zap-report.html
    - zap-api-scan.py -t http://app:8000/api/v1/openapi.json -f openapi -r zap-api-report.html
    # 检查高危漏洞
    - python /zap/check_zap_results.py zap-report.html
  artifacts:
    paths:
      - zap-report.html
      - zap-api-report.html
    reports:
      junit: zap-junit-report.xml
    expire_in: 1 week
  allow_failure: true

# 构建阶段
build:
  stage: build
  image: docker:20.10.16
  services:
    - docker:20.10.16-dind
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker build -t $DOCKER_IMAGE .
    - docker push $DOCKER_IMAGE
  only:
    - main
    - develop

# 部署到测试环境
deploy-staging:
  stage: deploy-staging
  image: alpine/helm:3.8.1
  before_script:
    - kubectl config set-cluster k8s --server="$K8S_SERVER" --certificate-authority="$K8S_CA"
    - kubectl config set-credentials gitlab --token="$K8S_TOKEN"
    - kubectl config set-context default --cluster=k8s --user=gitlab
    - kubectl config use-context default
  script:
    - helm upgrade --install myapp-staging helm/myapp
      --namespace staging
      --create-namespace
      --set image.repository=$CI_REGISTRY_IMAGE
      --set image.tag=$CI_COMMIT_SHA
      --set environment=staging
      --wait --timeout=600s
  environment:
    name: staging
    url: https://staging.example.com
  only:
    - main
    - develop

# E2E测试阶段
e2e-test:
  stage: e2e-test
  image: cypress/included:10.3.0
  services:
    - name: selenium/standalone-chrome:4.0.0
      alias: selenium
  variables:
    CYPRESS_baseUrl: "https://staging.example.com"
    CYPRESS_VIDEO: "true"
    CYPRESS_SCREENSHOT: "true"
  before_script:
    - npm install
    - npx wait-on https://staging.example.com --timeout 300000
  script:
    - npx cypress run --record --key $CYPRESS_RECORD_KEY
  artifacts:
    when: always
    paths:
      - cypress/videos/
      - cypress/screenshots/
      - cypress/reports/
    reports:
      junit: cypress/reports/junit.xml
    expire_in: 1 week
  dependencies:
    - deploy-staging

# 性能测试阶段
performance-test:
  stage: performance-test
  image: loadimpact/k6:latest
  variables:
    K6_CLOUD_PROJECT_ID: "$K6_PROJECT_ID"
    K6_CLOUD_TOKEN: "$K6_TOKEN"
  script:
    - k6 run --out cloud tests/performance/load-test.js
    - k6 run --out json=results.json tests/performance/stress-test.js
    - python scripts/analyze_performance.py results.json
  artifacts:
    paths:
      - results.json
      - performance-report.html
    reports:
      performance: performance-report.json
    expire_in: 1 week
  dependencies:
    - deploy-staging
```

**Jenkins Pipeline示例**：
```groovy
// Jenkinsfile - 声明式流水线
pipeline {
    agent {
        kubernetes {
            yaml """
                apiVersion: v1
                kind: Pod
                spec:
                  containers:
                  - name: maven
                    image: maven:3.8.1-jdk-11
                    command: ['cat']
                    tty: true
                  - name: docker
                    image: docker:20.10.16
                    command: ['cat']
                    tty: true
                    volumeMounts:
                    - name: docker-sock
                      mountPath: /var/run/docker.sock
                  - name: kubectl
                    image: bitnami/kubectl:latest
                    command: ['cat']
                    tty: true
                  volumes:
                  - name: docker-sock
                    hostPath:
                      path: /var/run/docker.sock
            """
        }
    }
    
    environment {
        DOCKER_IMAGE = "${env.DOCKER_REGISTRY}/${env.JOB_NAME}:${env.BUILD_NUMBER}"
        KUBECONFIG = credentials('kubeconfig')
        SONAR_TOKEN = credentials('sonar-token')
    }
    
    stages {
        stage('Checkout & Setup') {
            steps {
                checkout scm
                container('maven') {
                    sh '''
                        mvn clean compile
                        mvn dependency:resolve
                    '''
                }
            }
        }
        
        stage('Code Quality') {
            parallel {
                stage('SonarQube Analysis') {
                    steps {
                        container('maven') {
                            sh '''
                                mvn sonar:sonar \
                                  -Dsonar.projectKey=$JOB_NAME \
                                  -Dsonar.host.url=$SONAR_HOST_URL \
                                  -Dsonar.login=$SONAR_TOKEN
                            '''
                        }
                    }
                }
                stage('Security Scan') {
                    steps {
                        container('maven') {
                            sh 'mvn org.owasp:dependency-check-maven:check'
                            publishHTML([
                                allowMissing: false,
                                alwaysLinkToLastBuild: true,
                                keepAll: true,
                                reportDir: 'target',
                                reportFiles: 'dependency-check-report.html',
                                reportName: 'OWASP Dependency Check Report'
                            ])
                        }
                    }
                }
            }
        }
        
        stage('Test') {
            parallel {
                stage('Unit Tests') {
                    steps {
                        container('maven') {
                            sh 'mvn test'
                        }
                    }
                    post {
                        always {
                            junit 'target/surefire-reports/*.xml'
                            publishCoverage adapters: [
                                jacocoAdapter('target/site/jacoco/jacoco.xml')
                            ], sourceFileResolver: sourceFiles('STORE_LAST_BUILD')
                        }
                    }
                }
                
                stage('Integration Tests') {
                    steps {
                        container('maven') {
                            sh '''
                                mvn verify -P integration-test \
                                  -Dspring.profiles.active=integration
                            '''
                        }
                    }
                    post {
                        always {
                            junit 'target/failsafe-reports/*.xml'
                        }
                    }
                }
            }
        }
        
        stage('Build & Push Image') {
            when {
                anyOf {
                    branch 'main'
                    branch 'develop'
                }
            }
            steps {
                container('docker') {
                    sh '''
                        docker build -t $DOCKER_IMAGE .
                        echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin $DOCKER_REGISTRY
                        docker push $DOCKER_IMAGE
                    '''
                }
            }
        }
        
        stage('Deploy to Staging') {
            when {
                anyOf {
                    branch 'main'
                    branch 'develop'
                }
            }
            steps {
                container('kubectl') {
                    sh '''
                        helm upgrade --install myapp-staging ./helm/myapp \
                          --namespace staging \
                          --set image.repository=${DOCKER_REGISTRY}/${JOB_NAME} \
                          --set image.tag=${BUILD_NUMBER} \
                          --set environment=staging \
                          --wait --timeout=600s
                    '''
                }
            }
        }
        
        stage('E2E Tests') {
            when {
                anyOf {
                    branch 'main'
                    branch 'develop'
                }
            }
            steps {
                script {
                    def stagingUrl = sh(
                        script: "kubectl get ingress myapp-staging -n staging -o jsonpath='{.spec.rules[0].host}'",
                        returnStdout: true
                    ).trim()
                    
                    build job: 'e2e-tests',
                          parameters: [
                              string(name: 'TARGET_URL', value: "https://${stagingUrl}"),
                              string(name: 'TEST_SUITE', value: 'regression')
                          ],
                          wait: true
                }
            }
        }
        
        stage('Performance Tests') {
            when { branch 'main' }
            steps {
                script {
                    build job: 'performance-tests',
                          parameters: [
                              string(name: 'TARGET_URL', value: env.STAGING_URL),
                              string(name: 'LOAD_PATTERN', value: 'baseline')
                          ],
                          wait: true
                }
            }
        }
        
        stage('Deploy to Production') {
            when {
                allOf {
                    branch 'main'
                    expression { 
                        return currentBuild.result == null || currentBuild.result == 'SUCCESS' 
                    }
                }
            }
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    input message: 'Deploy to Production?', 
                          ok: 'Deploy',
                          parameters: [
                              choice(name: 'DEPLOYMENT_STRATEGY',
                                   choices: ['blue-green', 'rolling', 'canary'],
                                   description: 'Deployment Strategy')
                          ]
                }
                
                container('kubectl') {
                    sh '''
                        helm upgrade --install myapp-prod ./helm/myapp \
                          --namespace production \
                          --set image.repository=${DOCKER_REGISTRY}/${JOB_NAME} \
                          --set image.tag=${BUILD_NUMBER} \
                          --set environment=production \
                          --set deployment.strategy=${DEPLOYMENT_STRATEGY} \
                          --wait --timeout=900s
                    '''
                }
            }
        }
    }
    
    post {
        always {
            publishTestResults testResultsPattern: 'target/surefire-reports/*.xml, target/failsafe-reports/*.xml'
            
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'target/site',
                reportFiles: 'index.html',
                reportName: 'Test Coverage Report'
            ])
        }
        
        failure {
            emailext(
                subject: "Build Failed: ${env.JOB_NAME} - ${env.BUILD_NUMBER}",
                body: "Build failed. Check console output at ${env.BUILD_URL}",
                to: "${env.DEVELOPER_EMAIL}"
            )
            
            slackSend(
                channel: '#ci-cd',
                color: 'danger',
                message: "Build Failed: ${env.JOB_NAME} - ${env.BUILD_NUMBER}"
            )
        }
        
        success {
            slackSend(
                channel: '#ci-cd',
                color: 'good',
                message: "Build Successful: ${env.JOB_NAME} - ${env.BUILD_NUMBER}"
            )
        }
    }
}
```

**GitHub Actions工作流示例**：
```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
      
      redis:
        image: redis:6.2
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379
    
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
        cache: 'pip'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-test.txt
    
    - name: Lint with flake8
      run: |
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    
    - name: Test with pytest
      env:
        DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
        REDIS_URL: redis://localhost:6379/0
      run: |
        pytest --cov=./ --cov-report=xml --junitxml=junit.xml
    
    - name: Upload coverage reports
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella
    
    - name: Upload test results
      uses: dorny/test-reporter@v1
      if: success() || failure()
      with:
        name: Test Results (Python ${{ matrix.python-version }})
        path: junit.xml
        reporter: java-junit

  security:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Run Bandit security scan
      uses: securecodewarrior/github-action-bandit@v1
      with:
        config_file: .bandit
    
    - name: Run Safety check
      run: |
        pip install safety
        safety check --json --output safety-report.json
    
    - name: Upload security reports
      uses: actions/upload-artifact@v3
      with:
        name: security-reports
        path: |
          bandit-report.json
          safety-report.json

  build-and-push:
    needs: [test, security]
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && (github.ref == 'refs/heads/main' || github.ref == 'refs/heads/develop')
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v3
    
    - name: Log in to Container Registry
      uses: docker/login-action@v2
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
    
    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v4
      with:
        images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
        tags: |
          type=ref,event=branch
          type=sha,prefix={{branch}}-
    
    - name: Build and push Docker image
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max

  deploy-staging:
    needs: build-and-push
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/develop'
    environment: staging
    
    steps:
    - name: Deploy to staging
      uses: azure/k8s-deploy@v1
      with:
        manifests: |
          k8s/staging/deployment.yaml
          k8s/staging/service.yaml
        images: |
          ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:develop-${{ github.sha }}
        kubectl-version: 'latest'

  e2e-tests:
    needs: deploy-staging
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/develop'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Run E2E tests
      uses: cypress-io/github-action@v5
      with:
        config: baseUrl=https://staging.example.com
        record: true
        parallel: true
        group: 'E2E Tests'
      env:
        CYPRESS_RECORD_KEY: ${{ secrets.CYPRESS_RECORD_KEY }}
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    
    - name: Upload E2E test artifacts
      uses: actions/upload-artifact@v3
      if: failure()
      with:
        name: cypress-screenshots-videos
        path: |
          cypress/screenshots
          cypress/videos

  deploy-production:
    needs: [build-and-push, e2e-tests]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: production
    
    steps:
    - name: Deploy to production
      uses: azure/k8s-deploy@v1
      with:
        manifests: |
          k8s/production/deployment.yaml
          k8s/production/service.yaml
        images: |
          ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:main-${{ github.sha }}
        kubectl-version: 'latest'
        strategy: blue-green
```

**测试流水线最佳实践**：
```python
# pipeline_utils.py - 流水线工具函数
import os
import yaml
import json
import subprocess
from typing import Dict, List, Any

class PipelineTestManager:
    def __init__(self, config_path: str):
        self.config = self.load_config(config_path)
        self.test_results = {}
    
    def load_config(self, config_path: str) -> Dict:
        """加载流水线配置"""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def run_test_stage(self, stage_name: str) -> Dict[str, Any]:
        """执行测试阶段"""
        stage_config = self.config['stages'].get(stage_name)
        if not stage_config:
            raise ValueError(f"Stage {stage_name} not found in config")
        
        result = {
            'stage': stage_name,
            'status': 'running',
            'start_time': self.get_current_timestamp(),
            'commands': stage_config.get('commands', []),
            'artifacts': [],
            'test_results': {}
        }
        
        try:
            # 执行前置脚本
            if 'before_script' in stage_config:
                self.execute_commands(stage_config['before_script'])
            
            # 执行主要命令
            for command in stage_config['commands']:
                exit_code = self.execute_command(command)
                if exit_code != 0 and not stage_config.get('allow_failure', False):
                    raise subprocess.CalledProcessError(exit_code, command)
            
            # 执行后置脚本
            if 'after_script' in stage_config:
                self.execute_commands(stage_config['after_script'])
            
            # 收集构件
            if 'artifacts' in stage_config:
                result['artifacts'] = self.collect_artifacts(
                    stage_config['artifacts']
                )
            
            # 解析测试结果
            if 'reports' in stage_config:
                result['test_results'] = self.parse_test_reports(
                    stage_config['reports']
                )
            
            result['status'] = 'success'
            result['end_time'] = self.get_current_timestamp()
            
        except Exception as e:
            result['status'] = 'failed'
            result['error'] = str(e)
            result['end_time'] = self.get_current_timestamp()
            
            # 失败时仍然收集构件
            if 'artifacts' in stage_config:
                result['artifacts'] = self.collect_artifacts(
                    stage_config['artifacts']
                )
        
        self.test_results[stage_name] = result
        return result
    
    def execute_command(self, command: str) -> int:
        """执行命令并返回退出码"""
        print(f"Executing: {command}")
        process = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )
        
        if process.stdout:
            print(process.stdout)
        if process.stderr:
            print(process.stderr)
        
        return process.returncode
    
    def execute_commands(self, commands: List[str]) -> None:
        """执行多个命令"""
        for command in commands:
            exit_code = self.execute_command(command)
            if exit_code != 0:
                raise subprocess.CalledProcessError(exit_code, command)
    
    def collect_artifacts(self, artifacts_config: Dict) -> List[str]:
        """收集构件"""
        collected = []
        
        for artifact_path in artifacts_config.get('paths', []):
            if os.path.exists(artifact_path):
                # 复制到构件目录
                artifact_dir = 'artifacts'
                os.makedirs(artifact_dir, exist_ok=True)
                
                import shutil
                dest_path = os.path.join(artifact_dir, os.path.basename(artifact_path))
                
                if os.path.isfile(artifact_path):
                    shutil.copy2(artifact_path, dest_path)
                else:
                    shutil.copytree(artifact_path, dest_path, dirs_exist_ok=True)
                
                collected.append(dest_path)
        
        return collected
    
    def parse_test_reports(self, reports_config: Dict) -> Dict:
        """解析测试报告"""
        results = {}
        
        # 解析JUnit报告
        if 'junit' in reports_config:
            junit_files = reports_config['junit']
            if isinstance(junit_files, str):
                junit_files = [junit_files]
            
            results['junit'] = self.parse_junit_reports(junit_files)
        
        # 解析覆盖率报告
        if 'coverage' in reports_config:
            results['coverage'] = self.parse_coverage_report(
                reports_config['coverage']
            )
        
        return results
    
    def parse_junit_reports(self, junit_files: List[str]) -> Dict:
        """解析JUnit测试报告"""
        import xml.etree.ElementTree as ET
        
        total_tests = 0
        total_failures = 0
        total_errors = 0
        total_skipped = 0
        test_suites = []
        
        for junit_file in junit_files:
            if not os.path.exists(junit_file):
                continue
            
            try:
                tree = ET.parse(junit_file)
                root = tree.getroot()
                
                # 处理testsuite或testsuites根元素
                if root.tag == 'testsuites':
                    testsuites = root.findall('testsuite')
                else:
                    testsuites = [root]
                
                for testsuite in testsuites:
                    suite_data = {
                        'name': testsuite.get('name', ''),
                        'tests': int(testsuite.get('tests', 0)),
                        'failures': int(testsuite.get('failures', 0)),
                        'errors': int(testsuite.get('errors', 0)),
                        'skipped': int(testsuite.get('skipped', 0)),
                        'time': float(testsuite.get('time', 0))
                    }
                    
                    total_tests += suite_data['tests']
                    total_failures += suite_data['failures']
                    total_errors += suite_data['errors']
                    total_skipped += suite_data['skipped']
                    
                    test_suites.append(suite_data)
            
            except ET.ParseError as e:
                print(f"Error parsing JUnit file {junit_file}: {e}")
        
        return {
            'total_tests': total_tests,
            'total_failures': total_failures,
            'total_errors': total_errors,
            'total_skipped': total_skipped,
            'success_rate': ((total_tests - total_failures - total_errors) / total_tests * 100) if total_tests > 0 else 0,
            'test_suites': test_suites
        }
    
    def parse_coverage_report(self, coverage_file: str) -> Dict:
        """解析覆盖率报告"""
        if not os.path.exists(coverage_file):
            return {}
        
        if coverage_file.endswith('.xml'):
            return self.parse_cobertura_coverage(coverage_file)
        elif coverage_file.endswith('.json'):
            return self.parse_json_coverage(coverage_file)
        
        return {}
    
    def parse_cobertura_coverage(self, coverage_file: str) -> Dict:
        """解析Cobertura格式的覆盖率报告"""
        import xml.etree.ElementTree as ET
        
        try:
            tree = ET.parse(coverage_file)
            root = tree.getroot()
            
            line_rate = float(root.get('line-rate', 0))
            branch_rate = float(root.get('branch-rate', 0))
            
            return {
                'line_coverage': line_rate * 100,
                'branch_coverage': branch_rate * 100,
                'total_coverage': (line_rate + branch_rate) / 2 * 100
            }
        
        except Exception as e:
            print(f"Error parsing coverage file {coverage_file}: {e}")
            return {}
    
    def generate_pipeline_report(self) -> str:
        """生成流水线测试报告"""
        report = "# CI/CD Pipeline Test Report\n\n"
        
        total_stages = len(self.test_results)
        successful_stages = len([r for r in self.test_results.values() if r['status'] == 'success'])
        
        report += f"## Summary\n"
        report += f"- Total Stages: {total_stages}\n"
        report += f"- Successful: {successful_stages}\n"
        report += f"- Failed: {total_stages - successful_stages}\n"
        report += f"- Success Rate: {successful_stages/total_stages*100:.1f}%\n\n"
        
        for stage_name, result in self.test_results.items():
            report += f"## Stage: {stage_name}\n"
            report += f"- Status: {result['status']}\n"
            report += f"- Duration: {self.calculate_duration(result)}\n"
            
            if 'test_results' in result and result['test_results']:
                junit_results = result['test_results'].get('junit', {})
                if junit_results:
                    report += f"- Tests: {junit_results['total_tests']}\n"
                    report += f"- Failures: {junit_results['total_failures']}\n"
                    report += f"- Success Rate: {junit_results['success_rate']:.1f}%\n"
                
                coverage_results = result['test_results'].get('coverage', {})
                if coverage_results:
                    report += f"- Coverage: {coverage_results.get('total_coverage', 0):.1f}%\n"
            
            if result['status'] == 'failed' and 'error' in result:
                report += f"- Error: {result['error']}\n"
            
            report += "\n"
        
        return report
    
    def get_current_timestamp(self) -> str:
        """获取当前时间戳"""
        import datetime
        return datetime.datetime.now().isoformat()
    
    def calculate_duration(self, result: Dict) -> str:
        """计算阶段持续时间"""
        if 'start_time' not in result or 'end_time' not in result:
            return "Unknown"
        
        import datetime
        start = datetime.datetime.fromisoformat(result['start_time'])
        end = datetime.datetime.fromisoformat(result['end_time'])
        duration = end - start
        
        return str(duration)

# 使用示例
if __name__ == "__main__":
    pipeline_manager = PipelineTestManager('pipeline-config.yaml')
    
    # 执行测试阶段
    stages = ['unit-test', 'integration-test', 'security-test', 'e2e-test']
    
    for stage in stages:
        try:
            result = pipeline_manager.run_test_stage(stage)
            print(f"Stage {stage}: {result['status']}")
        except Exception as e:
            print(f"Stage {stage} failed: {e}")
    
    # 生成报告
    report = pipeline_manager.generate_pipeline_report()
    print(report)
    
    # 保存报告
    with open('pipeline-report.md', 'w') as f:
        f.write(report)
```

---

### ⭐⭐⭐ Docker容器化测试环境的设计与管理
**难度**：⭐⭐⭐  
**频率**：🔥🔥🔥

**标准答案**：
**容器化测试架构设计**：

```yaml
# docker-compose.test.yml - 测试环境编排
version: '3.8'

services:
  # 应用服务
  app:
    build:
      context: .
      dockerfile: Dockerfile.test
      args:
        - BUILD_ENV=test
    environment:
      - DATABASE_URL=postgresql://testuser:testpass@postgres:5432/testdb
      - REDIS_URL=redis://redis:6379/0
      - RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672/
      - ELASTICSEARCH_URL=http://elasticsearch:9200
      - LOG_LEVEL=DEBUG
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
      rabbitmq:
        condition: service_healthy
    volumes:
      - ./tests:/app/tests
      - ./coverage:/app/coverage
      - test-results:/app/test-results
    networks:
      - test-network
    command: |
      sh -c "
        echo 'Waiting for services to be ready...'
        sleep 10
        python manage.py migrate --run-syncdb
        python manage.py collectstatic --noinput
        pytest tests/ --cov=app --cov-report=html --cov-report=xml --junitxml=test-results/junit.xml
      "

  # 数据库服务
  postgres:
    image: postgres:13-alpine
    environment:
      POSTGRES_DB: testdb
      POSTGRES_USER: testuser
      POSTGRES_PASSWORD: testpass
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./tests/fixtures/db_init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - test-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U testuser -d testdb"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s

  # 缓存服务
  redis:
    image: redis:6.2-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis-data:/data
    networks:
      - test-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3

  # 消息队列
  rabbitmq:
    image: rabbitmq:3.9-management-alpine
    environment:
      RABBITMQ_DEFAULT_USER: guest
      RABBITMQ_DEFAULT_PASS: guest
    volumes:
      - rabbitmq-data:/var/lib/rabbitmq
    networks:
      - test-network
    healthcheck:
      test: ["CMD", "rabbitmqctl", "status"]
      interval: 30s
      timeout: 10s
      retries: 3

  # 搜索引擎
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.17.0
    environment:
      - discovery.type=single-node
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
      - xpack.security.enabled=false
    volumes:
      - elasticsearch-data:/usr/share/elasticsearch/data
    networks:
      - test-network
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:9200/_cluster/health || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3

  # 模拟外部API服务
  mock-api:
    image: wiremock/wiremock:2.35.0
    volumes:
      - ./tests/mocks:/home/wiremock
    networks:
      - test-network
    ports:
      - "8080:8080"
    command: ["--global-response-templating", "--verbose"]

  # Selenium Grid Hub
  selenium-hub:
    image: selenium/hub:4.0.0
    environment:
      - GRID_MAX_SESSION=4
      - GRID_BROWSER_TIMEOUT=300
      - GRID_TIMEOUT=300
    networks:
      - test-network
    ports:
      - "4444:4444"

  # Chrome节点
  selenium-chrome:
    image: selenium/node-chrome:4.0.0
    depends_on:
      - selenium-hub
    environment:
      - HUB_HOST=selenium-hub
      - HUB_PORT=4444
      - NODE_MAX_INSTANCES=2
      - NODE_MAX_SESSION=2
    volumes:
      - /dev/shm:/dev/shm
    networks:
      - test-network
    scale: 2

  # Firefox节点
  selenium-firefox:
    image: selenium/node-firefox:4.0.0
    depends_on:
      - selenium-hub
    environment:
      - HUB_HOST=selenium-hub
      - HUB_PORT=4444
      - NODE_MAX_INSTANCES=2
      - NODE_MAX_SESSION=2
    volumes:
      - /dev/shm:/dev/shm
    networks:
      - test-network

  # 测试报告服务
  allure:
    image: frankescobar/allure-docker-service
    environment:
      CHECK_RESULTS_EVERY_SECONDS: 1
      KEEP_HISTORY: 1
    ports:
      - "5050:5050"
    volumes:
      - allure-results:/app/allure-results
      - allure-reports:/app/default-reports
    networks:
      - test-network

volumes:
  postgres-data:
  redis-data:
  rabbitmq-data:
  elasticsearch-data:
  test-results:
  allure-results:
  allure-reports:

networks:
  test-network:
    driver: bridge
```

**多阶段测试Dockerfile**：
```dockerfile
# Dockerfile.test - 多阶段测试镜像
# 基础阶段
FROM python:3.9-slim as base
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 开发依赖阶段
FROM base as dev-deps
COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

# 测试阶段
FROM dev-deps as test
COPY . .

# 安装测试工具
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    && rm -rf /var/lib/apt/lists/*

# 安装代码质量工具
RUN pip install \
    pytest \
    pytest-cov \
    pytest-xdist \
    pytest-mock \
    pytest-django \
    pytest-asyncio \
    bandit \
    safety \
    black \
    flake8 \
    mypy

# 创建测试用户
RUN groupadd -r testuser && useradd -r -g testuser testuser
RUN chown -R testuser:testuser /app
USER testuser

# 设置测试环境变量
ENV PYTHONPATH=/app
ENV DJANGO_SETTINGS_MODULE=config.settings.test
ENV TESTING=true

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

# 默认命令
CMD ["pytest", "tests/", "--cov=app/", "--cov-report=html", "--cov-report=xml"]

# 生产构建阶段
FROM base as production
COPY . .
RUN pip install --no-cache-dir gunicorn
EXPOSE 8000
CMD ["gunicorn", "app.wsgi:application", "--bind", "0.0.0.0:8000"]
```

**容器化测试管理工具**：
```python
# docker_test_manager.py - Docker测试环境管理器
import docker
import subprocess
import yaml
import json
import time
import os
from typing import Dict, List, Any, Optional
import logging

class DockerTestManager:
    def __init__(self, compose_file: str = "docker-compose.test.yml"):
        self.compose_file = compose_file
        self.client = docker.from_env()
        self.project_name = os.path.basename(os.getcwd()).lower()
        self.logger = self.setup_logger()
    
    def setup_logger(self) -> logging.Logger:
        """设置日志记录器"""
        logger = logging.getLogger('docker_test_manager')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def build_test_environment(self, no_cache: bool = False) -> bool:
        """构建测试环境"""
        try:
            self.logger.info("Building test environment...")
            
            build_cmd = ["docker-compose", "-f", self.compose_file, "build"]
            if no_cache:
                build_cmd.append("--no-cache")
            
            result = subprocess.run(
                build_cmd,
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            
            if result.returncode == 0:
                self.logger.info("Test environment built successfully")
                return True
            else:
                self.logger.error(f"Build failed: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error building test environment: {e}")
            return False
    
    def start_test_services(self, services: Optional[List[str]] = None) -> bool:
        """启动测试服务"""
        try:
            self.logger.info("Starting test services...")
            
            cmd = ["docker-compose", "-f", self.compose_file, "up", "-d"]
            if services:
                cmd.extend(services)
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            
            if result.returncode == 0:
                self.logger.info("Test services started successfully")
                return self.wait_for_services_ready()
            else:
                self.logger.error(f"Failed to start services: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error starting test services: {e}")
            return False
    
    def wait_for_services_ready(self, timeout: int = 300) -> bool:
        """等待服务就绪"""
        self.logger.info("Waiting for services to be ready...")
        
        start_time = time.time()
        
        # 获取所有服务的健康检查状态
        while time.time() - start_time < timeout:
            try:
                result = subprocess.run(
                    ["docker-compose", "-f", self.compose_file, "ps", "--format", "json"],
                    capture_output=True,
                    text=True,
                    cwd=os.getcwd()
                )
                
                if result.returncode == 0:
                    services_status = []
                    for line in result.stdout.strip().split('\n'):
                        if line:
                            service_info = json.loads(line)
                            services_status.append({
                                'name': service_info.get('Service'),
                                'state': service_info.get('State'),
                                'health': service_info.get('Health', 'N/A')
                            })
                    
                    # 检查所有服务是否准备就绪
                    all_ready = True
                    for service in services_status:
                        if service['state'] != 'running':
                            all_ready = False
                            break
                        
                        # 如果有健康检查，等待健康
                        if service['health'] not in ['healthy', 'N/A']:
                            all_ready = False
                            break
                    
                    if all_ready:
                        self.logger.info("All services are ready")
                        return True
                    
                    self.logger.info(f"Waiting for services... Status: {services_status}")
                    time.sleep(10)
                
            except Exception as e:
                self.logger.warning(f"Error checking service status: {e}")
                time.sleep(5)
        
        self.logger.error("Timeout waiting for services to be ready")
        return False
    
    def run_tests(self, test_suite: str = None, parallel: bool = True) -> Dict[str, Any]:
        """运行测试"""
        try:
            self.logger.info(f"Running tests: {test_suite or 'all'}")
            
            # 构建测试命令
            test_cmd = ["pytest"]
            
            if test_suite:
                test_cmd.append(test_suite)
            else:
                test_cmd.append("tests/")
            
            # 添加测试选项
            test_options = [
                "--cov=app/",
                "--cov-report=html:coverage/html",
                "--cov-report=xml:coverage/coverage.xml",
                "--junitxml=test-results/junit.xml",
                "--html=test-results/report.html",
                "--self-contained-html"
            ]
            
            if parallel:
                test_options.extend(["-n", "auto"])  # pytest-xdist并行执行
            
            test_cmd.extend(test_options)
            
            # 在容器中执行测试
            exec_cmd = [
                "docker-compose", "-f", self.compose_file,
                "exec", "-T", "app"
            ] + test_cmd
            
            start_time = time.time()
            result = subprocess.run(
                exec_cmd,
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            end_time = time.time()
            
            # 收集测试结果
            test_result = {
                'exit_code': result.returncode,
                'duration': end_time - start_time,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'success': result.returncode == 0
            }
            
            # 解析测试报告
            test_result.update(self.parse_test_results())
            
            if test_result['success']:
                self.logger.info(f"Tests completed successfully in {test_result['duration']:.2f}s")
            else:
                self.logger.error(f"Tests failed after {test_result['duration']:.2f}s")
            
            return test_result
            
        except Exception as e:
            self.logger.error(f"Error running tests: {e}")
            return {
                'exit_code': 1,
                'success': False,
                'error': str(e)
            }
    
    def parse_test_results(self) -> Dict[str, Any]:
        """解析测试结果"""
        results = {}
        
        # 解析JUnit XML报告
        junit_file = "test-results/junit.xml"
        if os.path.exists(junit_file):
            results['junit'] = self.parse_junit_xml(junit_file)
        
        # 解析覆盖率报告
        coverage_file = "coverage/coverage.xml"
        if os.path.exists(coverage_file):
            results['coverage'] = self.parse_coverage_xml(coverage_file)
        
        return results
    
    def parse_junit_xml(self, junit_file: str) -> Dict[str, Any]:
        """解析JUnit XML报告"""
        import xml.etree.ElementTree as ET
        
        try:
            tree = ET.parse(junit_file)
            root = tree.getroot()
            
            return {
                'tests': int(root.get('tests', 0)),
                'failures': int(root.get('failures', 0)),
                'errors': int(root.get('errors', 0)),
                'skipped': int(root.get('skipped', 0)),
                'time': float(root.get('time', 0))
            }
        except Exception as e:
            self.logger.warning(f"Error parsing JUnit XML: {e}")
            return {}
    
    def parse_coverage_xml(self, coverage_file: str) -> Dict[str, Any]:
        """解析覆盖率XML报告"""
        import xml.etree.ElementTree as ET
        
        try:
            tree = ET.parse(coverage_file)
            root = tree.getroot()
            
            line_rate = float(root.get('line-rate', 0))
            branch_rate = float(root.get('branch-rate', 0))
            
            return {
                'line_coverage': line_rate * 100,
                'branch_coverage': branch_rate * 100,
                'statements': int(root.get('lines-covered', 0)),
                'missing': int(root.get('lines-valid', 0)) - int(root.get('lines-covered', 0))
            }
        except Exception as e:
            self.logger.warning(f"Error parsing coverage XML: {e}")
            return {}
    
    def collect_test_artifacts(self, output_dir: str = "test-output") -> List[str]:
        """收集测试构件"""
        artifacts = []
        
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        
        # 从容器中复制文件
        copy_commands = [
            {
                'source': 'app:/app/test-results',
                'dest': f"{output_dir}/test-results"
            },
            {
                'source': 'app:/app/coverage',
                'dest': f"{output_dir}/coverage"
            },
            {
                'source': 'app:/app/logs',
                'dest': f"{output_dir}/logs"
            }
        ]
        
        for copy_cmd in copy_commands:
            try:
                result = subprocess.run([
                    "docker-compose", "-f", self.compose_file,
                    "cp", copy_cmd['source'], copy_cmd['dest']
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    artifacts.append(copy_cmd['dest'])
                    self.logger.info(f"Collected artifact: {copy_cmd['dest']}")
                else:
                    self.logger.warning(f"Failed to collect {copy_cmd['source']}: {result.stderr}")
            
            except Exception as e:
                self.logger.warning(f"Error collecting artifacts: {e}")
        
        return artifacts
    
    def cleanup_test_environment(self, remove_volumes: bool = False) -> bool:
        """清理测试环境"""
        try:
            self.logger.info("Cleaning up test environment...")
            
            # 停止并删除容器
            cmd = ["docker-compose", "-f", self.compose_file, "down"]
            if remove_volumes:
                cmd.extend(["-v", "--remove-orphans"])
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            
            if result.returncode == 0:
                self.logger.info("Test environment cleaned up successfully")
                
                # 清理悬空镜像
                if remove_volumes:
                    self.client.images.prune(filters={'dangling': True})
                    self.client.volumes.prune()
                
                return True
            else:
                self.logger.error(f"Cleanup failed: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error cleaning up test environment: {e}")
            return False
    
    def run_full_test_cycle(self, test_suite: str = None) -> Dict[str, Any]:
        """运行完整的测试周期"""
        cycle_result = {
            'build': False,
            'start_services': False,
            'run_tests': False,
            'collect_artifacts': False,
            'cleanup': False,
            'overall_success': False
        }
        
        try:
            # 1. 构建测试环境
            cycle_result['build'] = self.build_test_environment()
            if not cycle_result['build']:
                return cycle_result
            
            # 2. 启动测试服务
            cycle_result['start_services'] = self.start_test_services()
            if not cycle_result['start_services']:
                return cycle_result
            
            # 3. 运行测试
            test_result = self.run_tests(test_suite)
            cycle_result['run_tests'] = test_result['success']
            cycle_result['test_details'] = test_result
            
            # 4. 收集构件
            artifacts = self.collect_test_artifacts()
            cycle_result['collect_artifacts'] = len(artifacts) > 0
            cycle_result['artifacts'] = artifacts
            
            # 5. 清理环境
            cycle_result['cleanup'] = self.cleanup_test_environment()
            
            cycle_result['overall_success'] = (
                cycle_result['build'] and
                cycle_result['start_services'] and
                cycle_result['run_tests'] and
                cycle_result['collect_artifacts']
            )
            
        except Exception as e:
            self.logger.error(f"Error in test cycle: {e}")
            cycle_result['error'] = str(e)
        
        finally:
            # 确保清理
            self.cleanup_test_environment()
        
        return cycle_result

# 使用示例
if __name__ == "__main__":
    manager = DockerTestManager()
    
    # 运行完整的测试周期
    result = manager.run_full_test_cycle()
    
    if result['overall_success']:
        print("✅ All tests passed!")
        if 'test_details' in result:
            test_details = result['test_details']
            if 'junit' in test_details:
                junit = test_details['junit']
                print(f"📊 Test Results: {junit['tests']} tests, {junit['failures']} failures")
            if 'coverage' in test_details:
                coverage = test_details['coverage']
                print(f"📈 Coverage: {coverage['line_coverage']:.1f}%")
    else:
        print("❌ Tests failed or environment issues occurred")
        print(f"Build: {result['build']}")
        print(f"Services: {result['start_services']}")
        print(f"Tests: {result['run_tests']}")
```

---

## 专题总结

CI/CD集成测试是现代软件开发的关键环节，需要掌握：

1. **流水线设计**：构建高效的CI/CD测试流水线，实现持续集成
2. **容器化技术**：使用Docker实现一致性的测试环境
3. **自动化集成**：与各种工具和平台的集成配置
4. **环境管理**：测试环境的创建、管理和清理
5. **监控报告**：测试结果的收集、分析和报告生成

**面试回答要点**：
- 展示对DevOps理念和实践的深度理解
- 结合实际项目说明CI/CD实施经验
- 强调测试自动化和持续质量保障
- 体现基础设施即代码和云原生思维