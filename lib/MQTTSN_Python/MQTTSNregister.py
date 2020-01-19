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

from MQTTSNclient import Callback
from MQTTSNclient import Client
import MQTTSN
import time
broker="192.168.1.159"
port=1884
aclient = Client("register")
aclient.registerCallback(Callback())
#aclient.loop_start()
aclient.connect(broker,port)
result = aclient.register("jkjkjkjkj")
print("result from register 1 is", result)
result = aclient.register("jkjkjkjkj")
print("result from register 1 is", result)
result = aclient.register("jkjkjkjkj2")
print("result from register 2 is", result)
time.sleep(8)
#aclient.loop_stop()
