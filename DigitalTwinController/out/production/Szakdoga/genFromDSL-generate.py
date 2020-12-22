import xml.etree.ElementTree as xml
import sys
from xml.dom import minidom
import os


def genXML(dat):
    ###########################################################################

    root = xml.Element('dds')
    root.attrib['xmlns:xsi'] = "http://www.w3.org/2001/XMLSchema-instance"
    root.attrib['xsi:noNamespaceSchemaLocation'] = "http://community.rti.com/schema/6.0.0/rti_dds_profiles.xsd"
    root.attrib['version'] = "6.0.0"

    ###########################################################################
    qoslib = xml.SubElement(root, 'qos_library')
    qoslib.attrib['name'] = "QosLibrary"

    qosprofile = xml.SubElement(qoslib, 'qos_profile')
    qosprofile.attrib['name'] = "DefaultProfile"
    qosprofile.attrib['base_name'] = "BuiltinQosLib::Generic.StrictReliable"
    qosprofile.attrib['is_default_qos'] = "true"

    participantqos = xml.SubElement(qosprofile, 'participant_qos')

    participantname = xml.SubElement(participantqos, 'participant_name')

    name = xml.SubElement(participantname, 'name')
    name.text = "Connector Example"
    ###########################################################################

    ###########################################################################
    types = xml.SubElement(root, 'types')
    struct = xml.SubElement(types, 'struct')
    struct.attrib['name'] = dat[1].strip() + "Type"

    data = dat[2]
    for key in data:
        member = xml.SubElement(struct, "member")
        member.attrib['name'] = key
        member.attrib['type'] = data[key]
        if (data[key] == "string"):
            member.attrib['stringMaxLength'] = "128"

    struct = xml.SubElement(types, 'struct')
    struct.attrib['name'] = "MessageType"
    member = xml.SubElement(struct, "member")
    member.attrib['name'] = "Message"
    member.attrib['type'] = "string"
    member.attrib['stringMaxLength'] = "128"
    ###########################################################################
    domainlib = xml.SubElement(root, 'domain_library')
    domainlib.attrib['name'] = "MyDomainLibrary"

    domain = xml.SubElement(domainlib, 'domain')
    domain.attrib['name'] = "MyDomain"
    domain.attrib['domain_id'] = "0"

    registertype = xml.SubElement(domain, 'register_type')
    registertype.attrib['name'] = dat[1].strip() + "Type"
    registertype.attrib['type_ref'] = dat[1].strip() + "Type"

    topic = xml.SubElement(domain, 'topic')
    topic.attrib['name'] = dat[1].strip()
    topic.attrib['register_type_ref'] = dat[1].strip() + "Type"

    registertype = xml.SubElement(domain, 'register_type')
    registertype.attrib['name'] = "MessageType"
    registertype.attrib['type_ref'] = "MessageType"

    topic = xml.SubElement(domain, 'topic')
    topic.attrib['name'] = "Message"
    topic.attrib['register_type_ref'] = "MessageType"
    ###########################################################################

    ###########################################################################
    domainparticlib = xml.SubElement(root, 'domain_participant_library')
    domainparticlib.attrib['name'] = "MyParticipantLibrary"

    domainpartic = xml.SubElement(domainparticlib, 'domain_participant')
    domainpartic.attrib['name'] = "MyPubParticipant"
    domainpartic.attrib['domain_ref'] = "MyDomainLibrary::MyDomain"

    publisher = xml.SubElement(domainpartic, 'publisher')
    publisher.attrib['name'] = "MyPublisher"

    datawriter = xml.SubElement(publisher, 'data_writer')
    datawriter.attrib['name'] = "My" + dat[1].strip() + "Writer"
    datawriter.attrib['topic_ref'] = dat[1].strip()

    datawriter = xml.SubElement(publisher, 'data_writer')
    datawriter.attrib['name'] = "MyMessageWriter"
    datawriter.attrib['topic_ref'] = "Message"

    domainpartic1 = xml.SubElement(domainparticlib, 'domain_participant')
    domainpartic1.attrib['name'] = "MySubParticipant"
    domainpartic1.attrib['domain_ref'] = "MyDomainLibrary::MyDomain"

    subscriber = xml.SubElement(domainpartic1, 'subscriber')
    subscriber.attrib['name'] = "MySubscriber"

    datareader = xml.SubElement(subscriber, 'data_reader')
    datareader.attrib['name'] = "My" + dat[1].strip() + "Reader"
    datareader.attrib['topic_ref'] = dat[1].strip()

    datareader = xml.SubElement(subscriber, 'data_reader')
    datareader.attrib['name'] = "MyMessageReader"
    datareader.attrib['topic_ref'] = "Message"

    ###########################################################################


    rough_string = xml.tostring(root, 'utf-8')
    reparsed = minidom.parseString(rough_string)

    filename = "Every.xml"
    if not os.path.exists("generated"):
        os.mkdir("generated")
    if not os.path.exists("generated/" + dat[1]):
        os.mkdir(("generated/" + dat[1]))

    file = open("generated/" + dat[1] + "/" + filename, 'w')
    file.write(reparsed.toprettyxml(indent="  "))
    file.close()


