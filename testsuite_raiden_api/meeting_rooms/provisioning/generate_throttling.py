import unittest
import sys
import time
import json
import requests
from awscrt import mqtt, io
from awsiot import mqtt_connection_builder
import random
import argparse
from common.aws_wrappers import SSMParameterStore


def on_message_received(topic, payload, dup, qos, retain, **kwargs):
    print("Received message from topic '{}': {} at time {}".format(topic, payload, str(time.ctime(int(time.time())))))


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
    print("Connected!")

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


class RaidenSendMessages(unittest.TestCase):
    """
    Throttling tests.
    """

    @classmethod
    def setUpClass(cls):
        try:
            super(RaidenSendMessages, cls).setUpClass()
            cls.role = 'SysAdmin'
            env_list = ['qadev', 'production', 'latest', 'staging', 'dev']
            parser = argparse.ArgumentParser(
                description='Please specify the server where tests have to be run',
            )
            parser.add_argument('--env', '-e', choices=env_list)
            args = parser.parse_args()
            cls.env = args.env
            cls.config = None
            try:
                aws_config_file = None
                prefix = '/seam/raiden/' + cls.env + '/'
                cls.ssm_ps_wrapper = SSMParameterStore(
                    prefix=prefix, aws_config_file=aws_config_file)
            except Exception as e:
                print(
                    'Unable to fetch SSM Credentials. Make sure AWS credentials are set properly')
                raise e

            try:
                cls.config = cls.ssm_ps_wrapper.get_parameter_value_as_struct(
                    'config')
            except Exception as e:
                print('Exception while reading config: {}'.format(e))
                raise e

        except Exception as e:
            print('Exception occurred- {}'.format(e))
            raise e

    def test_001_send_multipe_device_connect_disconnect_messages(self):
        """Send multiple device connect and disconnect messages to enable throttling functionality.
            Setup:
                  Sign in to Sync Portal using valid Super Admin credentials.

            Test:
                 1. Create an Org.
                 2. Provision a room containing mettup.
                 3. Send multiple device connect and disconnect status messages for 15 minutes.
                 4. Throttling should occur and room events should stop.
                 5. Send only few messages for next 20 minutes.
                 6. Between 10-15 minutes, throttling stops and the room events resume.

        """
        # Step1: Sign In using System Admin Credentials
        baseUrl = self.config.BASE_URL + '/api/'  # point to your stage
        _data = self.config.ROLES[self.role]['signin_payload']

        # Step 1: Sign In
        sign_in_response = requests.post(baseUrl + 'session/sign-in',
                                         data=_data)
        print()
        print('--Sign in response--')
        print(json.dumps(sign_in_response.json(), indent=2))
        s = requests.Session()
        s.headers.update({'authorization': sign_in_response.json()['token']})

        # Step2: Create Organization.
        org_creation_response = s.post(baseUrl + 'org', data={'name': 'Test Org ' + str(int(random.random() * 10000))})
        orgId = org_creation_response.json()['id']
        print('--Org Creation response--')
        print(json.dumps(org_creation_response.json(), indent=2))

        try:
            # Step2: Room Provisioning
            room_name = 'Test Room ' + str(int(random.random() * 10000))
            r = s.post(baseUrl + 'org/' + orgId + '/prov',
                       data={'room': room_name})
            print('--Initiate Provisioning response--')
            print(json.dumps(r.json(), indent=2))
            init_prov_response = r.json()['completion']
            completeUrl = init_prov_response['url']
            r = s.post(completeUrl, json={
                'completion': init_prov_response,
                'device': {
                    "type": "Computer",
                    "name": room_name,
                    "make": "Apple",
                    "model": "Apple Mac mini",
                    "proc": "Intel(R) Core(TM) i7-8700B CPU @ 3.20GHz",
                    "ram": "16 GB",
                    "os": "macOS",
                    "osv": "Version 10.16 (Build 20D91)",
                    "sw": "2.4.356",
                    "ip": "10.0.1.23"
                }
            })
            prov = r.json()
            roomId = prov['room']['id']
            print('--Provisioning response--')
            print(json.dumps(prov, indent=2))

            # Step 3: Establish MQTT connection and send connect/disconnect/reconnect messages.
            mqtt_connection = connect(prov)

            # send message
            end_time = time.time() + 60 * 15
            while time.time() < end_time:
                publish_future, packet_id = mqtt_connection.publish(
                    topic=prov['topics']['host']['outgoing'],
                    payload=json.dumps({
                        'payload': {
                            "room": {
                                "infoTs": time.time(),
                            },
                            'devices': [{
                                "uid": "0x14115000",
                                "pid": "0x881",
                                "name": "MeetUp",
                                "type": "MeetUp",
                                "vv": "1.0.1008",
                                "eev": "1.28",
                                "ablev": "1.0.0",
                                "acv": "1.0.0",
                                "status": 1,
                                "updateStatus": -1,
                                "serial": "088f:20181011:4473d623600e",
                                "sw": "1.0.1008",
                                "bleMac": "44:73:d6:0e:9e:44"
                            }]
                        },
                        'type': 2,
                        'ts': time.time()
                    }),
                    qos=mqtt.QoS.AT_LEAST_ONCE)
                publish_future.result()

                time.sleep(0.75)

                publish_future, packet_id = mqtt_connection.publish(
                    topic=prov['topics']['host']['outgoing'],
                    payload=json.dumps({
                        'payload': {
                            "room": {
                                "infoTs": time.time(),
                            },
                            'devices': [{
                                "uid": "0x14115000",
                                "pid": "0x881",
                                "name": "MeetUp",
                                "type": "MeetUp",
                                "vv": "1.0.1008",
                                "eev": "1.28",
                                "ablev": "1.0.0",
                                "acv": "1.0.0",
                                "status": 0,
                                "updateStatus": -1,
                                "serial": "088f:20181011:4473d623600e",
                                "sw": "1.0.1008",
                                "bleMac": "44:73:d6:0e:9e:44"
                            }]
                        },
                        'type': 2,
                        'ts': time.time()
                    }),
                    qos=mqtt.QoS.AT_LEAST_ONCE)
                publish_future.result()

            time.sleep(10)
            # Check there is no room event around the end time.
            r = s.post(baseUrl + 'org/' + orgId + '/room/' + roomId + '/events/search',
                       data=json.dumps({}))
            events = r.json()
            latest_Event = events['events'][0]
            print(json.dumps(latest_Event))
            time_stamp = float(latest_Event['ts']/1000)
            assert not (end_time + 120 > time_stamp > end_time - 120), 'Throttling did not occur'
            if not (end_time + 120 > time_stamp > end_time - 120):
                print('Throttling has occurred successfully.')

            start = time.time()
            while time.time() - start < 60 * 15:
                publish_future, packet_id = mqtt_connection.publish(
                    topic=prov['topics']['host']['outgoing'],
                    payload=json.dumps({
                        'payload': {
                            "room": {
                                "infoTs": time.time(),
                            },
                            'devices': [{
                                "uid": "0x14115000",
                                "pid": "0x881",
                                "name": "MeetUp",
                                "type": "MeetUp",
                                "vv": "1.0.1008",
                                "eev": "1.28",
                                "ablev": "1.0.0",
                                "acv": "1.0.0",
                                "status": 1,
                                "updateStatus": -1,
                                "serial": "088f:20181011:4473d623600e",
                                "sw": "1.0.1008",
                                "bleMac": "44:73:d6:0e:9e:44"
                            }]
                        },
                        'type': 2,
                        'ts': time.time()
                    }),
                    qos=mqtt.QoS.AT_LEAST_ONCE)
                publish_future.result()

                time.sleep(15)

                publish_future, packet_id = mqtt_connection.publish(
                    topic=prov['topics']['host']['outgoing'],
                    payload=json.dumps({
                        'payload': {
                            "room": {
                                "infoTs": time.time(),
                            },
                            'devices': [{
                                "uid": "0x14115000",
                                "pid": "0x881",
                                "name": "MeetUp",
                                "type": "MeetUp",
                                "vv": "1.0.1008",
                                "eev": "1.28",
                                "ablev": "1.0.0",
                                "acv": "1.0.0",
                                "status": 0,
                                "updateStatus": -1,
                                "serial": "088f:20181011:4473d623600e",
                                "sw": "1.0.1008",
                                "bleMac": "44:73:d6:0e:9e:44"
                            }]
                        },
                        'type': 2,
                        'ts': time.time()
                    }),
                    qos=mqtt.QoS.AT_LEAST_ONCE)
                publish_future.result()

            end_of_timer = time.time() + 60 * 5
            while time.time() < end_of_timer:
                publish_future, packet_id = mqtt_connection.publish(
                    topic=prov['topics']['host']['outgoing'],
                    payload=json.dumps({
                        'payload': {
                            "room": {
                                "infoTs": time.time(),
                            },
                            'devices': [{
                                "uid": "0x14115000",
                                "pid": "0x881",
                                "name": "MeetUp",
                                "type": "MeetUp",
                                "vv": "1.0.1008",
                                "eev": "1.28",
                                "ablev": "1.0.0",
                                "acv": "1.0.0",
                                "status": 1,
                                "updateStatus": -1,
                                "serial": "088f:20181011:4473d623600e",
                                "sw": "1.0.1008",
                                "bleMac": "44:73:d6:0e:9e:44"
                            }]
                        },
                        'type': 2,
                        'ts': time.time()
                    }),
                    qos=mqtt.QoS.AT_LEAST_ONCE)
                publish_future.result()

                time.sleep(20)

                publish_future, packet_id = mqtt_connection.publish(
                    topic=prov['topics']['host']['outgoing'],
                    payload=json.dumps({
                        'payload': {
                            "room": {
                                "infoTs": time.time(),
                            },
                            'devices': [{
                                "uid": "0x14115000",
                                "pid": "0x881",
                                "name": "MeetUp",
                                "type": "MeetUp",
                                "vv": "1.0.1008",
                                "eev": "1.28",
                                "ablev": "1.0.0",
                                "acv": "1.0.0",
                                "status": 0,
                                "updateStatus": -1,
                                "serial": "088f:20181011:4473d623600e",
                                "sw": "1.0.1008",
                                "bleMac": "44:73:d6:0e:9e:44"
                            }]
                        },
                        'type': 2,
                        'ts': time.time()
                    }),
                    qos=mqtt.QoS.AT_LEAST_ONCE)
                publish_future.result()

            time.sleep(10)
            r = s.post(baseUrl + 'org/' + orgId + '/room/' + roomId + '/events/search',
                       data=json.dumps({}))
            events = r.json()
            latest_Event = events['events'][0]
            print(json.dumps(latest_Event, indent=2))
            time_stamp = float(latest_Event['ts']/1000)
            if time_stamp > end_time:
                print('Throttling is stopped.')
            assert (time_stamp > end_time), 'Throttling did not stop'

            # disconnect
            mqtt_connection.disconnect().result()

            # I've just given myself a short timeout here to check that the room has been created and updated in Sync Portal
            time.sleep(90)

        finally:
            # clean-up
            s.delete(baseUrl + 'org/' + orgId)
            print('Org is deleted successfully!!.')

    def test_002_send_multiple_room_online_offline_messages(self):
        """Send multiple room online/offline messages to enable throttling functionality.
            Setup:
                  Sign in to Sync Portal using valid Super Admin credentials.

            Test:
                 1. Create an Org.
                 2. Provision a room containing mettup.
                 3. Send multiple room online/offline messages for 15 minutes.
                 4. Throttling should occur and room events should stop.
                 5. Send only few messages for next 20 minutes.
                 6. Between 10-15 minutes, throttling stops and the room events resume.

        """
        # Step1: Sign In using System Admin Credentials
        baseUrl = self.config.BASE_URL + '/api/'  # point to your stage
        _data = self.config.ROLES[self.role]['signin_payload']

        # Step 1: Sign In
        sign_in_response = requests.post(baseUrl + 'session/sign-in',
                          data=_data)
        print()
        print('--Sign in response--')
        print(json.dumps(sign_in_response.json(), indent=2))
        s = requests.Session()
        s.headers.update({'authorization': sign_in_response.json()['token']})

        # Step2: Create Organization.
        org_creation_response = s.post(baseUrl + 'org', data={'name': 'Test Org ' + str(int(random.random()*10000))})
        orgId = org_creation_response.json()['id']
        print('--Org Creation response--')
        print(json.dumps(org_creation_response.json(), indent=2))

        try:
            # Step2: Room Provisioning
            room_name = 'Test Room ' + str(int(random.random()*10000))
            r = s.post(baseUrl + 'org/' + orgId + '/prov',
                       data={'room': room_name})
            print('--Initiate Provisioning response--')
            print(json.dumps(r.json(), indent=2))
            init_prov_response = r.json()['completion']
            completeUrl = init_prov_response['url']
            r = s.post(completeUrl, json={
                'completion': init_prov_response,
                'device': {
                    "type": "Computer",
                    "name": room_name,
                    "make": "Apple",
                    "model": "Apple Mac mini",
                    "proc": "Intel(R) Core(TM) i7-8700B CPU @ 3.20GHz",
                    "ram": "16 GB",
                    "os": "macOS",
                    "osv": "Version 10.16 (Build 20D91)",
                    "sw": "2.4.356",
                    "ip": "10.0.1.23"
                }
            })
            prov = r.json()
            roomId = prov['room']['id']
            print('--Provisioning response--')
            print(json.dumps(prov, indent=2))

            # Step 3: Establish MQTT connection and send connect/disconnect/reconnect messages.
            mqtt_connection = connect(prov)
            publish_future, packet_id = mqtt_connection.publish(
                topic=prov['topics']['host']['outgoing'],
                payload=json.dumps({
                    'payload': {
                        "room": {
                            "infoTs": time.time(),
                        },
                        'devices': [{
                            "uid": "0x14115000",
                            "pid": "0x881",
                            "name": "MeetUp",
                            "type": "MeetUp",
                            "vv": "1.0.1008",
                            "eev": "1.28",
                            "ablev": "1.0.0",
                            "acv": "1.0.0",
                            "status": 1,
                            "updateStatus": -1,
                            "serial": "088f:20181011:4473d623600e",
                            "sw": "1.0.1008",
                            "bleMac": "44:73:d6:0e:9e:44"
                        }]
                    },
                    'type': 2,
                    'ts': time.time()
                }),
                qos=mqtt.QoS.AT_LEAST_ONCE)
            publish_future.result()

            # send message
            end_time = time.time() + 60 * 15
            while time.time() < end_time:
                try:
                    connect(prov)
                    time.sleep(1)
                except Exception as e:
                    pass

            time.sleep(10)
            # Check there is no room event around the end time.
            r = s.post(baseUrl + 'org/' + orgId + '/room/' + roomId + '/events/search',
                       data=json.dumps({}))
            events = r.json()
            latest_Event = events['events'][0]
            print(json.dumps(latest_Event))
            time_stamp = float(latest_Event['ts']/1000)
            assert not(end_time + 120 > time_stamp > end_time - 120), 'Throttling did not occur'
            if not(end_time + 120 > time_stamp > end_time - 120):
                print('Throttling has occurred successfully.')

            start = time.time()
            while time.time() - start < 60*15:
                try:
                    connect(prov)
                    time.sleep(15)
                except Exception as e:
                    pass

            end_of_timer = time.time() + 60 * 5
            while time.time() < end_of_timer:
                try:
                    connect(prov)
                    time.sleep(20)
                except Exception as e:
                    pass

            time.sleep(10)
            r = s.post(baseUrl + 'org/' + orgId + '/room/' + roomId + '/events/search',
                       data=json.dumps({}))
            events = r.json()
            latest_Event = events['events'][0]
            print(json.dumps(latest_Event, indent=2))
            time_stamp = float(latest_Event['ts']/1000)
            if time_stamp > end_time:
                print('Throttling is stopped.')
            assert (time_stamp > end_time), 'Throttling did not stop'

            mqtt_connection = connect(prov)
            time.sleep(10)
            mqtt_connection.disconnect().result()

        finally:
            # clean-up
            s.delete(baseUrl + 'org/' + orgId)
            print('Org is deleted successfully!!.')

    def test_003_send_limited_device_connect_disconnect_messages(self):
        """Send multiple device connect and disconnect messages to enable throttling functionality.
            Setup:
                  Sign in to Sync Portal using valid Super Admin credentials.

            Test:
                 1. Create an Org.
                 2. Provision a room containing mettup.
                 3. Send limited device connect and disconnect status messages for 10 minutes. (< 150 messages/ 5 minutes).
                 4. Throttling should not occur and room events should be seen.

        """
        # Step1: Sign In using System Admin Credentials
        baseUrl = self.config.BASE_URL + '/api/'  # point to your stage
        _data = self.config.ROLES[self.role]['signin_payload']

        # Step 1: Sign In
        sign_in_response = requests.post(baseUrl + 'session/sign-in',
                                         data=_data)
        print()
        print('--Sign in response--')
        print(json.dumps(sign_in_response.json(), indent=2))
        s = requests.Session()
        s.headers.update({'authorization': sign_in_response.json()['token']})

        # Step2: Create Organization.
        org_creation_response = s.post(baseUrl + 'org', data={'name': 'Test Org ' + str(int(random.random() * 10000))})
        orgId = org_creation_response.json()['id']
        print('--Org Creation response--')
        print(json.dumps(org_creation_response.json(), indent=2))

        try:
            # Step2: Room Provisioning
            room_name = 'Test Room ' + str(int(random.random() * 10000))
            r = s.post(baseUrl + 'org/' + orgId + '/prov',
                       data={'room': room_name})
            print('--Initiate Provisioning response--')
            print(json.dumps(r.json(), indent=2))
            init_prov_response = r.json()['completion']
            completeUrl = init_prov_response['url']
            r = s.post(completeUrl, json={
                'completion': init_prov_response,
                'device': {
                    "type": "Computer",
                    "name": room_name,
                    "make": "Apple",
                    "model": "Apple Mac mini",
                    "proc": "Intel(R) Core(TM) i7-8700B CPU @ 3.20GHz",
                    "ram": "16 GB",
                    "os": "macOS",
                    "osv": "Version 10.16 (Build 20D91)",
                    "sw": "2.4.356",
                    "ip": "10.0.1.23"
                }
            })
            prov = r.json()
            roomId = prov['room']['id']
            print('--Provisioning response--')
            print(json.dumps(prov, indent=2))

            # Step 3: Establish MQTT connection and send connect/disconnect/reconnect messages.
            mqtt_connection = connect(prov)

            # send message
            end_time = time.time() + 60 * 10
            while time.time() < end_time:
                try:
                    publish_future, packet_id = mqtt_connection.publish(
                        topic=prov['topics']['host']['outgoing'],
                        payload=json.dumps({
                            'payload': {
                                "room": {
                                    "infoTs": time.time(),
                                },
                                'devices': [{
                                    "uid": "0x14115000",
                                    "pid": "0x881",
                                    "name": "MeetUp",
                                    "type": "MeetUp",
                                    "vv": "1.0.1008",
                                    "eev": "1.28",
                                    "ablev": "1.0.0",
                                    "acv": "1.0.0",
                                    "status": 1,
                                    "updateStatus": -1,
                                    "serial": "088f:20181011:4473d623600e",
                                    "sw": "1.0.1008",
                                    "bleMac": "44:73:d6:0e:9e:44"
                                }]
                            },
                            'type': 2,
                            'ts': time.time()
                        }),
                        qos=mqtt.QoS.AT_LEAST_ONCE)
                    publish_future.result()

                    time.sleep(10)

                    publish_future, packet_id = mqtt_connection.publish(
                        topic=prov['topics']['host']['outgoing'],
                        payload=json.dumps({
                            'payload': {
                                "room": {
                                    "infoTs": time.time(),
                                },
                                'devices': [{
                                    "uid": "0x14115000",
                                    "pid": "0x881",
                                    "name": "MeetUp",
                                    "type": "MeetUp",
                                    "vv": "1.0.1008",
                                    "eev": "1.28",
                                    "ablev": "1.0.0",
                                    "acv": "1.0.0",
                                    "status": 0,
                                    "updateStatus": -1,
                                    "serial": "088f:20181011:4473d623600e",
                                    "sw": "1.0.1008",
                                    "bleMac": "44:73:d6:0e:9e:44"
                                }]
                            },
                            'type': 2,
                            'ts': time.time()
                        }),
                        qos=mqtt.QoS.AT_LEAST_ONCE)
                    publish_future.result()

                except Exception as e:
                    pass

            time.sleep(10)
            # Check there is no room event around the end time.
            r = s.post(baseUrl + 'org/' + orgId + '/room/' + roomId + '/events/search',
                       data=json.dumps({}))
            events = r.json()
            latest_Event = events['events'][0]
            print(json.dumps(latest_Event))
            time_stamp = float(latest_Event['ts']/1000)
            assert (end_time + 120 > time_stamp > end_time - 120), 'Throttling occurred'
            if end_time + 120 > time_stamp > end_time - 120:
                print('Throttling did not occur. Room events are seen.')

            # disconnect
            mqtt_connection.disconnect().result()

        finally:
            # clean-up
            s.delete(baseUrl + 'org/' + orgId)
            print('Org is deleted successfully!!.')

    def test_004_send_limited_room_online_offline_messages(self):
        """Send limited room online/offline messages to enable throttling functionality.
            Setup:
                  Sign in to Sync Portal using valid Super Admin credentials.

            Test:
                 1. Create an Org.
                 2. Provision a room containing mettup.
                 3. Send limited room online/offline messages for 10 minutes. (< 150 messages per 5 minutes)
                 4. Throttling should not occur and room events should be seen.

        """
        # Step1: Sign In using System Admin Credentials
        baseUrl = self.config.BASE_URL + '/api/'  # point to your stage
        _data = self.config.ROLES[self.role]['signin_payload']

        # Step 1: Sign In
        sign_in_response = requests.post(baseUrl + 'session/sign-in',
                                         data=_data)
        print()
        print('--Sign in response--')
        print(json.dumps(sign_in_response.json(), indent=2))
        s = requests.Session()
        s.headers.update({'authorization': sign_in_response.json()['token']})

        # Step2: Create Organization.
        org_creation_response = s.post(baseUrl + 'org', data={'name': 'Test Org ' + str(int(random.random() * 10000))})
        orgId = org_creation_response.json()['id']
        print('--Org Creation response--')
        print(json.dumps(org_creation_response.json(), indent=2))

        try:
            # Step2: Room Provisioning
            room_name = 'Test Room ' + str(int(random.random() * 10000))
            r = s.post(baseUrl + 'org/' + orgId + '/prov',
                       data={'room': room_name})
            print('--Initiate Provisioning response--')
            print(json.dumps(r.json(), indent=2))
            init_prov_response = r.json()['completion']
            completeUrl = init_prov_response['url']
            r = s.post(completeUrl, json={
                'completion': init_prov_response,
                'device': {
                    "type": "Computer",
                    "name": room_name,
                    "make": "Apple",
                    "model": "Apple Mac mini",
                    "proc": "Intel(R) Core(TM) i7-8700B CPU @ 3.20GHz",
                    "ram": "16 GB",
                    "os": "macOS",
                    "osv": "Version 10.16 (Build 20D91)",
                    "sw": "2.4.356",
                    "ip": "10.0.1.23"
                }
            })
            prov = r.json()
            roomId = prov['room']['id']
            print('--Provisioning response--')
            print(json.dumps(prov, indent=2))

            # Step 3: Establish MQTT connection and send connect/disconnect/reconnect messages.
            mqtt_connection = connect(prov)
            publish_future, packet_id = mqtt_connection.publish(
                topic=prov['topics']['host']['outgoing'],
                payload=json.dumps({
                    'payload': {
                        "room": {
                            "infoTs": time.time(),
                        },
                        'devices': [{
                            "uid": "0x14115000",
                            "pid": "0x881",
                            "name": "MeetUp",
                            "type": "MeetUp",
                            "vv": "1.0.1008",
                            "eev": "1.28",
                            "ablev": "1.0.0",
                            "acv": "1.0.0",
                            "status": 1,
                            "updateStatus": -1,
                            "serial": "088f:20181011:4473d623600e",
                            "sw": "1.0.1008",
                            "bleMac": "44:73:d6:0e:9e:44"
                        }]
                    },
                    'type': 2,
                    'ts': time.time()
                }),
                qos=mqtt.QoS.AT_LEAST_ONCE)
            publish_future.result()

            # send message
            end_time = time.time() + 60 * 10
            while time.time() < end_time:
                try:
                    connect(prov)
                    time.sleep(10)
                except Exception as e:
                    pass

            time.sleep(10)
            # Check there is no room event around the end time.
            r = s.post(baseUrl + 'org/' + orgId + '/room/' + roomId + '/events/search',
                       data=json.dumps({}))
            events = r.json()
            latest_Event = events['events'][0]
            print(json.dumps(latest_Event))
            time_stamp = float(latest_Event['ts']/1000)
            assert (end_time + 120 > time_stamp > end_time - 120), 'Throttling occurred'
            if end_time + 120 > time_stamp > end_time - 120:
                print('Throttling did not occur.Room events are seen.')

        finally:
            # clean-up
            s.delete(baseUrl + 'org/' + orgId)
            print('Org is deleted successfully!!.')


if __name__ == "__main__":
    test_suite = unittest.TestLoader().loadTestsFromTestCase(RaidenSendMessages)
    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    if result is None or result.failures or result.errors or result.unexpectedSuccesses:
        sys.exit("Test failures detected.")
