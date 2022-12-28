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
