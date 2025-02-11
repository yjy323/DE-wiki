*가상*의 서버
- OS
	- AMI(Amazon Machine Image)
- Family Type
	- 머신의 목적
		- 범용, Memory Optimized, Compute Optimized...
- 인스턴스 타입
	- 메모리, 디스크, vCPU 결정
	- Ex) T2.micro
		- T: 인스턴스 타입
		- 2: 세대
		- micro: 스펙
---
### EC2 Life Cycle
- 가상화 저장공간(디스크)
	1. EBS(Elastic Block Storage)
	2. Instance Strorage
- Stop - Running
	- Pending이 일어난다 = 다른 장비에서 실행
- Reboot
	- Pending이 일어나지 않는다 = 같은 장비에서 실행
