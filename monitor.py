#!/usr/bin/env python

import config

import pika
import json

from pyzabbix import ZabbixAPI


if __name__ == "__main__":
    zapi = ZabbixAPI("http://ni2.codeabovelab.com:8080/zabbix")
    zapi.login("admin", "zabbix")
    print "Connected to Zabbix API Version %s" % zapi.api_version()



    rabbit_connection = pika.BlockingConnection(pika.URLParameters('amqp://admin:opentsp@ni1.codeabovelab.com:5672/%2F'))
    print "Connected to rabbit %s"% rabbit_connection.server_properties
    channel = rabbit_connection.channel()
    channel.exchange_declare(exchange='opentsp.log', type='fanout')
    for host in zapi.host.get(output="extend"):
        for item in zapi.item.get(hostid=host['hostid']):
            channel.basic_publish(exchange='opentsp.log', routing_key='zabbix', body=json.dumps(item), properties=pika.BasicProperties(content_type='application/json'))

    rabbit_connection.close()