# Real‑Time Fraud Detection 🔍💳

A minimal Python demo that streams payment transactions through **Apache Kafka**,  
flags suspicious activity on the fly, visualises it in a **Tkinter GUI** with a live bar‑chart,  
and stores every fraud alert in **MongoDB**.

<p align="center">
  <img src="docs/screenshot.gif" alt="Tkinter fraud‑detection GUI" width="700">
</p>

---

## Features
| Component | Tech | Purpose |
|-----------|------|---------|
| **Producer** | `producer.py` | Generates random transactions → Kafka topic `payments`. |
| **Consumer UI** | `consumer_gui.py` | Reads the stream, detects `amount > 3000`, logs alerts, updates matplotlib bar‑chart, inserts fraud docs into MongoDB. |
| **Alt. producers** | `webhook_producer.py`, `mysql_to_kafka.py` | Examples of feeding Kafka from a webhook or a MySQL table. |
| **Sample data** | `creditcard.csv` | Optional CSV you can adapt for bulk‑load tests. |
| **Docs** | `distributed.docx` | Design notes / step‑by‑step command list. |

---

## Quick Start

### 1  Prerequisites
| Tool | Tested Version |
|------|----------------|
| Python 3.10+ |
| Kafka 3.x (`kafka_2.13‑3.9.0`) |
| MongoDB 6.x |
| Java 8+ (for Spark examples) |

Python libs:
```bash
pip install kafka-python pymongo matplotlib numpy


> **Replace** `/opt/kafka` below if Kafka lives elsewhere on your machine.

<details>
<summary><b>Terminal 1 – ZooKeeper & Kafka</b></summary>

```bash
cd /opt/kafka
bin/zookeeper-server-start.sh config/zookeeper.properties &   # start ZooKeeper
sleep 5                                                       # give it 5 s
bin/kafka-server-start.sh config/server.properties            # start broker

python3 producer.py

python3 consumer_gui.py

mongosh
use fraud_detection
db.fraud_logs.find().pretty()


Add this under your **“Quick Start”** section (or wherever you like) and commit:

```bash
git add README.md
git commit -m "Add run commands snippet"
git push origin main


Folder Structure:
fraud-detection/
├── consumer_gui.py       # main Tkinter + Mongo consumer
├── producer.py           # random‑data Kafka producer
├── webhook_producer.py   # alt. producer (REST → Kafka)
├── mysql_to_kafka.py     # alt. producer (MySQL → Kafka)
├── creditcard.csv        # sample dataset
├── distributed.docx      # design notes / commands
└── Commands.txt


