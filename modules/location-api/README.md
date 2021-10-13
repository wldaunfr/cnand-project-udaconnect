## Generating gRPC files

`pip install grpcio-tools grpcio`

`python -m grpc_tools.protoc -I./ --python_out=./app --grpc_python_out=./app ./app/location.proto`
