from awsiot import mqtt_connection_builder
from awscrt import io, mqtt
import logging

log = logging.getLogger(__name__)


def on_message_received(topic, payload, dup, qos, retain, **kwargs):
    print("Received message from topic '{}': {}".format(topic, payload))


def connect(prov):
    event_loop_group = io.EventLoopGroup(1)
    host_resolver = io.DefaultHostResolver(event_loop_group)
    client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
    mqtt_connection = mqtt_connection_builder.mtls_from_bytes(
        cert_bytes=bytes(prov['credentials']['cert'], 'utf8'),
        pri_key_bytes=bytes(prov['credentials']['privateKey'], 'utf8'),
        ca_bytes=bytes(prov['credentials']['rootCert'], 'utf8'),
        endpoint=prov['connection']['endpoint'],
        client_bootstrap=client_bootstrap,
        region='us-west-2',
        client_id=prov['credentials']['clientId'],
        # anything below here you can configure to your liking, add connection interrupted/resumed handlers etc.
        clean_session=False,
        keep_alive_secs=30
        # on_connection_interrupted=on_connection_interrupted,
        # on_connection_resumed=on_connection_resumed,
    )
    connect_future = mqtt_connection.connect()
    connect_future.result()
    log.debug("Connected!")

    # subscribe to MQTT messages sent by the cloud, important!
    subscribe_future, packet_id = mqtt_connection.subscribe(
        topic=prov['topics']['host']['incoming'],
        qos=mqtt.QoS.AT_LEAST_ONCE,
        callback=on_message_received)
    subscribe_future.result()

    subscribe_future, packet_id = mqtt_connection.subscribe(
        topic=prov['topics']['device']['incoming'],
        qos=mqtt.QoS.AT_LEAST_ONCE,
        callback=on_message_received)
    subscribe_future.result()

    subscribe_future, packet_id = mqtt_connection.subscribe(
        topic=prov['topics']['room']['incoming'],
        qos=mqtt.QoS.AT_LEAST_ONCE,
        callback=on_message_received)
    subscribe_future.result()

    subscribe_future, packet_id = mqtt_connection.subscribe(
        topic=prov['topics']['org']['incoming'],
        qos=mqtt.QoS.AT_LEAST_ONCE,
        callback=on_message_received)
    subscribe_future.result()

    return mqtt_connection