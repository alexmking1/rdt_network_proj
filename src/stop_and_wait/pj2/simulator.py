from pj2.msg import *
from pj2.event_list import *
from pj2.event import *

import random
import copy


class simulator:
    def __init__(self):
    # you may want to change the following parameters to adjust the characteristics of the communication channels
        #DEFAULT SIM VALUES: (uncomment for final submission)
        self.nsimmax = 20  # number of msgs to generate, then stop
        self.lossprob = 0.3 # probability that a packet is dropped, default == 0.3
        self.corruptprob = 0.2  # probability that one bit is packet is flipped, default = 0.2
        self.Lambda = 1000  # arrival rate of messages from layer 5

        # # SIM VALUES FOR TESTING...(comment-out for final submission)
        # self.nsimmax = 20  # number of msgs to generate, then stop
        # self.lossprob = 0.3 # probability that a packet is dropped, default == 0.3
        # self.corruptprob = 0.3  # probability that one bit is packet is flipped, default = 0.2
        # self.Lambda = 1000  # arrival rate of messages from layer 5

        # STOP_AND_WAIT TESTS...

        # TEST-CASE 1 of 4 (stop-and-wait)
        # self.nsimmax = 20
        # self.lossprob = 0.0
        # self.corruptprob = 0.0
        # self.Lambda = 1000

        # # TEST-CASE 2 of 4 (stop-and-wait)
        # self.nsimmax = 20 
        # self.lossprob = 0.2
        # self.corruptprob = 0.0
        # self.Lambda = 1000

        # TEST-CASE 3 of 4 (stop-and-wait)
        # self.nsimmax = 20 
        # self.lossprob = 0.0
        # self.corruptprob = 0.3
        # self.Lambda = 1000 
               
        # TEST-CASE 4 of 4 (stop-and-wait)
        # self.nsimmax = 20
        # self.lossprob = 0.3
        # self.corruptprob = 0.3
        # self.Lambda = 1000

        
        self.TRACE = 0  # for your debugging


        self.nsim = 0  # number of messages from 5 to 4 so far
        self.ntolayer3 = 0  # number sent into layer 3
        self.nlost = 0  # number lost in media
        self.ncorrupt = 0  # number corrupted by media
        self.time = 0.0  # initialize time to 0.0

        self.envlist = evl # defined in event.py

        self.generate_next_arrival()  # insert the first event for the simulator to process

# do not modify this
    def generate_next_arrival(self):
        time = self.time + self.Lambda
        self.envlist.insert(event(time, "FROM_LAYER5", "A"))
        return

# do not modify this
    def run(self):
        while (1):
            env = self.envlist.remove_head()
            if env == None:
                print("simulation end!")
                return
            else:
                #env.print_self()
                self.time = env.evtime

            if self.nsim == self.nsimmax:
                print("simulation end")
                return

            if env.evtype == "FROM_LAYER5":
                self.generate_next_arrival()
                ch = chr(97 + self.nsim % 26)
                m = msg(ch)
                self.nsim = self.nsim + 1
                if env.eventity == "A":
                    from pj2.A import a
                    a.A_output(m)
                else:
                    from pj2.A import b
                    b.B_output(m)

            elif env.evtype == "FROM_LAYER3":
                pkt2give = env.pkt
                if env.eventity == "A":
                    from pj2.A import a
                    a.A_input(pkt2give)
                else:
                    from pj2.B import b
                    b.B_input(pkt2give)

            elif env.evtype == "TIMER_INTERRUPT":
                if env.eventity == "A":
                    a.A_handle_timer()
                else:
                    b.B_handle_timer()

            else:
                print("!!!!!!!????")

# do not modify this
def to_layer_three(AorB, pkt):
    if random.uniform(0, 1) < sim.lossprob:
        return

    packet = copy.deepcopy(pkt)

    if random.uniform(0, 1) < sim.corruptprob:
        if packet.payload!=0:
            packet.payload.data = packet.payload.data[0:-1] + "*"
        else:
            packet.seqnum=-1

    q = sim.envlist.head
    lasttime = sim.time
    while q != None:
        if q.eventity == AorB and q.evtype == "FROM_LAYER3":
            lasttime = q.evtime

        q=q.next

    eventime = lasttime + 1 + 9 * random.uniform(0, 1)
    if AorB == "A":
        sim.envlist.insert(event(eventime, "FROM_LAYER3", "B", packet))
    else:
        sim.envlist.insert(event(eventime, "FROM_LAYER3", "A", packet))

# do not modify this
def to_layer_five(AorB, data):
    print("data recieved：{}".format(data))


sim = simulator()
