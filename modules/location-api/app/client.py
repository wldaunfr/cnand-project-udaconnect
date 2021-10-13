import grpc
import location_pb2
import location_pb2_grpc
import os
import random
import time
from google.protobuf.timestamp_pb2 import Timestamp

def random_location_message():
    creation_time = Timestamp()
    creation_time.GetCurrentTime()

    random_latitude = random.uniform(-90, 90)
    random_longitude = random.uniform(-180, 180)

    return location_pb2.LocationMessage(
        person_id=random.choice([1, 5, 6, 8, 9]),
        latitude=random_latitude,
        longitude=random_longitude,
        creation_time=creation_time,
    )

location_api_server = os.environ.get('LOCATION_API_SERVER') or 'localhost:30002'

channel = grpc.insecure_channel(location_api_server)
stub = location_pb2_grpc.LocationServiceStub(channel)

print(f"Sending random location data to '{location_api_server}' (press ctrl-c to stop)...")
while True:
    location_message = random_location_message()
    stub.Create(location_message)
    time.sleep(1)
