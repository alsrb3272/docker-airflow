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


## Part4. Airflow 설치 후 MYSQL 서버 및 DAG를 통한 크롤링 자동화 생성
## DOCKER - AIRFLOW - MYSQL < NAVER-API, Linux(wsl )>

**필요한 S/W**

- Window(wsl2)
- Docker
- Docker compose
- Mysql
- Linux
- Visual Studio
- Airflow

**리눅스에서 Docker를 이용하여 Local에서 Airflow 구축 후 Naver api를 이용하여 Mysql로 데이터를 옮기는 실습을 할 것이다.**

##### 참고로 airflow.cfg 폴더위치 바꿀것

##### dags_folder = /home/mink/airflow/dags

##### base_log_folder = /home/mink/airflow/logs

-------------------------

## 실습 전 세팅

### 1. VSC 설치

간략설명

1. Visual Studio를 먼저 설치 

   [Visual Studio Code 설치 사이트](https://visualstudio.microsoft.com/ko/downloads/)

2. Linux에서 airflow 폴더로 이동 (cd /airflow)

3. 비쥬얼 스튜디오 실행 명령어 입력(code .) ![vsc](img/image-20230118121738214.png)

**설치하는 이유 : 리눅스에선 vi로 코드를 편집할 수 있지만 내가 불편해서 vsc를 깔고 code로 보게되면 편해지고 코드를 보기 편하다..(특히 자동입력최고..★)**

----------------------

### 2. 샘플 DAG들 정리

docker와 airflow를 설치했다면 airflow 폴더에 docker-compose.yaml을 들어가자.

(code docker-compose.yaml 실행)

<img src="img/image-20230118122512522.png" alt="image-20230118122512522" style="zoom: 50%;" />

들어가게 된다면 `AIRFLOW__CORE__LOAD_EXAMPLES: 'true'`라고 되어있어서
true -> false로 설정하고 저장 후 airflow를 다시 실행하면 없어져있을 것이다. 

![image-20230118122721804](img/image-20230118122721804.png)

**하는 이유 : 기존에 있던 dag들을 확인해봤다면 없애고 내가 테스트 및 실습 할 dag들로만 구성해야 보기 편하다.**

----------------

### 3.  MYSQL 및 Dbeaver 설치

**참고 : 검색창에 mysql를 쳐서 MYSQL SHELL이 나온다면 이 과정은 넘겨도 된다.**

<img src="img/image-20230118123259875.png" alt="image-20230118123259875" style="zoom:50%;" />

간략설명

1. mysql 설치

   [MYSQL 설치 사이트](https://dev.mysql.com/downloads/installer/)

2. 다운로드 가이드 사이트를 보면서 설치

   [다운로드 가이드](https://hongong.hanbit.co.kr/mysql-%EB%8B%A4%EC%9A%B4%EB%A1%9C%EB%93%9C-%EB%B0%8F-%EC%84%A4%EC%B9%98%ED%95%98%EA%B8%B0mysql-community-8-0/)

3. Dbeaver 설치하기(가이드 참고)

   [다운로드 가이드](https://computer-science-student.tistory.com/505)

4. 환경변수 설정

   1. mysql

      1. 시스템 속성 -> 환경 변수 -> 시스템 변수 -> 변수 **Path** 편집 -> 새로 만들기 -> C:\Program Files\MySQL\MySQL Server 8.0\bin 입력(각자 다른 폴더에 있을 수도 있으니 확인바람.)

      2. cmd 창을 열어 mysql -u [계정] -p [비밀번호] 입력

      3. 접속 완료

         ![image-20230118132258521](img/image-20230118132258521.png)

   2. dbeaver 

      1. dbeaver를 열어 새 데이터베이스 연결 -> mysql -> settings부분에서 username과 password 입력 -> test connection 클릭 -> 하단 이미지처럼 완성됐다면 완료버튼 클릭  

         ![image-20230118140949369](img/image-20230118140949369.png)

      2. script창을 새로 만들어 `select * from mysql.user;` 입력하고 mysql에 입력된 user리스트들을 한눈에 보여준다.

      3. 외부에서 접속할 수 있도록 계정을 먼저 설정해준다.

         `create user '[사용자명]'@'%' identified by '[비밀번호]';`

         - `@'localhost'` : 로컬에서만 접근 가능
         - `@'%'` : 어떤 client에서든 접근 가능
         - `@'[특정 IP]` : 특정 IP에서만 접근 가능
         - `223.101.%` : `223.101.X.X` 대역의 IP에서 접근 가능
         - `223.101.13.21` : `223.101.13.21` IP에서만 접근 가능

      4. 해당 계정에 권한 부여

         `grant all privileges on [DB].[Table] to '사용자명'@'%';`

         **대상 객체**

         - 모든 DB와 Table을 대상으로 할 경우 `*.*` 입력
         - `test` DB의 모든 Table을 대상으로 할 경우 : `test.*`
         - `test` DB의 `abc` Table을 대상으로 할 경우 : `test.abc`

         **DML 권한**

         - 모든 DML 권한을 주기 위해서는 `all` 입력
         - `select` 권한만 줄 경우
           `grant select privileges ~`
         - `select`, `insert`, `update` 권한을 줄 경우
           `grant select, insert, update privileges ~`

      5. 변경된 내용 반영

         `flush privileges`

      6. 다시 user리스트를 조회하는 명령어를 사용 및 cmd로 mysql에 새로운 계정 접속 확인

   -------------

   ### 4.  MYSQL과  Airflow 연결 < test과정>

   **aiirflow와 연결하려면 Mysql local에서 사용하고 있는 Ip를 알아야함.**

   1. 새 cmd창에서 ipconfig입력 주소 확인하기.<img src="img/image-20230118140555669.png" alt="image-20230118140555669" style="zoom:67%;" />

   2.  localhost:8080(airflow)에서 Admin -> connections -> +버튼 클릭![image-20230118143103734](img/image-20230118143103734.png)

   3. connection에 지금까지 설정해둔 내용들 입력 후 test해보고 저장<img src="img/image-20230118144800884.png" alt="image-20230118144800884" style="zoom:50%;" />

   4. DAG 작성

      ```python
      # import할 패키지들 기존에 제공되는 패키지는 1번이고 2번은 새로 설치해야하는 패키지들
      # 1 
      from datetime import datetime, timedelta
      from email.policy import default
      from textwrap import dedent
      
      # 2(MysqlOperator설치)
      from airflow import DAG
      from airflow.providers.mysql.operators.mysql import MySqlOperator
      
      # default_args은 dag를 실행할때 횟수나 빈도를 설정하는 변수
      default_args = {
          'depends_on_past': False,
          'retires': 1,
          'retry_delay': timedelta(minutes=5)
      }
      
      # employees 테이블 생성구문 변수
      sql_create_table = """
          CREATE TABLE `employees` (
              `employeeNumber` int(11) NOT NULL,
              `lastName` varchar(50) NOT NULL,
              `firstName` varchar(50) NOT NULL,
              `extension` varchar(10) NOT NULL,
              `email` varchar(100) NOT NULL,
              `officeCode` varchar(10) NOT NULL,
              `reportsTo` int(11) DEFAULT NULL,
              `jobTitle` varchar(50) NOT NULL,
          PRIMARY KEY (`employeeNumber`)
          );
      """
      
      # employees 테이블 데이터 추가구문 변수
      sql_insert_data = """
          insert into `employees`(`employeeNumber`,`lastName`,`firstName`,`extension`,`email`,`officeCode`,`reportsTo`,`jobTitle`) values
           (1002,'Murphy','Diane','x5800','dmurphy@classicmodelcars.com','1',NULL,'President'),
              (1056,'Patterson','Mary','x4611','mpatterso@classicmodelcars.com','1',1002,'VP Sales'),
              (1076,'Firrelli','Jeff','x9273','jfirrelli@classicmodelcars.com','1',1002,'VP Marketing'),
              (1088,'Patterson','William','x4871','wpatterson@classicmodelcars.com','6',1056,'Sales Manager (APAC)'),
              (1102,'Bondur','Gerard','x5408','gbondur@classicmodelcars.com','4',1056,'Sale Manager (EMEA)'),
              (1143,'Bow','Anthony','x5428','abow@classicmodelcars.com','1',1056,'Sales Manager (NA)'),
              (1165,'Jennings','Leslie','x3291','ljennings@classicmodelcars.com','1',1143,'Sales Rep'),
              (1166,'Thompson','Leslie','x4065','lthompson@classicmodelcars.com','1',1143,'Sales Rep'),
              (1188,'Firrelli','Julie','x2173','jfirrelli@classicmodelcars.com','2',1143,'Sales Rep'),
              (1216,'Patterson','Steve','x4334','spatterson@classicmodelcars.com','2',1143,'Sales Rep'),
              (1286,'Tseng','Foon Yue','x2248','ftseng@classicmodelcars.com','3',1143,'Sales Rep'),
              (1323,'Vanauf','George','x4102','gvanauf@classicmodelcars.com','3',1143,'Sales Rep'),
              (1337,'Bondur','Loui','x6493','lbondur@classicmodelcars.com','4',1102,'Sales Rep'),
              (1370,'Hernandez','Gerard','x2028','ghernande@classicmodelcars.com','4',1102,'Sales Rep'),
              (1401,'Castillo','Pamela','x2759','pcastillo@classicmodelcars.com','4',1102,'Sales Rep'),
              (1501,'Bott','Larry','x2311','lbott@classicmodelcars.com','7',1102,'Sales Rep'),
              (1504,'Jones','Barry','x102','bjones@classicmodelcars.com','7',1102,'Sales Rep'),
              (1611,'Fixter','Andy','x101','afixter@classicmodelcars.com','6',1088,'Sales Rep'),
              (1612,'Marsh','Peter','x102','pmarsh@classicmodelcars.com','6',1088,'Sales Rep'),
              (1619,'King','Tom','x103','tking@classicmodelcars.com','6',1088,'Sales Rep'),
              (1621,'Nishi','Mami','x101','mnishi@classicmodelcars.com','5',1056,'Sales Rep'),
              (1625,'Kato','Yoshimi','x102','ykato@classicmodelcars.com','5',1621,'Sales Rep'),
              (1702,'Gerard','Martin','x2312','mgerard@classicmodelcars.com','4',1102,'Sales Rep');
      """
      
      # DAG 설정
      with DAG(
          'connect_to_local_mysql',
          default_args = default_args,
          description = """
              1) create 'employees' table in local mysqld
              2) insert data to 'employees' table
          """,
          schedule_interval = '@daily',
          start_date = datetime(2022, 1, 1),
          catchup = False,
          tags = ['mysql', 'local', 'test', 'employees']
      ) as dag:
          t1 = MySqlOperator(
              task_id="create_employees_table",
              mysql_conn_id="mysql_local_test",
              sql=sql_create_table,
          )
      
          t2 = MySqlOperator(
              task_id="insert_employees_data",
              mysql_conn_id="mysql_local_test",
              sql=sql_insert_data
          )
      
      
      # 순서
          t1 >> t2
      
      
      ```

   5. DAG를 실행시켜 파일이 잘 되었는지 확인

      ```bash
      mink@PMK-HS1HH67:~/airflow/dags$ python3 connect_to_local_mysql.py
      ```

   6. 실행이됐다면 airflow에 들어가서 dag 실행한 후 결과가 하단처럼 나와야함<안 됐을 시 오류난 곳 확인하기.>

      ![image-20230118151157434](img/image-20230118151157434.png)

      - **오류는 다음과 같은 곳에서 확인가능** 

      Details -> failed -> log url 확인하면 어느 부분에서 에러가 났는 지 확인 가능.

      ![image-20230118151421956](img/image-20230118151421956.png)

      ![image-20230118151843056](img/image-20230118151843056.png)

   7. dbeaver로 데이터 들어갔는 지 확인

      ![image-20230118152011306](img/image-20230118152011306.png)

------------

### 5.  Naver api를 이용한 자동 크롤링 및 db 생성, 데이터 추가

1. 네이버 api를 등록

   1. [NAVER DEVELOPERS](https://developers.naver.com/main/) 접속 후 로그인

   2. 애플리케이션 등록

      ![image-20230118161745768](img/image-20230118161745768.png)

   3. 등록하게되면 Client ID, Client Secret을 발급받게 됌.

      ![image-20230118161930423](img/image-20230118161930423.png)

   4. pipeline과 preprocessing 두 부분으로 나눠서 py로 생성

      1. ~/airflow/dags 폴더 안에 naver_search_pipeline.py 파일을 만든다.(vi로 하든 code로 들어가서 생성하든 상관없다.)

         ```python
         # 필요한 모듈 Import
         from datetime import datetime
         import json
         import pandas as pd
         from airflow import DAG
         from pandas import json_normalize
         from naver_preprocess import abc
         
         # 사용할 Operator Import
         from airflow.providers.http.sensors.http import HttpSensor
         from airflow.providers.http.operators.http import SimpleHttpOperator
         from airflow.operators.python import PythonOperator
         from airflow.operators.bash import BashOperator
         from airflow.providers.mysql.operators.mysql import MySqlOperator
         
         
         # 디폴트 설정
         default_args = {
             "start_date": datetime(2023, 1, 1) # 2023년 1월 1일 부터 태그 시작-->
             # 현재는 23년 1월이므로 태그를 실행하면 무조건 한번은 돌아갈 것
         }
         
         
         NAVER_CLI_ID = "<발급받은 번호입력>"
         NAVER_CLI_SECRET = "<발급받은 번호입력>"
         
         # naver_search_result 테이블 생성 쿼리
         sql_create_table="""
                 CREATE TABLE `naver_search_result`(
                 `title` TEXT,
                 `address` TEXT,
                 `category` TEXT,
                 `description` TEXT,
                 `link` TEXT
                 );
             """
         
         
         # DAG를 설정
         with DAG(
             dag_id="naver-search-pipeline",
             # 스케쥴을 매일 갱신
             schedule_interval="@daily",
             default_args=default_args,
             #태그는 원하는대로
             tags=["naver", "search", "local", "api", "pipeline"],
             # catchup을 True로 하면, start_date부터 현재까지 못돌린 날들을 채운다.
             catchup=False) as dag:
         
         	# mysqloperator - mysql로 테이블을 생성
             create_naver_table = MySqlOperator(
                 task_id = "create_naver_table",
                 mysql_conn_id = "mysql_local_test",
                 sql=sql_create_table,
             )
         	# HttpSensor - 데이터 가져오는 것이 가능한지 확인하기
             is_api_available = HttpSensor(
                 task_id = "is_api_available",
                 http_conn_id="naver_search_api",
                 endpoint="v1/search/local.json",
             
             headers={
                 "X-Naver-Client-Id" : f"{NAVER_CLI_ID}",
                 "X-Naver-Client-Secret" : f"{NAVER_CLI_SECRET}",
             },
             request_params={
                 "query" : "김치찌개",
                 "display" : 5
             },
             response_check=lambda response: response.json()
             )
             
             # SimpleHttpOperator - 크롤링한 데이터를 json형태로 설정
             crawl_naver = SimpleHttpOperator(
                 task_id='crawl_naver',
                 http_conn_id='naver_search_api',
                 endpoint="v1/search/local.json",
                 
                 headers={
                     "X-Naver-Client-Id" : f"{NAVER_CLI_ID}",
                     "X-Naver-Client-Secret" : f"{NAVER_CLI_SECRET}",
                 },
                 data={
                     "query":"김치찌개",
                     "display" : 5
                 },
                 method="GET",
                 response_filter=lambda res : json.loads(res.text),
                 log_response=True     
             )
         
             # PythonOperator - 크롤링된 가공되지않은 데이터 전처리
             preprocess_result = PythonOperator(
                     task_id="preprocess_result",
                      python_callable=abc)
         
         
         
             def _success():
                 print("네이버 검색 DAG 완료")
              # 대그 완료 출력
             print_complete = PythonOperator(
                     task_id="print_complete",
                     python_callable=_success
                     )
         
         
             # 파이프라인 구성하기
             create_naver_table >> is_api_available >> crawl_naver >> preprocess_result >> print_complete
         ```

      2. ~/airflow/dags 폴더 안에 naver_preprocess.py 파일을 만든다.(vi로 하든 code로 들어가서 생성하든 상관없다.)

         ```python
         from pandas import json_normalize
         from airflow.operators.python import PythonOperator
         import pandas as pd
         import sqlalchemy
         from airflow import DAG
         
         __all__ = ["abc"]
         
         def abc(ti):
             # ti(task instance) - dag 내의 task의 정보를 얻어 낼 수 있는 객체
         
             # xcom(cross communication) - Operator와 Operator 사이에 데이터를 전달 할 수 있게끔 하는 도구
             naver_search = ti.xcom_pull(task_ids=["crawl_naver"])
         
             # xcom을 이용해 가지고 온 결과가 없는 경우
             if not len(naver_search):
                 raise ValueError("검색 결과 없음")
         
         
             # for i in naver_search: naver_data = i['items'] <- 이 방식으로 해도 dictionary형태인 item들을
             # 제대로된 배치로 저장함.
             items = naver_search[0]['items']
         
             processed_items = pd.json_normalize([
                 {"title": i["title"],
                 "address" : i["address"],
                 "category": i["category"],
                 "description": i["description"],
                 "link": i["link"]} for i in items
             ])
             
             # db info
             user_name = 'mysql외부계정'
             pass_my = '비밀번호'
             host_my = 'airflow connection에 사용된 포트(ex.172.16.0.1:3306)'
             db_name = '데이터베이스 이름'
         
             # to_sql, mysql connector
             connection= sqlalchemy.create_engine(f"mysql+mysqlconnector://{user_name}:{pass_my}@{host_my}/{db_name}")
             table_name = 'naver_search_result'
             processed_items.to_sql(name      = table_name
                                         ,con       = connection 
                                         ,index     = False
                                         ,if_exists = 'append')
             
         ```

      3. 결과가 이렇게 나와야함

      ![image-20230118170201237](img/image-20230118170201237.png)

      

      



[기초 셋팅](https://velog.io/@jskim/Airflow-%EA%B0%9C%EB%B0%9C%ED%99%98%EA%B2%BD-%EC%85%8B%ED%8C%85%ED%95%98%EA%B8%B0-on-Docker)

[mysql로 크롤링 데이터 저장](https://pbj0812.tistory.com/390)

[네이버 API를 활용하여 크롤링 참고](https://velog.io/@clueless_coder/Airflow-%EC%97%84%EC%B2%AD-%EC%9E%90%EC%84%B8%ED%95%9C-%ED%8A%9C%ED%86%A0%EB%A6%AC%EC%96%BC-%EC%99%95%EC%B4%88%EC%8B%AC%EC%9E%90%EC%9A%A9)

[window상에 mysql 설치 및 환경설정](https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=jin93hj&logNo=221118160512)

[MYSQL LOCAL 오픈 및 테스트](https://velog.io/@jskim/Airflow-Pipeline-%EB%A7%8C%EB%93%A4%EA%B8%B0-MySQL-Query-%ED%95%98%EA%B8%B0)





- 에러 모음집

```bash
# 모듈이 제대로 설치가 안 되서 해당 에러 발생
# setup 도구들을 업그레이드
$ pip install --upgrade setuptools 
# mysql설치 시 필요한 의존성 라이브러리들을 다시 설치
$ sudo apt-get install python3-dev default-libmysqlclient-dev build-essential 
# Debian / Ubuntu

```

[apache-airflow-providers-mysql 설치 에러 시 참고_1](https://mingzz1.github.io/error/python/2020/01/20/Error-pip_install.html/)

[참고_2](https://stackoverflow.com/questions/61063676/command-errored-out-with-exit-status-1-python-setup-py-egg-info-check-the-logs)

[참고_3](https://velog.io/@sandartchip/Command-errored-out-with-exit-status-1-python-setup.py-egginfo-Check-the-logs-for-full-command-output)
