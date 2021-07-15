# Simon Duff <sduff@confluent.io>
# Basic consumer to read Confluent Cloud Audit Log events and write them to a file

import os # needed to access environment variables
from confluent_kafka import Consumer

cfg= {
    'security.protocol': 'sasl_ssl',
    'sasl.mechanisms': 'PLAIN',
    'sasl.username': os.environ.get('SASL_USERNAME'),
    'sasl.password': os.environ.get('SASL_PASSWORD'),
    'bootstrap.servers': os.environ.get('BOOTSTRAP_SERVERS'),
    'group.id': os.environ.get('GROUP_ID') or "auditlogger",
    'auto.offset.reset': os.environ.get('OFFSET_RESET') or "earliest"
}

print ("Configuration")
print (cfg)

# Make sure log file is writeable
logfile = os.path.join("/logs",(os.environ.get('LOGFILE') or "confluent-cloud-audit-log"))
try:
	open(logfile,"a+")
except:
	print("Error attempting to write to logfile: ",logfile)
	quit()

# Use the default topic unless overwritten
topic = os.environ.get('TOPIC') or 'confluent-audit-log-events'

# Create the consumer and start processing audit log events
c = Consumer(cfg)
print("Consumer created")
c.subscribe([topic])
print("Subsribed to ", topic)
print("Writing to ", logfile)

while True:
    msg = c.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        continue

    f = open(logfile,"a+")
    f.write('{}\n'.format(msg.value().decode('utf-8')))
    f.close()

c.close()
