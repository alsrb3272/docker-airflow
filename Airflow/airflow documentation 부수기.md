# Airflow Tutorial documentation

[Airflow Tutorial documentation](https://airflow.apache.org/docs/apache-airflow/stable/tutorial.html)

### 실행환경 버전 - Airflow 버전 : 2.1.2, Linux 버전 :   x86_64

[ㄴㄴ](https://velog.io/@clueless_coder/Airflow-%EC%97%84%EC%B2%AD-%EC%9E%90%EC%84%B8%ED%95%9C-%ED%8A%9C%ED%86%A0%EB%A6%AC%EC%96%BC-%EC%99%95%EC%B4%88%EC%8B%AC%EC%9E%90%EC%9A%A9)

### 기본 개념

예제 파이프라인 정의<Airflow에서 제공하는 airflow/example_dags/tutorial.py 전체코드> 

```python
# Importing Modules부분
from datetime import datetime, timedelta
from textwrap import dedent

# DAG를 정의하는데 필요한 Modules
# DAG - dag를 정의하기 위함
from airflow import DAG

# operators - 실제 연산(실행)을 하기 위해 필요한 operators들을 불러오기 위함
from airflow.operators.bash import BashOperator

with DAG(
    "tutorial",
    # Default Arguments부분
    # DAG를 만들거나 다른 task들을 만들 때, default로 제공하는 파라미터의 집합인 default_args를 선언하는 코드이다. operator를 선언할 때 변경 가능함.
    default_args={
        # depends_on_past (bool) - true일 경우, task instance가 순차적으로 실행
        # start_date에 대한 task instance 실행이 허용됨.
        "depends_on_past": False,
        
        # email(str or list[str]) -email 알람을 받는 메일 주소
        # 하나 혹은 여러 메일 주소를 입력 가능
        # 여러 메일인 경우, comma니 semi-colon을 통해 분리
        "email": ["airflow@example.com"],
        
        # email_on_failure (bool) - task가 실패할 경우 메일을 보내는 여부
        "email_on_failure": False,
        
        # email_on_retry(bool) - task가 재시도 될 경우 메일을 보내는 여부
        "email_on_retry": False,
        
        # retries(int) - task가 실패할 경우 재시도하는 횟수
        "retries": 1,
        
        # retry_delay(datetime.timedelta) - 재시도 사이의 delay 시간
        "retry_delay": timedelta(minutes=5),
        # 'queue': 'bash_queue',
        # 'pool': 'backfill',
        # 'priority_weight': 10,
        # 'end_date': datetime(2016, 1, 1),
        # 'wait_for_downstream': False,
        # 'sla': timedelta(hours=2),
        # 'execution_timeout': timedelta(seconds=300),
        # 'on_failure_callback': some_function,
        # 'on_success_callback': some_other_function,
        # 'on_retry_callback': another_function,
        # 'sla_miss_callback': yet_another_function,
        # 'trigger_rule': 'all_success'
    },
    # Instantiate a DAG
    # task를 DAG에 넣기 위해 DAG를 선언
    # description(str) - airflow 웹 서버에서 보여지는 내용
    description="A simple tutorial DAG",
    
    # schedule - 얼마나 자주 DAG를 run 할지 정하는 것
    schedule=timedelta(days=1),
    
    # start_date(datetime.datetime) - 스케쥴러가 backfill(?)을 시도하는 것
    # 아마 스케줄러가 DAG를 실행 queue에 집어 넣는 것을 말하는 것과 같음
    start_date=datetime(2021, 1, 1),
    
    # catchup - Scheduler는 DAG의 전체 lifetime을 확인하면서 실행되지 않은 DAG를 실행함.
    # 이렇게 정해진 시간에 실해되지 못한 DAG를 늦게라도 실행하는 것
    catchup=False,
    
    # tags: Optional[List[str]] = None)
    tags=["example"],
) as dag:

    # Tasks
    # Task는 operator를 인스턴스화 할때 생성
    # 인스턴스화 된 연산자를 Task라고 부름
    # task id는 task의 unique identifier이다.
    # BashOperator를 인스턴스화 할 때 받는 다양한 argument가 있을 수도 있다.
    # Task 우선순위 룰
    # 1. 명시적으로 전달된 arguments
    # 2. default_args dictonary에 있는 값
    # 3. 해당하는 operator에 있는 default value
    # ※ task에서는 반드시 task_id 와 owner 가 전달되어야 한다. 그렇지 않으면 exception error 가 발생한다.
    
    # t1같은경우
    # task_id: 작업을 구별하는 유일한 이름.
    # bash_command: 실행할 bash 명령어. 문자열 형태.
    t1 = BashOperator(
        task_id="print_date",
        bash_command="date",
    )

    # t2같은경우 
    # retries(int) - task가 실패할 경우 재시도하는 횟수 ("retries": 1,~)
    # depends_on_past (bool) - true일 경우, task instance가 순차적으로 실행
    # bash_command: 실행할 bash 명령어. 문자열 형태.
    # default_args에서 선언했던 retries를 operator's constructor에서 상속받아 3으로 오버라이드한다.
    t2 = BashOperator(
        task_id="sleep",
        depends_on_past=False,
        bash_command="sleep 5",
        retries=3,
    )
    
    # Adding DAG and Tasks documentation
    t1.doc_md = dedent(
        """\
    #### Task Documentation
    You can document your task using the attributes `doc_md` (markdown),
    `doc` (plain text), `doc_rst`, `doc_json`, `doc_yaml` which gets
    rendered in the UI's Task Instance Details page.
    ![img](http://montcs.bloomu.edu/~bobmon/Semesters/2012-01/491/import%20soul.png)
    **Image Credit:** Randall Munroe, [XKCD](https://xkcd.com/license.html)
    """
    )

    dag.doc_md = __doc__  # providing that you have a docstring at the beginning of the DAG; OR
    dag.doc_md = """
    This is a documentation placed anywhere
    """  # otherwise, type it like this
    
    # Templating with Jinja
    # Jinja template을 이용하여 파라미터를 전달.
    # Airflow에서는 Jinja라는 template의 장점을 활용하고 pipeline 작성자에게 기본 제공되는 매개변수 및 매크로 집합을 제공.
    # 그들 자체의 own parameters와 macros 그리고 templates를 제공
    
    # templated_command 변수에 {% %}의 블록 형태로 감싸진 내용은 구문의 시작과 끝
    # {{ds}}의 형태는 (today's "date stamp")를 의미
    # {{ macros.ds_add(ds, 7)}} macros라는 function을 불러오는 것
    # ds에 날짜를 7일 더 함.
    templated_command = dedent(
        """
    {% for i in range(5) %}
        echo "{{ ds }}"
        echo "{{ macros.ds_add(ds, 7)}}"
    {% endfor %}
    """
    )

    # bash_command에는 bash script file을 보낼 수 있는데, 예를 들어 bash_command='templated_command.sh'도 가능
    # sh파일의 경로는 기본적으로 현재 python script가 쓰여지는 곳으로 설정된다. 
    # template_searchpath 를 통해 경로 변경이 가능하다.
    t3 = BashOperator(
        task_id="templated",
        depends_on_past=False,
        bash_command=templated_command,
    )

    t1 >> [t2, t3]
```

[#2 Airflow Tutorial documentation 부수기](https://hkim-data.tistory.com/3)