def genReaderAndDitto(dat, thingId, functiontodata):
    print(dat)
    code1 = '''const WebSocket = require('ws');
    class DittoWebSocket {

        constructor(pingInterval = 60000) {
            this.pingInterval = pingInterval;
            this.stopPing = false;
            this.clientCallbacks = {};
        }
        registerForMessages() {
            this.sendRaw('START-SEND-MESSAGES');
            console.log('registering')
            //this.logSendToUI(undefined, 'START-SEND-MESSAGES', '', 'tell Ditto that i want to receive Messages');
        }

        onConnected() {
            console.log('connected');
            this.registerForMessages();
        }
        connect(/*connectionConfig, callback*/) {
            const baseUrl = 'ws://ditto:ditto@localhost:8080/ws/1';
            this.ws = new WebSocket(baseUrl);
            this.ws.onopen = () => this.onOpen(this.onConnected());

        }

        close(callback) {
            this.ws.onclose = callback;
            this.ws.close();
        }

        onOpen(callback) {
            // define as functions, so the message is executed in current context
            this.ws.onmessage = (message) => this.onMessage(message);
            this.ws.onclose = () => this.onClosed();
            this.ws.onerror = (error) => this.onError(error);
            if (isDefined(callback)) {
                callback();
            }
            //this.schedulePingMessage();
        }

        onMessage(message) {
            if(message.data != "START-SEND-MESSAGES:ACK"){
                var obj = JSON.parse(message.data)
                if(obj['topic'].includes('messages')){
                    let array = obj['topic'].split('/')
                    let subject = array.pop()
                    sendToDevices(subject)
                }
            }
        }

        onClosed() {
            this.stopPing = true;
            if (isDefined(this.clientCallbacks.onClosed)) {
                this.clientCallbacks.onClosed();
            }
        }

        onError(error) {
            console.log(`error: ${e}`);
            if (isDefined(this.clientCallbacks.onError)) {
                this.clientCallbacks.onError(error);
            }
        }


        sendRaw(content) {
            this.ws.send(content);
        }

        send(json) {
            console.log(`sending JSON ${JSON.stringify(json)}`);
            this.sendRaw(JSON.stringify(json));
        }

        reply(message, payload, contentType, status) {
            const response = Object.assign({
                status
            }, this.protocolMessage(
                message.headers['thing-id'],
                message.topic,
                message.headers.subject,
                message.headers['correlation-id'],
                contentType,
                "FROM",
                message.path.replace("inbox", "outbox"),
                payload
            ));

            this.send(response);
        }

        /**
        * Create a Ditto protocol WebSocket API Message.
        */
        protocolMessage(thingId, topic, subject, correlationId, contentType, direction, path, payload) {
            return Object.assign({
                    "headers": {
                        "thing-id": thingId,
                        subject,
                        "correlation-id": correlationId,
                        "content-type": contentType,
                        direction
                    }
                },
                this.protocolEnvelope(topic, path, payload)
            );
        }

        /*
        * Create a ditto protocol envelope.
        */
        protocolEnvelope(topic, path, value) {
            return {
                topic,
                path,
                value
            };
        }

        setOnMessage(onMessage) {
            this.clientCallbacks.onMessage = onMessage;
        }

        setOnClosed(onClosed) {
            this.clientCallbacks.onClosed = onClosed;
        }

        setOnError(onError) {
            this.clientCallbacks.onError = onError;
        }

        schedulePingMessage() {
            setTimeout(() => this.sendPingMessage(), this.pingInterval);
        }

        sendPingMessage() {
            if (this.stopPing) {
                this.stopPing = false;
            } else {
                this.sendRaw(new ArrayBuffer(0));
                this.schedulePingMessage();
            }
        }
    }

    const protocolEnvelope = (topic, path, value) =>{
        return {
            topic,
            path,
            value
        };
    }


    const path = require('path')
    const rti = require('rticonnextdds-connector')\n'''

    code1 = code1 + "const configFile = path.join(__dirname, '/" + "Every.xml')\n"

    data = dat[2]
    code1 = code1 + '''const run''' + dat[1].strip() + ''' = async (sock) => {

    //

    //
    const connector = new rti.Connector('MyParticipantLibrary::MySubParticipant', configFile)
    const input = connector.getInput('MySubscriber::My''' + dat[1].strip() + '''Reader')
    try {
        console.log('Waiting for publications...')
        await input.waitForPublications()

        console.log('Waiting for data...')
        for (let i = 0; i < 500; i++) {
        await input.wait()
        input.take()
        for (const sample of input.samples.validDataIter) {
            const data = sample.getJson()\n'''

    for key in data:
        code1 = code1 + '''        const ''' + key + " = data." + key + "\n"

    for key in data:
        code1 = code1 + '''        console.log('Received ''' + key + ''': ' +''' + key + ''')\n'''
    code1 = code1 + '''
    const updateFeatureMessage = protocolEnvelope(
        '''
    code1 = code1 + "'" + dat[0] + '/' + thingId + "/things/twin/commands/modify',"
    code1 = code1 + '''
                '/',   
                {
                    "thingId":"'''
    code1 = code1 + dat[0] + ':' + thingId + '",\n'
    code1 = code1 + '      "features":{\n'
    for key in functiontodata:

        code1 = code1 + '''       "''' + key + '''":{
            "properties":{'''
        for data in functiontodata[key]:
            code1 = code1 + '''
           "''' + data + '''" :''' + data + ''',\n'''

        code1 = code1 + '''}},'''
    code1 = code1 + '''     }}
        )
        sock.send(updateFeatureMessage)
    }}} catch (err) {
        console.log('Error encountered: ' + err)
    }
    connector.close()
    }

'''

    code1 = code1 + '''
    isDefined = (arg) => typeof arg !== 'undefined';
    const sendToDevices = async (message)=> {
    const connector = new rti.Connector('MyParticipantLibrary::MyPubParticipant', configFile)
    const output = connector.getOutput('MyPublisher::MyMessageWriter')
    try {
        console.log('Waiting for subscriptions...')
        await output.waitForSubscriptions()

        console.log('Writing...')
        output.instance.setString('Message', message)
        output.write()

        // Wait for all subscriptions to receive the data before exiting
        await output.wait()
    } catch (err) {
        console.log('Error encountered: ' + err)
    }
    connector.close()

    }
    const socket = new DittoWebSocket()
    socket.connect()'''

    code1 = code1 + '''
    run''' + dat[1].strip() + '''(socket)'''
    path = os.getcwd()
    file = open(path + "/generated/" + dat[1] + "/AllReader.js", 'w')
    file.write(code1)


