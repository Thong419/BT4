GRPC_SOURCES = intent_service_pb2.py intent_service_pb2_grpc.py

all: $(GRPC_SOURCES)

$(GRPC_SOURCES): intent_service.proto
	python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. intent_service.proto

clean:
	python -c "from pathlib import Path; [Path(name).unlink(missing_ok=True) for name in ['intent_service_pb2.py', 'intent_service_pb2_grpc.py']]"