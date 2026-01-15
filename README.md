# 📊 Real-Time Big Data ETL Pipeline on GCP (Final Project)

## Project Overview

This project implements an **end-to-end real-time Big Data ETL pipeline** using **Google Cloud Platform (GCP)**. The pipeline continuously collects live news articles related to **Donald Trump** from **NewsAPI**, streams the data through **Apache Kafka**, processes it using **Apache Spark Structured Streaming**, and stores aggregated results in **HDFS**, which are then queried using **Apache Hive**.

This implementation strictly follows the workflow and components described in the **Final Project PDF** fileciteturn0file0 and was developed as part of a **Big Data Engineering Final Project**.

---

## 🏗️ System Architecture

**Data Flow:**

```
NewsAPI → Kafka Producer → Kafka Topic (DonaldTrump) → Spark Structured Streaming → HDFS → Hive External Table
```

* **Source**: NewsAPI (keyword: "Donald Trump")
* **Streaming Platform**: Apache Kafka
* **Processing Engine**: Apache Spark Structured Streaming
* **Storage**: HDFS
* **Analytics Layer**: Apache Hive

---

## 🔄 ETL Process Description

### 1️⃣ Data Extraction (NewsAPI)

* A NewsAPI token is generated and stored securely using environment variables
* News articles mentioning **Donald Trump** are fetched continuously
* Extracted fields include source, author, description, image URL, content, title, URL, and published timestamp
* A unique **article_id** is generated using MD5 hashing to avoid duplicate records

### 2️⃣ Data Ingestion (Apache Kafka)

* Zookeeper and Kafka broker are started
* A Kafka topic named **DonaldTrump** is created
* The Kafka producer publishes cleaned article data as pipe-separated strings
* Duplicate articles are filtered at the producer level

### 3️⃣ Data Processing (Spark Structured Streaming)

* Spark consumes streaming data from the Kafka topic
* Incoming messages are parsed and split into structured columns
* A processing timestamp is added
* Data is aggregated using:

  * **1-minute time windows**
  * **Source-wise article counts**
* Watermarking is applied to handle late-arriving data

### 4️⃣ Data Storage & Loading

* Aggregated streaming output is written to **HDFS** in CSV format
* Data is checkpointed for fault tolerance
* An **external Hive table** is created on top of the HDFS directory

---

## 🗄️ Hive Table Definition

```sql
CREATE EXTERNAL TABLE news_aggregated (
  window_start TIMESTAMP,
  window_end TIMESTAMP,
  source STRING,
  count INT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/BigData/news_data';
```

---

## 📈 Sample Hive Query

```sql
SELECT * FROM news_aggregated LIMIT 10;
```

This enables SQL-based analysis of real-time aggregated news data.

---

## ▶️ Execution Steps

1. Get NewsAPI token
2. Start Zookeeper and Kafka broker
3. Create Kafka topic **DonaldTrump**
4. Run Kafka Producer (NewsAPI ingestion)
5. Start Spark Structured Streaming consumer
6. Verify data saved in HDFS
7. Create Hive external table
8. Query data using HiveQL

---

## 📁 Project Components

* Kafka Producer (Python – NewsAPI ingestion)
* Spark Structured Streaming Consumer
* HDFS Storage
* Hive External Table & Queries

---

## ✅ Key Outcomes

* Real-time streaming ETL pipeline
* Kafka-based ingestion with deduplication
* Windowed aggregation using Spark Structured Streaming
* Scalable storage in HDFS
* SQL analytics using Hive

---

## 🎓 Academic Context

This project was completed as a **Big Data Final Project** under the guidance of **Professor Saber Amini**, demonstrating practical application of streaming data pipelines and distributed data processing concepts.

---

## 👩‍💻 Author (GitHub Profile Owner)

**Abinaya Kalaiarasan**

---

## 📜 License

This project is intended for academic and learning purposes only.
