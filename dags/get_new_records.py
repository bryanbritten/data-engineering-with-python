import datetime as dt
from datetime import timedelta
import requests
import time
from elasticsearch import Elasticsearch, helpers
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

default_args = {
    "owner": "Data Engineer",
    "start_date": dt.datetime.today(),
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
}

def get_timestamps():
    today = dt.datetime.today()
    month = str(today.month).rjust(2, "0")
    day = str(today.day - 1).rjust(2, "0")
    timestamps = {
        "after": f'{today.year}-{month}-{day}T00:00:00',
        "before": f'{today.strftime("%Y-%m-%d")}T00:00:00'
    }
    return timestamps

def build_url(page):
    base_url = "https://seeclickfix.com/api/v2/issues"
    timestamps = get_timestamps()
    params = {
        "place_url": "new-york",
        "per_page": 100,
        "page": page,
        "updated_at_after": timestamps["after"],
        "updated_at_before": timestamps["before"]
    }
    return f"{base_url}?{'&'.join([f'{k}={v}' for k,v in params.items()])}"

def get_results(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def add_additional_fields(record):
    record["coords"] = f'{str(record["lat"])},{str(record["lng"])}'
    record["created_date"] = record["created_at"].split("T")[0]
    record["created_time"] = record["created_at"].split("T")[1]
    record["updated_date"] = record["updated_at"].split("T")[0]
    record["updated_time"] = record["updated_at"].split("T")[1]
    return record

def write_to_elasticsearch(es, issues):
    data = [
        {
            "_op_type": "update",
            "_index": "scf",
            "_type": "issue",
            "_id": issue["id"],
            "doc": issue,
            "doc_as_upsert":True
        }
        for issue in issues
    ]
    result = helpers.bulk(es, data, index="scf", doc_type="issue")
    # fail the pipeline if all records were not uploaded
    assert result[0] == len(issues)
    return None

def ETL():
    es = Elasticsearch("http://es01:9200")
    if not es.indices.exists(index="scf"):
        es.indices.create(index="scf")
    page = 1

    while page is not None:
        url = build_url(page=page)
        results = get_results(url)
        issues = results["issues"]
        issues = list(map(add_additional_fields, issues))
        write_to_elasticsearch(es, issues)

        # exit condition if there are no more pages left
        page = results["metadata"]["pagination"]["next_page"]
    return None

with DAG(
    "get_new_records", 
    default_args=default_args, 
    schedule_interval="@daily"
) as dag:
    main_task = PythonOperator(
        task_id = 'fetch_records',
        python_callable = ETL
    )

    main_task