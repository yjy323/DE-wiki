### Global Infra Structure
1. Region: AWS가 서비스를 제공하는 도시
2. Availability Zone(AZ): 가용 영역, Region은 최소 두개의 AZ
	- Availability: 서비스의 **가용성**
		- 기본 조치 = 서버를 이중화
	- 데이터 센터(물리적으로는 1대의 데이터 센터를 의미하지 않는다(N대))
3. Edge Location
	- 요청에 대한 응답을 빠르게 내려줄 때 사용
	- ex) DNS(Route 53), CDN(CloudFront), Lambda edge
### VPC
Virtual Private Cloud(가상 사설망)
- 내부적으로는 private IP로 통신
- 2개 이상의 AZ 위에 구성된다.
- **Subnet**
	- VPC보다 작은 단위로 IP를 할당하기 위한 공간
	- 하나의 서브넷은 AZ에 귀속된다.
- 기본적으로 **인터넷과 통신할 수 없다**.
- Public 인터넷 통신 조건
	1. Internet Gateway(igw - idxxx) - VPC에 할당
	2. public IP - 서브넷에 할당
	3. Route Table
		1. 사용자 정의 라우팅 테이블 - N 개의 서브넷에 할당
		2. 메인 라우팅 테이블 - VPC에 할당
			1. VPC 하나에 기본적으로 생성, 내부적인 통신
	4. 보안 그룹(Security Group)
		1. 방화벽 역할
		2. *인스턴스 단위* 보안 규칙
			1. 인스턴스 - SG는 N:N 할당
		3. *허용 규칙만 지원*, Default *All Deny*
		4. Stateful
		5. <> Network Access Control List
			1. *서브넷 단위* 보안 규칙
			2. 허용, 거부 규칙 모두 지원, Default All Open
			3. Stateless -> 인바운드/아웃바운드 모두 정의 필요 -> 자주 하는 실수
### CIDR
- IPv4의 대역을 정의하는 표기법
- 0.0.0.0 - 255.255.255.255
- Masking, IP 대역을 $2^n$ 개까지 할당한다는 의미
### IAM
- **AWS 서비스 사용자**(개발자)에 대한 AuthN, AuthZ
	- AuthN: 자격 증명 인증
	- AuthZ: 권한 관리
- IAM 구성요소
	- User: AWS 리소스에 대한 액세스 **권한 부여 대상**
	- Group: 동일한 **권한을 공유**하는 User 모음
	- Role:
		- User에게 **임시**로 권한 부여 자격 증명
			- User의 권한을 **덮어 씌운다**.
		- User는 여러 Role 부여 가능 <> 동시 사용 불가
		- AWS 서비스에도 부여 가능
	- Policy: Permission의 묶음
		- 권한은 어떤 리소스에 대한 **ALLOW, DENY를 결정**한다.
		- 대부분 AWS에 JSON 문서로 저장한다.
- 요소끼리 충돌 여부 = 중요 X, 정책끼리 충돌할 때
	1. DENY 우선 평가
	2. ALLOW
---
#### Auto Scailing
- SG Chaining
	- RDS에서 접근 제어할 IP는 동적이다.
	- 이 때 RDS 인바운드 IP로 SG를 지정해 DB 접근 문제를 해결한다.
		- 보안 그룸 sg-idxxx가 있을 때, 해당 보안 그룹에서의 접근을 허용한다.