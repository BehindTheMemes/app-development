from __future__ import annotations

import json
import logging
import os
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pika

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s [service-b] %(message)s",
)
logger = logging.getLogger(__name__)

TASKS_QUEUE = "tasks"
RESULTS_QUEUE = "results"
PROCESSING_DELAY = float(os.getenv("PROCESSING_DELAY_SECONDS", "2.5"))
CACHE_PATH = Path(os.getenv("PROCESSED_CACHE_PATH", "/data/processed_jobs.json"))
CACHE_LOCK = threading.Lock()


def rabbitmq_parameters() -> pika.ConnectionParameters:
    credentials = pika.PlainCredentials(
        os.getenv("RABBITMQ_USER", "appuser"),
        os.getenv("RABBITMQ_PASSWORD", "apppass"),
    )
    return pika.ConnectionParameters(
        host=os.getenv("RABBITMQ_HOST", "localhost"),
        port=int(os.getenv("RABBITMQ_PORT", "5672")),
        virtual_host=os.getenv("RABBITMQ_VHOST", "/"),
        credentials=credentials,
        heartbeat=30,
        blocked_connection_timeout=10,
        socket_timeout=5,
        connection_attempts=10,
        retry_delay=2,
    )


def load_cached_event(job_id: str) -> dict[str, Any] | None:
    with CACHE_LOCK:
        if not CACHE_PATH.exists():
            return None
        try:
            cache = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
            return cache.get(job_id)
        except (json.JSONDecodeError, OSError):
            logger.exception("Could not read idempotency cache")
            raise


def save_cached_event(job_id: str, event: dict[str, Any]) -> None:
    """Атомарно сохраняет результат до публикации и ack исходной задачи."""
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with CACHE_LOCK:
        cache: dict[str, Any] = {}
        if CACHE_PATH.exists():
            cache = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
        cache[job_id] = event
        temporary_path = CACHE_PATH.with_suffix(".tmp")
        temporary_path.write_text(
            json.dumps(cache, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        os.replace(temporary_path, CACHE_PATH)


def process_job(job: dict[str, Any]) -> dict[str, Any]:
    job_id = job["id"]
    topic = job["topic"]
    logger.info("Started processing job id=%s topic=%r", job_id, topic)
    time.sleep(PROCESSING_DELAY)  # Имитация долгой обработки: 2–3 секунды.
    event = {
        "event": "JobCompleted",
        "id": job_id,
        "result": f"Задача «{topic}» выполнена",
        "completedAt": datetime.now(timezone.utc).isoformat(),
    }
    logger.info("Finished processing job id=%s", job_id)
    return event


def publish_result(channel: pika.adapters.blocking_connection.BlockingChannel,
                   event: dict[str, Any]) -> None:
    confirmed = channel.basic_publish(
        exchange="",
        routing_key=RESULTS_QUEUE,
        body=json.dumps(event, ensure_ascii=False).encode("utf-8"),
        properties=pika.BasicProperties(
            content_type="application/json",
            delivery_mode=2,
            message_id=event["id"],
            type="JobCompleted",
        ),
        mandatory=True,
    )
    if not confirmed:
        raise RuntimeError("RabbitMQ did not confirm result publication")


def main() -> None:
    while True:
        connection = None
        try:
            connection = pika.BlockingConnection(rabbitmq_parameters())
            channel = connection.channel()
            channel.queue_declare(queue=TASKS_QUEUE, durable=True)
            channel.queue_declare(queue=RESULTS_QUEUE, durable=True)
            channel.basic_qos(prefetch_count=1)
            channel.confirm_delivery()

            def on_task(ch: pika.adapters.blocking_connection.BlockingChannel,
                        method: pika.spec.Basic.Deliver,
                        properties: pika.spec.BasicProperties,
                        body: bytes) -> None:
                try:
                    job = json.loads(body.decode("utf-8"))
                    job_id = job["id"]

                    # Если задача уже обрабатывалась, используем сохранённое событие.
                    # Это позволяет не повторять долгую обработку после redelivery/restart.
                    event = load_cached_event(job_id)
                    if event is None:
                        event = process_job(job)
                        # Кэшируем до публикации: повторная доставка получит тот же event.
                        save_cached_event(job_id, event)
                    else:
                        logger.warning(
                            "Duplicate delivery detected for id=%s; reusing cached result",
                            job_id,
                        )

                    # Сначала подтверждаем публикацию результата, только потом ack задачи.
                    publish_result(ch, event)
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                    logger.info("Task acked: id=%s; JobCompleted published", job_id)
                except Exception:
                    logger.exception("Task failed; message will be requeued")
                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

            channel.basic_consume(
                queue=TASKS_QUEUE,
                on_message_callback=on_task,
                auto_ack=False,
            )
            logger.info(
                "Worker is listening on '%s'; result queue is '%s'",
                TASKS_QUEUE,
                RESULTS_QUEUE,
            )
            channel.start_consuming()
        except KeyboardInterrupt:
            logger.info("Worker stopped")
            break
        except Exception:
            logger.exception("Worker connection failed; retrying in 3 seconds")
            time.sleep(3)
        finally:
            if connection is not None and connection.is_open:
                try:
                    connection.close()
                except Exception:
                    logger.exception("Error while closing RabbitMQ connection")


if __name__ == "__main__":
    main()
