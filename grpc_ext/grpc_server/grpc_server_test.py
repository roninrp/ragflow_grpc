import socket


def test_grpc_server_is_up(host="localhost", port=50051):
    """Test that the gRPC server is listening on the given port."""
    s = socket.socket()
    s.settimeout(2)
    try:
        s.connect((host, port))
        connected = True
    except (ConnectionRefusedError, socket.timeout):
        connected = False
    finally:
        s.close()

    assert connected, f"Cannot connect to gRPC server at {host}:{port}"
