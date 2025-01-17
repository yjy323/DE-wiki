### 도커는 왜 사용하는가?
- 개발, 테스트, 배포 환경의 일관성 유지하기 위해 사용한다.
- 도커는 애플리케이션이 항상 동일한 환경에서 실행하도록 보장한다.
### Docker & AWS EC2
1. 애플리케이션 개발 및 파일 구성
2. 애플리케이션을 Docker 이미지로 만들기 위한 **Dockerfile**을 작성
3. 작성한 Dockerfile을 기반으로 Docker 이미지를 **빌드**
4. Docker 이미지를 **Docker Hub** 또는 **Amazon ECR**에 업로드해 배포 준비
5. AWS EC2 인스턴스에서 Docker 이미지를 실행해 **프로덕션 환경에 배포**

### Dockerfile
Docker 이미지를 만들기 위한 스크립트(설명서)
- **Docker는** Dockerfile을 읽고, 정의된 환경과 명령어에 따라 **이미지**를 생성
- Dockerfile을 통해 애플리케이션의 실행 환경을 표준화하고, **자동화된 배포**

#빌드
- **빌드**(Build)는 개발자가 작성한 **소스 코드**를 **실행 가능**하고 **배포 가능한 형태**로 변환하는 과정
- **컴파일, 링크, 패키징, 테스트** 등의 단계로 구성

```bash
AWS_REGION="ap-northeast-2"
AWS_ACCOUNT_ID="442426874570"
ECR_URI="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"

$(aws ecr get-login-password --region $AWS_REGION | sudo docker login --username AWS --password-stdin $ECR_URI)

# EC2
sudo docker pull ${ECR_URI}/w2m6:latest
sudo docker run -d --rm -p 8888:8888 -e JUPYTER_TOKEN=1111 --name w2m6 ${ECR_URI}/w2m6:latest

# buildx
docker buildx create --use
docker buildx build --platform linux/amd64 -t ${tag} --push --load
# push 옵션: Registry에 등록
# load 옵션: image 생성
docker buildx build --platform linux/amd64 -t 442426874570.dkr.ecr.ap-northeast-2.amazonaws.com/w2m6:latest --push .
```
### EC2 스왑 메모리 설정
```bash
sudo dd if=/dev/zero of=/swapfile bs=128M count=16
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

echo '/swapfile swap swap defaults 0 0' | sudo tee -a /etc/fstab
```

[Docker Reference](https://docs.docker.com/reference/)
## 대화식으로 Hadoop 설치
- 재현 가능성을 위해 우선 Dockerfile에 설치할 패키지를 어느정도 작성하는 것이 좋겠다.
```bash
docker search ubuntu
docker pull ubuntu

docker run -it --name hadoop-base ubuntu

docker exec -it $(docker ps -aqf "name=hadoop-base") /bin/bash
apt update
apt-get update
apt install openjdk-11-jdk # Java 8을 고려해야 할 수도 있다.
```
1. OS 컨테이너 설치
	1. Ubuntu:lastest 사용
2. 컨테이너 TTY 접속
3. 환경 설정을 위한 패키지 설정
4. JDK & Hadoop 환경 변수 설정
```bash
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64
export HADOOP_HOME=/hadoop_home/hadoop-3.3.6
export HADOOP_CONFIG_HOME=$HADOOP_HOME/etc/hadoop
export PATH=$PATH:$HADOOP_HOME/bin
export PATH=$PATH:HADOOP_HOME/sbin
```

## Docker manual
### Docker engine
Docker 컨테이너를 빌드, 실행, 배포하는 핵심 소프트웨어