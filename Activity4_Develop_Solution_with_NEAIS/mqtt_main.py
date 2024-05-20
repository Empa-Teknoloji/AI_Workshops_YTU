from __future__ import absolute_import
from __future__ import print_function
import json
from awscrt import io, mqtt
import sys
import threading
import requests
import cv2
import numpy as np

import Activity4_Develop_Solution_with_NEAIS.mqtt_constants as mqtt_constants


# 1. Get Authorization Key For Connection MQTT
received_all_event = threading.Event()
file_pointer = open("Dataset_from_Cloud_over_MQTT.csv", "a+")


def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i : i + n]


def get_authorization_key():
    response = requests.get(
        "https://apiv2.empacloud.com/sdk/ws-connection-kit",
        headers={"Authorization": mqtt_constants.EMPACLOUD_API_KEY},
    )
    if response.status_code == 200:
        response = response.json()
        return response["payload"]["ws_key"]
    else:
        raise Exception("API ERROR")


def on_connection_interrupted(connection, error, **kwargs):
    print("Connection interrupted. error: {}".format(error))


# Callback when an interrupted connection is re-established.
def on_connection_resumed(connection, return_code, session_present, **kwargs):
    print(
        "Connection resumed. return_code: {} session_present: {}".format(
            return_code, session_present
        )
    )

    if return_code == mqtt.ConnectReturnCode.ACCEPTED and not session_present:
        print("Session did not persist. Resubscribing to existing topics...")
        resubscribe_future, _ = connection.resubscribe_existing_topics()

        # Cannot synchronously wait for resubscribe result because we're on the connection's event-loop thread,
        # evaluate result with a callback instead.
        resubscribe_future.add_done_callback(on_resubscribe_complete)


def on_resubscribe_complete(resubscribe_future):
    resubscribe_results = resubscribe_future.result()
    print("Resubscribe results: {}".format(resubscribe_results))

    for topic, qos in resubscribe_results["topics"]:
        if qos is None:
            sys.exit("Server rejected resubscribe to topic: {}".format(topic))


# Callback when the subscribed topic receives a message
def on_message_received(topic, payload, **kwargs):
    print("Message Received")
    try:
        payload = json.loads(payload)

        new_list = []

        acc_set = payload["acc"]
        gyro_set = payload["gyro"]

        gyro_list = list(divide_chunks(gyro_set, 3))
        acc_list = list(divide_chunks(acc_set, 3))

        index = 0

        while index != len(gyro_list):
            new_list.extend(acc_list[index])
            new_list.extend(gyro_list[index])
            index += 1

        new_list = map(str, new_list)
        file_pointer.write(",".join(new_list) + "\n")

        print("Message Write")
    except Exception as exc:
        print("Data Parse Error", exc)
        pass


def add_headers(transform_args):
    transform_args.http_request.headers.add(
        "x-amz-customauthorizer-name", "emc-prod-custom-authorizer"
    )

    transform_args.set_done()


if __name__ == "__main__":
    ws_key = get_authorization_key()
    # Spin up resources
    event_loop_group = io.EventLoopGroup(1)
    host_resolver = io.DefaultHostResolver(event_loop_group)
    client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)

    tls_options = io.TlsContextOptions()
    socket_options = io.SocketOptions()

    tls_ctx = io.ClientTlsContext(options=tls_options)
    client = mqtt.Client(client_bootstrap, tls_ctx)

    mqtt_connection = mqtt.Connection(
        client=client,
        host_name=mqtt_constants.EMPACLOUD_MQTT_ENDPOINT,
        port=443,
        on_connection_interrupted=on_connection_interrupted,
        on_connection_resumed=on_connection_resumed,
        client_id="AIDe9vz8p_TEST",
        clean_session=True,
        keep_alive_secs=6,
        username=ws_key,
        password=ws_key,
        socket_options=socket_options,
        use_websockets=True,
        websocket_handshake_transform=add_headers,
    )

    print("Connecting")
    connect_future = mqtt_connection.connect()

    # Future.result() waits until a result is available
    connect_future.result()
    print("Connected!")

    subscribe_future, packet_id = mqtt_connection.subscribe(
        topic=f"pub/AIDe9vz8p/aiworkshop001",
        qos=mqtt.QoS.AT_LEAST_ONCE,
        callback=on_message_received,
    )

    subscribe_result = subscribe_future.result()
    print("Subscribed with {}".format(str(subscribe_result["qos"])))

    # keyboard.wait("esc")
    cv2.imshow("KeyPressWait", np.zeros((100, 100)))
    cv2.waitKey(0)

    print("Disconnecting...")
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
    print("Disconnected!")

    file_pointer.close()
