import grpc
import json
import location_pb2
import location_pb2_grpc
import logging
import os
import time

from concurrent import futures
from datetime import datetime
from kafka import KafkaProducer
from schemas import LocationSchema

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("udaconnect")

class LocationServicer(location_pb2_grpc.LocationServiceServicer):
    def Create(self, request, context):

        timestamp = request.creation_time
        timestamp_dt = datetime.fromtimestamp(timestamp.seconds + timestamp.nanos/1e9)

        kafka_value = json.dumps({
            "person_id": request.person_id,
            "latitude": request.latitude,
            "longitude": request.longitude,
            "creation_time": timestamp_dt.isoformat()
        }).encode()

        logger.info(f"{kafka_value}")
        kafka_producer.send(kafka_topic, kafka_value)
        kafka_producer.flush()

        return request


# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
location_pb2_grpc.add_LocationServiceServicer_to_server(LocationServicer(), server)

# Initialize Kafka producer
kafka_topic = os.environ.get('KAFKA_TOPIC') or 'locations'
kafka_servers = os.environ.get('KAFKA_SERVERS') or 'localhost:9092'
kafka_producer = KafkaProducer(bootstrap_servers=kafka_servers)

server.add_insecure_port("[::]:5005")
server.start()
logger.info("Server running on port 5005")
server.wait_for_termination()
