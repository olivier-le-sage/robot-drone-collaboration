"""
/*******************************************************************************
 * Copyright (c) 2011, 2013 IBM Corp.
 *
 * All rights reserved. This program and the accompanying materials
 * are made available under the terms of the Eclipse Public License v1.0
 * and Eclipse Distribution License v1.0 which accompany this distribution. 
 *
 * The Eclipse Public License is available at 
 *    http://www.eclipse.org/legal/epl-v10.html
 * and the Eclipse Distribution License is available at 
 *   http://www.eclipse.org/org/documents/edl-v10.php.
 *
 * Contributors:
 *    Ian Craggs - initial API and implementation and/or initial documentation
 *******************************************************************************/
"""
#add by me
import queue
import struct
import threading
import random

##

import MQTTSN,socket, time, MQTTSNinternal, _thread, sys,types
#, struct
debug=False
MQTTSNinternal.debug=False
      
class Callback:

  def __init__(self):
    self.events = []
    #self.registered = {} #added to client object
  def on_subscribe(self,client,TopicId,MsgId,rc):
    print("suback",TopicId,MsgId,rc)
    client.suback_flag=True
    for t in client.topic_ack:
      if t[1]==MsgId:
          t[2]=1 #acknowledged
          m="subscription acknowledged  "+str(t[0])
          print(m)
    client.sub_topicid=TopicId
    client.sub_msgid=MsgId
    client.sub_rc=rc
  def searchgw(self,client,packet):
    print("zz in search gateway ",packet)
    print (" search gw threads ",threading.activeCount()) 
    #client.gwinfo()

  def gwinfo(self,client,packet):
    print("In search gateway info ",packet)
    #gwinfo = MQTTSN.GWInfos()
    #gwinfo.unpack(packet)
    #print("address =",gwinfo.GwAdd)

    #self.events.append("gwinfo")
  def on_connect(self,client,address,rc):
    print("in on connect")
    if rc==0:
      client.connected_flag=True
    else:
      client.bad_connect_flag=True
  def on_disconnect(self,client,cause):
    #print("default connection Lost", cause)
    self.events.append("disconnected")
    client.connected_flag=False

  def messageArrived(self,client,TopicId, payload, qos, retained, msgid):
    m= "d-p-Arrived" +" topic  " +str(TopicId)+ "message " +\
       str(payload) +"  qos= " +str(qos) +" ret= " +str(retained)\
       +"  msgid= " + str(msgid)
    print("gotmessage")
    return True
  def published(self,client,msg_id):
    #print("In published callback ",msg_id)
    client.puback_flag=True

  def deliveryComplete(self, msgid):
    print("default deliveryComplete")
    pass
  
  def advertise(self,client,address, gwid, duration):
    m="advertise -address" + str(address)+"qwid= " +str(gwid)+"dur= " +str(duration)
    client.message_q.put(m)
    print ("found gateway at",m)
    ip_address,port=address
    client.GatewayFound=True


  def register(self,client, TopicId, TopicName):
    print("Topic name=",TopicName, "id =",TopicId)
    print("in register")
    client.registered[TopicId] = TopicName
    
  def regack(self,client, TopicId):
    print("in regack id =",TopicId)