def genMockWriter(dat):
    path = os.getcwd()
    file = open(path + "/generated/" + dat[1].strip() + "/MockWriter.py", "w")
    code1 = '''import sys
from sys import path as sys_path
from os import path as os_path

file_path = os_path.dirname(os_path.realpath(__file__))
sys_path.append(file_path + "/../../../")
import rticonnextdds_connector as rti
with rti.open_connector(
        config_name="MyParticipantLibrary::MyPubParticipant",
        url=file_path +"/''' + "Every.xml" + '''" ) as connector:'''
    code2 = "\n"
    count = 1
    for key in dat[2]:
        code2 = code2 + '''  ''' + key + " =sys.argv[" + str(count) + "]\n"
        count = count + 1
    code3 = '''  output = connector.get_output("MyPublisher::My''' + dat[1].strip() + '''Writer")

  print("Waiting for subscriptions...")
  output.wait_for_subscriptions()
        '''
    code4 = "\n"
    for key in dat[2]:
        code4 = code4 + '''  output.instance.set_string("''' + key + '''",''' + key + ")\n"
    code4 = code4 + '''  output.write()
  output.wait()'''
    file.write(code1 + code2 + code3 + code4)
    file.close()


def genDeviceWriter(dat, devicechoice, targetdir):
    devices = {"SenseHat": {"Humidity": "sense.get_humidity()", "Temperature": "sense.get_temperature()",
                            "Pressure": "sense.get_pressure()"}}
    path = os.getcwd()
    file = open(path + "/generated/" + dat[1].strip() + "/DeviceWriter.py", "w")
    code1 = '''import sys
from sys import path as sys_path
from os import path as os_path
from sense_hat import SenseHat
import time
sense = SenseHat()
file_path = os_path.dirname(os_path.realpath(__file__))
sys_path.append(file_path + "/../../../")
import rticonnextdds_connector as rti
with rti.open_connector(
            config_name="MyParticipantLibrary::MyPubParticipant",''' + '\n        url="' + targetdir + '/Every.xml") as connector:\n    while True:'
    code2 = "\n"

    count = 0
    for key in dat[2]:
        code2 = code2 + '''        ''' + key + " =" + devices[devicechoice[count]][devicechoice[count + 1]] + "\n"
        count = count + 2
    code3 = '''        output = connector.get_output("MyPublisher::My''' + dat[1].strip() + '''Writer")
        print("Waiting for subscriptions...")
            '''
    code4 = "\n"
    for key in dat[2]:
        if (dat[2][key] == "string"):
            type = "string"
        else:
            type = "number"
        code4 = code4 + "        output.instance.set_" + type + '''("''' + key + '''",''' + key + ")\n"

    code4 = code4 + '''        output.write()
        #output.wait()
        time.sleep(5)'''
    file.write(code1 + code2 + code3 + code4)
    file.close()


