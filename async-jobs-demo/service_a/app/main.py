from __future__ import annotations

import json
import logging
import os
import threading
import time
import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Any

import pika
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s [service-a] %(message)s",
)
logger = logging.getLogger(__name__)

TASKS_QUEUE = "tasks"
RESULTS_QUEUE = "results"

# По условию задания состояние хранится в памяти процесса A, без БД.
JOBS: dict[str, dict[str, Any]] = {}
JOBS_LOCK = threading.Lock()
STOP_CONSUMER = threading.Event()


class CreateJobRequest(BaseModel):
    topic: str = Field(min_length=1, max_length=500, examples=["Подготовить отчёт"])


def rabbitmq_parameters() -> pika.ConnectionParameters:
    credentials = pika.PlainCredentials(
        os.getenv("RABBITMQ_USER", "appuser"),
        os.getenv("RABBITMQ_PASSWORD", "apppass"),
    )
    vhost = os.getenv("RABBITMQ_VHOST", "/")
    return pika.ConnectionParameters(
        host=os.getenv("RABBITMQ_HOST", "localhost"),
        port=int(os.getenv("RABBITMQ_PORT", "5672")),
        virtual_host=vhost,
        credentials=credentials,
        heartbeat=30,
        blocked_connection_timeout=10,
        socket_timeout=5,
        connection_attempts=3,
        retry_delay=1,
    )


def publish_task(job: dict[str, Any]) -> None:
    """Публикует задачу и ждёт publisher confirm от RabbitMQ."""
    connection = pika.BlockingConnection(rabbitmq_parameters())
    try:
        channel = connection.channel()
        channel.queue_declare(queue=TASKS_QUEUE, durable=True)
        channel.confirm_delivery()
        body = json.dumps(job, ensure_ascii=False).encode("utf-8")
        confirmed = channel.basic_publish(
            exchange="",
            routing_key=TASKS_QUEUE,
            body=body,
            properties=pika.BasicProperties(
                content_type="application/json",
                delivery_mode=2,  # persistent message
                message_id=job["id"],
                timestamp=int(time.time()),
            ),
            mandatory=True,
        )
        if not confirmed:
            raise RuntimeError("RabbitMQ did not confirm task publication")
    finally:
        if connection.is_open:
            connection.close()


def consume_results_forever() -> None:
    """Отдельный поток A слушает results и обновляет состояние задач."""
    while not STOP_CONSUMER.is_set():
        connection = None
        try:
            connection = pika.BlockingConnection(rabbitmq_parameters())
            channel = connection.channel()
            channel.queue_declare(queue=RESULTS_QUEUE, durable=True)
            channel.basic_qos(prefetch_count=10)

            def on_result(ch: pika.adapters.blocking_connection.BlockingChannel,
                          method: pika.spec.Basic.Deliver,
                          properties: pika.spec.BasicProperties,
                          body: bytes) -> None:
                try:
                    event = json.loads(body.decode("utf-8"))
                    job_id = event["id"]
                    with JOBS_LOCK:
                        job = JOBS.get(job_id)
                        if job is None:
                            # Состояние A — in-memory: после рестарта A старые job id
                            # могут отсутствовать. Не блокируем очередь неизвестным событием.
                            logger.warning("Received result for unknown job id=%s", job_id)
                        else:
                            # Идемпотентное обновление: повторный JobCompleted для того же
                            # id просто устанавливает то же конечное состояние.
                            job.update(
                                {
                                    "status": "DONE",
                                    "result": event["result"],
                                    "completedAt": event["completedAt"],
                                }
                            )
                    logger.info("JobCompleted received: id=%s", job_id)
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                except Exception:
                    logger.exception("Could not process result event; requeueing")
                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

            channel.basic_consume(
                queue=RESULTS_QUEUE,
                on_message_callback=on_result,
                auto_ack=False,
            )
            logger.info("Listening for completion events in queue '%s'", RESULTS_QUEUE)
            channel.start_consuming()
        except Exception:
            if not STOP_CONSUMER.is_set():
                logger.exception("Results consumer connection failed; retrying in 3 seconds")
                STOP_CONSUMER.wait(3)
        finally:
            if connection is not None and connection.is_open:
                try:
                    connection.close()
                except Exception:
                    logger.exception("Error while closing RabbitMQ connection")


@asynccontextmanager
async def lifespan(_: FastAPI):
    STOP_CONSUMER.clear()
    consumer_thread = threading.Thread(
        target=consume_results_forever,
        name="rabbitmq-results-consumer",
        daemon=True,
    )
    consumer_thread.start()
    logger.info("Service A started")
    try:
        yield
    finally:
        STOP_CONSUMER.set()
        logger.info("Service A is shutting down")


app = FastAPI(
    title="Async Jobs API",
    version="1.0.0",
    description="Приём задач и получение результатов через RabbitMQ.",
    lifespan=lifespan,
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/jobs", status_code=status.HTTP_202_ACCEPTED)
def create_job(request: CreateJobRequest) -> dict[str, str]:
    job_id = str(uuid.uuid4())
    job = {
        "id": job_id,
        "topic": request.topic,
        "createdAt": datetime.now(timezone.utc).isoformat(),
    }

    # Регистрируем задачу до публикации, чтобы не потерять быстрый ответ-событие.
    with JOBS_LOCK:
        JOBS[job_id] = {"id": job_id, "status": "ACCEPTED"}

    try:
        publish_task(job)
    except Exception as exc:
        with JOBS_LOCK:
            JOBS.pop(job_id, None)
        logger.exception("Failed to publish job id=%s", job_id)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Message broker is temporarily unavailable",
        ) from exc

    logger.info("Job accepted and published: id=%s", job_id)
    return {"id": job_id, "status": "ACCEPTED"}


@app.get("/jobs/{job_id}")
def get_job(job_id: str) -> dict[str, Any]:
    with JOBS_LOCK:
        job = JOBS.get(job_id)
        if job is None:
            raise HTTPException(status_code=404, detail="Job not found")
        return dict(job)
