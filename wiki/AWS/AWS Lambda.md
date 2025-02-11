Use to run code *without provisioning or managing* servers.
- HA compute infrastructure
- All of the administration of the compute resources
#### 특징
1. **이벤트 기반** 아키텍처
	1. 상시 가동 X, 특정 이벤트 발생 시 실행
2. 서버 관리 불필요
	2. Auto Scale up-down
	3. 고가용성
#### Lambda는 어떤 요구사항, Challenge 속에서 등장했을까?
- 클라우드 인프라 발전 - MSA, 서버리스로 애플리케이션 아키텍처의 변화
- 빠른 프로토타이핑 요구 - 빨라진 개발/배포 사이클
#### Lambda를 왜 쓸까?
- 인프라 운영 부담 제거
- 개발자가 비즈니스 로직 구현에만 집중
- **짧고 주기가 일정한 작업**에 유리
	1. Batch
	2. 소규모/단순 작업
- Responsible only for Code
### [Lambda Key features](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html#features)
개발자가 Lambda 앱을 개발할 때 scalable, secure, and easily extensible하게 개발할 수 있도록 돕는다.

### Get Started:
- 간단한 Lambda function을 작성하고 실행하며 Lambda의 동작 과정과 환경을 이해한다.
- lambda_handler(event, context)
	- event, context 파라미터를 이해한다.
---
### Basic Concepts
1. Lambda functions
	- A piece of code that runs in **response to events**: 실행의 책임
	- A function has **one specific job**
	- response to specific events에서 **필요할 때만 실행한다**.
2. Lambda runtimes
	- Lambda 함수가 **실행되는 환경**
		- Environment는 격리 환경이고 재사용될 수 있다.
	- 여러 의존성 및 패키지를 포함한다.
3. Triggers and event source mappings
	- 람다 함수를 호출하는 개념의 object
	- AWS CLI, Lambda API, 다른 AWS 서비스의 event가 Trigger가 될 수 있다.
4. The event object
	- 함수를 호출한 event와 함수가 사용하는 데이터를 담고 있는 JSON 객체
		- 정확히는 문서지만, runtime시 객체로 변환된다.
5. Lambda permissions
	- AWS Services가 Lambda를 invoke할 권한
	- Lambda가 다른 AWS Services API를 호출할 권한

+**나머지 Concepts 추가 학습 필요**
### Building with Python
- 파이썬 lambda_handler가 Lambda 환경에서 실제로 동작하는 방법
	- dict로 저장되는 event object
	- Lambda runtime에 포함된 파이썬 환경
- Best Practice
	- lambda_handler와 로직을 분리하라
	- 실행 시간 및 크기를 고려해 배포 환경까지 최적화하자
---
## References
- [AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
- [Tutorial: Create an EventBridge scheduled rule for AWS Lambda functions](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-run-lambda-schedule.html)
- [Launch a Spark job in a transient EMR cluster using a Lambda function](https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/launch-a-spark-job-in-a-transient-emr-cluster-using-a-lambda-function.html)