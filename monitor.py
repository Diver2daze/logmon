#!/usr/bin/env python

import config

import pika
import json

from pyzabbix import ZabbixAPI


if __name__ == "__main__":
    message ={}
    zapi = ZabbixAPI("http://ni2.codeabovelab.com:8080/zabbix")
    zapi.login("admin", "zabbix")
    print "Connected to Zabbix API Version %s" % zapi.api_version()

    for host in zapi.host.get(output="extend"):
        message[host['hostid']]=zapi.item.get(hostid=host['hostid'])

    #print json.dumps(message, indent=2)
    rabbit_connection = pika.BlockingConnection(pika.URLParameters('amqp://admin:opentsp@ni1.codeabovelab.com:5672/%2F'))
    channel = rabbit_connection.channel()
    channel.exchange_declare(exchange='opentsp.log', type='fanout')
    channel.basic_publish(exchange='opentsp.log', routing_key='', body=json.dumps(message, indent=2))