class Client:
  ##added by me create gwifo for sending
    def gwinfo(self,multicast_port,multicast_group):
        gwinfo = MQTTSN.GWInfos()
        if self.host!="":
            print("adding host ",type(gwinfo.GwAdd))
            gwinfo.GwAdd=self.host
        m=gwinfo.pack()
        m= m.encode() #turn to bytes

        print(type(m))
        print("address type ",type(gwinfo.GwAdd))
        print("sending GW packet ",gwinfo )
        self.sock.sendto(m,(multicast_group, multicast_port))

    def Search_GWs(self,multicast_port,multicast_group):
        if  not self.multicast_flag:
          self.create_multicast_socket(multicast_port,multicast_group)
         
        searchgw = MQTTSN.SearchGWs()
        #print(type(searchgw))
        m=searchgw.pack()
        #print(type(m))
        m= m.encode() #turn to bytes
        #print(type(m))
        print("sending GW packet ",searchgw)
        #sock2.sendto(m,(s_group, s_port))
        sock2.sendto(m,group)
    def create_multicast_socket(self,multicast_port,multicast_group):
        server_address = ('', multicast_port)
        socket.setdefaulttimeout(0.01)
        group = (multicast_group, multicast_port)
        sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        mreq = struct.pack('4sL', socket.inet_aton(multicast_group), socket.INADDR_ANY) 

        sock2.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        sock2.bind(server_address)#receive advertise mssages
        #create new receiver for multicast

        self.__receiver_gw = MQTTSNinternal.Receivers(sock2,self)
        self.multicast_flag=True


    def find_gateway(self,multicast_port,multicast_group):
        print("in start ",multicast_group)
        self.GatewayFound=False
        if  not self.multicast_flag:
          self.create_multicast_socket(multicast_port,multicast_group)
        

    def __init__(self, clientid="",cleansession=True):
        #self.message_q=queue.Queue()
        self.multicast_flag=False
        self.registered = {}
        self.running_loop=False #set when starting external loop
        self.clientid = clientid
        if clientid=="":
          a=random.randint(0,1000)
          clientid="testclient-"+str(a)
        self.gateway=("",1883)
        self.topic_ack=[]
        self.cleansession=cleansession
        self.msgid = 1
        self.callback = None
        self.connected_flag=False #added
        self.bad_connection_flag=False
        self.puback_flag=False #added
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(0.001)
        self.__receiver = MQTTSNinternal.Receivers(self.sock,self)

        self.suback_flag=False
        self.sub_topicid=""
        self.sub_msgid=""
        self.sub_rc=""
    def start(self):
      self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
      self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      self.sock.settimeout(0.01)

      group = socket.inet_aton(m_group)
      mreq = struct.pack('4sL', group, socket.INADDR_ANY)  
      self.sock.bind(('',m_port))
      self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
      self.startReceiver() 

      
    def stop(self):
        self.loop_stop()

    def __nextMsgid(self):
        def getWrappedMsgid():
            id = self.msgid + 1
            if id == 65535:
                id = 1
            if debug:
                print("in next message id -returning id=", id)
                print("returning",id)
            return id

        if len(self.__receiver.outMsgs) >= 65535:
            raise "No slots left!!"
        else:
            self.msgid = getWrappedMsgid()
            while self.msgid in self.__receiver.outMsgs:
                self.msgid = getWrappedMsgid()
        print("returning",self.msgid)
        return self.msgid


    def registerCallback(self, callback):
        self.callback = callback


    def connect(self,host,port=1883,keepalive=60):
        self.host = host
        self.port = port
        self.bad_connect_flag=False
        self.connected_flag=False
        self.keepalive=keepalive
        
        self.sock.connect((self.host, self.port))

        connect = MQTTSN.Connects()
        connect.ClientId = self.clientid
        connect.CleanSession = self.cleansession
        connect.KeepAliveTimer = self.keepalive
        self.sock.send(connect.pack().encode())





  
    def lookfor(self,msgType):
        if self.__receiver:
          self.__receiver.lookfor(msgType)


    def waitfor(self, msgType, msgId=None): #old
        msg = self.__receiver.waitfor(msgType, msgId)
        #print("the message is",msg)
        return msg
    



    def subscribe(self, topic, qos=2):
        self.suback_flag=False
        self.sub_topicid=""
        self.sub_msgid=""
        self.sub_rc=""
        subscribe = MQTTSN.Subscribes()
        subscribe.MsgId = self.__nextMsgid()
        if type(topic) is str:
            #print("topic is string  ",topic)
            subscribe.TopicName = topic
            if len(topic) > 2:
                subscribe.Flags.TopicIdType = MQTTSN.TOPIC_NORMAL
            else:
                subscribe.Flags.TopicIdType = MQTTSN.TOPIC_SHORTNAME
        else:
            subscribe.TopicId = topic # should be int
            subscribe.Flags.TopicIdType = MQTTSN.TOPIC_PREDEFINED
        subscribe.Flags.QoS = qos
        self.sock.send(subscribe.pack().encode())
        self.lookfor(MQTTSN.SUBACK)
        msg = self.waitfor(MQTTSN.SUBACK, subscribe.MsgId)
        if msg!=None:
          if subscribe.MsgId==msg.MsgId:
            print("received suback for msgid",msg.MsgId)
            print("topicid= ",msg.TopicId)
            return msg.ReturnCode, msg.TopicId
          else:
            raise SystemExit("Subscription failed quitting")
            return (None,None)
        else:
            return (None,None)




    def unsubscribe(self, topics):
        unsubscribe = MQTTSN.Unsubscribes()
        unsubscribe.MsgId = self.__nextMsgid()
        unsubscribe.data = topics
        if self.__receiver:
          self.__receiver.lookfor(MQTTSN.UNSUBACK)
        self.sock.send(unsubscribe.pack().encode())
        msg = self.waitfor(MQTTSN.UNSUBACK, unsubscribe.MsgId)
  
  
    def register(self, topicName):
        register = MQTTSN.Registers()
        register.TopicName = topicName
        
        if self.__receiver:#this uses callbacks
            self.__receiver.lookfor(MQTTSN.REGACK)
            #print("\n\nsending register ",register.pack(),"\n\n")
        self.sock.send(register.pack().encode())
        self.lookfor(MQTTSN.REGACK)
        msg = self.waitfor(MQTTSN.REGACK, register.MsgId)
        if msg:
          return msg.TopicId
        else:
          return None



    def publish(self, topic, payload, qos=0, retained=False):
        publish = MQTTSN.Publishes()
        publish.Flags.QoS = qos
        publish.Flags.Retain = retained
        self.puback_flag=False #reset flag
        if type(topic) == str and len(topic)>2:
          print("invalid topic")
          return None
        if qos in [-1, 0]: #qos 0 or -1
            publish.MsgId = 0
        else:
            publish.MsgId = self.__nextMsgid()
            print("MsgId=", publish.MsgId)
        if type(topic) == int:
            publish.Flags.TopicIdType = MQTTSN.TOPIC_NORMAL
            publish.TopicId = topic

        if type(topic) == str and len(topic)<=2:
            publish.Flags.TopicIdType = MQTTSN.TOPIC_SHORTNAME
            publish.TopicId = topic
            #########

        publish.Data = payload
        a=publish.pack()
        self.sock.send(a.encode())
        self.__receiver.outMsgs[publish.MsgId] = publish
        #self.lookfor(MQTTSN.PUBACK)
        #return(self.waitfor(MQTTSN.PUBACK))
        return publish.MsgId

    def disconnect(self):
        disconnect = MQTTSN.Disconnects()
        self.sock.send(disconnect.pack().encode())
        self.lookfor(MQTTSN.DISCONNECT)
        msg = self.waitfor(MQTTSN.DISCONNECT)
        return msg

    def loop_start_gw(self):#looks for incoming messages
        print("running loop gateway ")
        if self.callback:#only if we have defined callbacks
          print("starting gw loop")
          t = threading.Thread(target=self.__receiver_gw,args=(self.callback,)) #start
          t.start() #start thread
          self.multicast_loop_flag=True
 
    def loop_stop_gw(self):#looks for incoming messages
      self.multicast_loop_flag=False

    
    def loop_start(self):#looks for incoming messages
        print("running loop  ",self.running_loop)
        if self.running_loop: #already created so return
          return
        if self.callback:#only if we have defined callbacks
          print("starting loop")
          self.running_loop=True
          t = threading.Thread(target=self.__receiver,args=(self.callback,)) #start
          t.start() #start thread
          #id = _thread.start_new_thread(self.__receiver, (self.callback,))
          
    def loop_stop(self):
        self.running_loop=False 
        assert self.__receiver.inMsgs == {}
        #assert self.__receiver.outMsgs == {}
        self.__receiver = None
        self.loop_stop_gw()
    def loop(self,interval=.01):
        self.interval=interval #not used
        if self.running_loop: #already created external so return
          return
        self.__receiver.receive(self.callback)


def publish(topic, payload, retained=False, port=1883, host="localhost"):
  publish = MQTTSN.Publishes()
  publish.Flags.QoS = 3
  publish.Flags.Retain = retained  
  if type(topic) == bytes:
    if len(topic) > 2:
      publish.Flags.TopicIdType = MQTTSN.TOPIC_NORMAL
      publish.TopicId = len(topic)
      payload = topic + payload
    else:
      publish.Flags.TopicIdType = MQTTSN.TOPIC_NORMAL
      publish.TopicName = topic
  if type(topic) == str and len(topic)<=2:
    publish.Flags.TopicIdType = MQTTSN.TOPIC_SHORTNAME
    publish.TopicId = topic
  publish.MsgId = 0
  publish.Data = payload
  a=publish.pack()
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  sock.sendto(a.encode(), (host, port))
  sock.close()
  return 
########




