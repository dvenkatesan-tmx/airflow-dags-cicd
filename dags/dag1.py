from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

# Function to be executed by PythonOperator
def print_hello():
    print("Hello, Airflow!")

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 11, 3),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag_tags = [
    'project:<PROJECT_NAME>',
    'client:<CLIENT>',
    'file_source:<FILE_SOURCE>',
    'file_landing_location:<FILE_LANDING_LOCATION>',
    'raw_database:<RAW_DATABASE>',
    'raw_table:<RAW_TABLE>',
    'normalized_database:<NORMALIZED_DATABASE>',
    'normalized_table:<NORMALIZED_TABLE>',
    'business_domain:<BUSINESS_DOMAIN>',
    'dq_checks:<DQ_CHECKS>',
    'dependency_child:<DAG_DEPENDENCY_CHILD>',
    'dependency_parent:<DAG_DEPENDENCY_PARENT>'
]

# Instantiate the DAG
dag = DAG(
    'sample_dag',
    default_args=default_args,
    description='A simple sample DAG',
    schedule_interval=timedelta(days=1),  # Runs once a day
    tags=dag_tags
)

# Define the tasks
start_task = DummyOperator(
    task_id='start',
    dag=dag,
)

hello_task = PythonOperator(
    task_id='print_hello',
    python_callable=print_hello,
    dag=dag,
)

end_task = DummyOperator(
    task_id='end',
    dag=dag,
)

# Set task dependencies
start_task >> hello_task >> end_task
