# Overview

This project is based on the proposed project from the book [Data Engineering with Python](https://www.amazon.com/Data-Engineering-Python-datasets-pipelines/dp/183921418X/ref=sr_1_1_sspa), and adds its own flair by containerizing the services with Docker. Using Apache Airflow, PostgreSQL, ElasticSearch, Redis, and Kibana, a data flow is established to stream data from the [SeeClickFix](http://dev.seeclickfix.com/) API so that it can be visualized and analyzed. 

# Objective

The purpose of this project is simply to gain familiarity with the various tools - especially Apache Airflow and Docker - and their role in creating data pipelines. It's unlikely that the approach taken in this project is the ideal approach, so feedback is always welcomed and encouraged.

# Usage

In order to get this to run on your local machine, clone the repo and run the following two commands:

```
docker compose up airflow-init
docker compose up
```

For more information, you can read the [official docs](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html) on getting Airflow to run on Docker. Once that's up, you can navigate to `localhost:8080` to see the Airflow dashboard or `localhost:5601` to see the Kibana dashboard.

# Details

The aforementioned book is really the best place to go to see how all of this came together, but if you're curious to hear my thoughts on it, or read about some of the places where I deviated or encountered obstacles, you can read the blog post I put together about this project [here](https://tibblesnbits.com) (Blog post is currently unwritten, but will be coming soon).