def generate():
    data = []
    for str in sys.argv:
        data.append(str)
    name = data[2]
    namespace = data[3]
    thingid = data[1]
    targetdir = data[4]
    functiontodata = {}

    del (data[0])
    del (data[0])
    del (data[0])
    del (data[0])
    del (data[0])
    count = 0
    for dat in data:
        if dat.__contains__("->"):
            functiontodata[dat.split("->")[0]] = dat.split("->")[1]
            count = count + 1

    values = functiontodata.values()
    realfunctiontodata = {}
    for value in values:
        datafunc = []
        for key in functiontodata.keys():
            if (functiontodata[key] == value):
                datafunc.append(key)
        realfunctiontodata[value] = datafunc
    for i in range(count):
        del (data[0])

    index = 0
    datavars = []
    datavars.append(namespace)
    datavars.append(name)
    datavars.append({})
    devicechoices = []
    while index < len(data) / 4:
        datavars[2][data[4 * index + 0]] = data[4 * index + 1]
        devicechoices.append(data[4 * index + 2])
        devicechoices.append(data[4 * index + 3])
        index = index + 1
    genXML(datavars)
    genReaderAndDitto(datavars, thingid, realfunctiontodata)
    genMockWriter(datavars)
    genDeviceWriter(datavars, devicechoices, targetdir)


generate()
