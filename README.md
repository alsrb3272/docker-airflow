# Docker-Ubuntu-Airflow 설치방법

## Part1. Window wsl 설치(Ubuntu)

맨 처음 윈도우에 리눅스를 먼저 설치할 것이다.

------------------

### ※ WSL 시스템 요구사항 ※

아래의 요구사항을 충족시키지 못한다면 아쉽지만 WSL을 설치할 수 없다.

- **OS** : Windows 10 버전 1607이상
- **아키텍처** : x64
- **계정** : 이메일 계정으로 PC로그인 (로컬사용자 제외 - MS스토어 사용을 위해)

----------

### WSL 기본적인 기능 설치를 위한 옵션

제어판 -> 프로그램 -> Windows 기능 켜기/끄기 -> Linux용 Windows 하위 시스템 체크하고 재부팅하기

![wsl](https://github.com/alsrb3272/docker-airflow/blob/d3dd081f88fe93706bff3a12becac2f6d91fdca3/img/%EC%A0%9C%EB%AA%A9%20%EC%97%86%EC%9D%8C.png)



검색창에 Microsoft Store로 이동 후 Linux를 검색하면 하단에 나온 이미지와 같은 앱을 설치

![ubuntu](img/스크린샷_20221228_120110.png)

다운로드가 완료되면 실행을 하여 콘솔 창에 username과 password를 자유롭게 설정하고 들어가면된다.

#### BASH

```bash
# 우분투버전 확인
lsb_release -a
# 현재위치 확인
pwd
# 현재디렉토리 파일정보 
ls -al
# 날짜와 시간확인
date
```



Windows상에 Ubuntu 설치 끝



--------------------

## Part2. Docker 설치

다음으론 Docker 설치하기

[도커설치 사이트](https://docs.docker.com/docker-for-windows/install/)

사이트로 들어가서 설치

[설치참고]([2021.08.14 - [Development Environment\] - Windows 10에 WSL2 설치하기](https://hkim-data.tistory.com/17))



-----------------

## Part3. Airflow 설치

Airflow documentation을 읽고 Docker 기반으로 Airflow를 설치했다.

```bash
# docker 디렉터리 생성 및 이동 
$ mkdir docker && cd doker

# docker-compose.yaml 다운로드
# airflow를 설치하기 전에 환경설정
# <여러 개의 컨테이너로부터 이루어진 서비스를 구축, 실행하는 순서를 자동으로 하여, 관리를 간단히하는 기능>
# linux에서는 docker container가 사용할 용량과 linux filesystem 권한 등이 필요
$ curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.1.2/docker-compose.yaml'
$ mkdir ./dags ./logs ./plugins
$ echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env

# airflw에 필요한 각종 database 큐 redis 등을 설치
$ docker-compose up airflow-init

# 상단 명령어를 통해 설치완료 후 airflow를 실행
# airflow 2.1.2 버전 기준 default username과 password는 둘 다 airflow이다.
$ docker-compose up

# Airflow의 버전과 폴더구성 및 시스템 정보, 툴 정보 및 경로, 설치한 패키지 버전
# 실행한 Airflow의 버전과 폴더구성, 경로를 보여줌
$ docker-compose run airflow-worker airflow info

# -L --location => 서버 응답이 HTTP 301이나 302 응답이 왔을 경우 redirect URL로 따라감
# -o --output FILE => curl은 remote에서 받아온 데이터를 기본적으로 콘솔에 출력
# o 옵션 뒤에 FILE을 적어주면 해당 FILE로 저장한다.
# -f --form <name=content> => 요청 헤더의 contentType은 multipart/form-data로 보냄
$ curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.1.2/airflow.sh'

# 권한에 추가설정
$ chmod +x airflow.sh

# 정보 확인 가능
$ ./airflow.sh info
# bash shell container에서 상호작용 가능
$ ./airflow.sh bash
# python contatiner에서 상호작용 가능
$ ./airflow.sh python

# 돌아가고있는 컨테이너 확인 / 옵션 -a 추가시 모든 컨테이너 확인
$ docker ps
```

## 최종점검

### DAG란?

DAG(Directed Acyclic Graph) 즉 비순환 그래프라고 하며 순환하는 사이클이 존재하지 않고, 일방향성만 가지고있다.

![DAG](https://github.com/alsrb3272/docker-airflow/blob/38d7645c2ea45c6b9f11c2b654d65cca674ccdb1/img/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7_20221228_040314.png)

**※ 분기 조건이 바뀔 시 전체 애플리케이션을 수정하고 배포해야하는 불편함을 가짐**

**그렇지만 Airflow에서는 실행할 순서에 따라 DAG에 배치하고 실행 주기와 분기 조건을 반영한다.**



### Airflow란?

ETL 자동화 파이프라인을 구성하는데 사용하며 WorkFlow를 정의하고 실행 가능한 플랫폼으로 반복된 작업을 자동화하기위해 사용된다.



### Airflow 아키텍처

![Airflow 아키텍처](https://github.com/alsrb3272/docker-airflow/blob/38d7645c2ea45c6b9f11c2b654d65cca674ccdb1/img/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7_20221228_035945.png)

**Scheduler** - Airflow의 DAG와 작업들을 모니터링하고 실행 순서와 상태 관리

**Worker** - Airflow의 작업을 실행하는 공간

**Metadata Database** - Airflow에서 실행할 작업에 관한 정보들을 저장

**WebServer** - Airflow의 User Interface 제공

**DAG Directory** - Airflow에서 실행할 작업들을 파이프라인 형태로 저장



즉, Airflow는 Scheduler가 DAG Directory의 작업을 가져와서 Worker에서 실행하는 형태



## Docker을 사용하는 경우 

- docker-compse 실행 시 Airflow 이미지가 각각 Scheduler, Worker, Webserver, flower 컨테이너로 실행
- 추가로 PostgreSQL과 redis 컨테이너도 필요
- PostgreSQL은 Airflow의 설정 정보, DAG과 작업들의 메타 정보등을 저장
- redis는 메시지 브로커로서 Scheduler에서 Worker로 메시지를 전달하는 역할을 수행




[Airflow Documentation](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html)

[Airflow설치참고 사이트](https://hkim-data.tistory.com/2)

[로컬 airflow사이트](http://localhost:8080)



