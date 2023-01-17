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

NAVER_CLI_ID = "MU4487CE1mRkX3THqT42"
NAVER_CLI_SECRET = "tUmVdjRQ3z"


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
    # crontab 표현 사용 가능
    schedule_interval="@daily",
    default_args=default_args,
    #태그는 원하는대로
    tags=["naver", "search", "local", "api", "pipeline"],
    # catchup을 True로 하면, start_date부터 현재까지 못돌린 날들을 채운다.
    catchup=False) as dag:


    create_naver_table = MySqlOperator(
        task_id = "create_naver_table",
        mysql_conn_id = "mysql_local_test",
        sql=sql_create_table,
    )

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

    preprocess_result = PythonOperator(
            task_id="preprocess_result",
             python_callable=abc)

    # csv 파일로 저장된 것을 테이블에 저장
    # store_result = BashOperator(
    #     task_id="store_naver",
    #     bash_command='echo -e ".separator ","\n.import /opt/airflow/dags/naver_processed_result.csv naver_search_result" | sqlite3 /opt/airflow/airflow.db'
    # )

    def _success():
        print("네이버 검색 DAG 완료")
     # 대그 완료 출력
    print_complete = PythonOperator(
            task_id="print_complete",
            python_callable=_success
            )


    # insert_naver_table = MySqlOperator(
    #     task_id = "insert_naver_table",
    #     mysql_conn_id = "mysql_local_test",
    #     sql=,
    # )            

    # 파이프라인 구성하기
    # create_naver_table >> is_api_available >> crawl_naver >> preprocess_result >> store_result >> print_complete
    create_naver_table >> is_api_available >> crawl_naver >> preprocess_result >> print_complete
