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


    # for i in naver_search:
    #     naver_data = i['items']
    items = naver_search[0]['items']

    processed_items = pd.json_normalize([
        {"title": i["title"],
        "address" : i["address"],
        "category": i["category"],
        "description": i["description"],
        "link": i["link"]} for i in items
    ])
    
    # db info
    user_name = 'mink'
    pass_my = '1234'
    host_my = '192.168.0.1:3306'
    db_name = 'test'

    # to_sql
    connection= sqlalchemy.create_engine(f"mysql+mysqlconnector://{user_name}:{pass_my}@{host_my}/{db_name}")
    table_name = 'naver_search_result'
    processed_items.to_sql(name      = table_name
                                ,con       = connection
                                ,index     = False
                                ,if_exists = 'append')
    

   # processed_items.to_csv("/opt/airflow/dags/naver_processed_result.csv", index=None, header=False)
