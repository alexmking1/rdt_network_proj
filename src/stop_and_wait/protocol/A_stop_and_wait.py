from pj2.simulator import sim
from pj2.simulator import to_layer_three
from pj2.event_list import evl
from pj2.packet import *

#WAIT_LAYER5 == initial state, b4 sent pkt to rcv side
#WAIT_ACK == state after sent pkt to rcv side

# HOW TO SAVE PACKET SO CAN BE USED IN TIME-OUT FUNCTION RE-SEND...
# HOW TO CALC CHECKSUM ON THE SENDER SIDE AND THEN USE IT AS ARG FOR PACKET CREATION...
# HOW MANY THINGS NEED TO BE INITIALIZED?
class A:
    def __init__(self):
        # stop and wait, the initialization of A
        # for stop and wait, the state can be "WAIT_LAYER5" or "WAIT_ACK"
        # "WAIT_LAYER5" is the state that A waits messages from application layer.
        # "WAIT_ACK" is the state that A waits acknowledgement
        # You can set the estimated_rtt to be 30, which is used as a parameter when you call start_timer
        self.seq = 0
        self.estimated_rtt = 30
        self.state = "WAIT_LAYER5"
        self.savedPacket = packet() # attempting to have mechanism to save pkt 
        self.timerCheck = 0
        return

    def A_output(self, m):
        # stop and wait A_output
        # msg m is the message. It should be used as payload to construct the packet.
        # You can construct the packet using the "packet(seqnum,payload)" in "packet.py".
        # call to_layer_three(entity,pkt) to send the packet
        # save the packet so that it can be resent if needed.
        # Set the timer using "evl.start_timer(entity,time)", and the time should be set to estimated_rtt. Make sure that there is only one timer started in the event list.
        # In the end, you should change the state to "WAIT_ACK"
        # STATE 1 CASE -> WAIT_LAYER5-0        
        if self.state == "WAIT_LAYER5" and self.seq == 0:
            myPacket = packet(self.seq, 0, m)
            self.savedPacket = myPacket
            to_layer_three("A", myPacket)
            if self.timerCheck == 0:
                evl.start_timer("A",self.estimated_rtt)
                self.timerCheck = 1
            self.state = "WAIT_ACK"
        
        # STATE 2 CASE -> WAIT_LAYER5-1
        elif self.state == "WAIT_LAYER5" and self.seq == 1:
            myPacket = packet(self.seq, 1, m)
            self.savedPacket = myPacket
            to_layer_three("A", myPacket)
            if self.timerCheck == 0:
                evl.start_timer("A",self.estimated_rtt)
                self.timerCheck = 1
            self.state = "WAIT_ACK"
            #print("TEST HERE")

        elif self.state == "WAIT_ACK":
            #print("DROPPED DUE TO NO-BUFFER... ")
            print("DROPPED:" + m.data)


    def A_input(self, pkt):
        # stop and wait A_input
        # p is the packet from the B
        # first verify the checksum to make sure that packet is uncorrupted
        # then verify the acknowledgement number to see whether it is the expected one
        # if not, you may need to resend the packet.
        # if the acknowledgement is the expected one, you need to update the state of A from "WAIT_ACK" to "WAIT_LAYER5" again
        # STATE 3 CASE -> WAIT_ACK0 state
        if self.state == "WAIT_ACK" and self.seq == 0:
            #were in the WAIT_ACK0 state... 3 diff options from this state, 2 of which are taken care of by default
            if pkt.checksum == pkt.get_checksum() and self.seq == pkt.acknum:
                # both checksum & acknum good so we can stop timer
                if self.timerCheck == 1:
                    evl.remove_timer()
                    self.timerCheck = 0
                self.state = "WAIT_LAYER5"
                self.seq = 1

        # STATE 4 CASE -> WAIT_ACK1 state
        elif self.state == "WAIT_ACK" and self.seq == 1:
            #were in the WAIT_ACK1 state...
            if pkt.checksum == pkt.get_checksum() and self.seq == pkt.acknum:
                # both checksum & acknum good so we can stop timer and change state accordingly...
                if self.timerCheck == 1:
                    evl.remove_timer()
                    self.timerCheck = 0
                self.state = "WAIT_LAYER5"
                self.seq = 0
        else:
            #print("ERROR: IMPOSSIBLE STATE REACHED")
            x = 1+1

    def A_handle_timer(self):
        # stop and wait A_handle_timer
        # if it is triggered, it means the packet isn't delivered
        # so you need to resend the last packet "using to_layer_three()"
        # After sending the last packet, don't forget to set the timer again
        to_layer_three("A", self.savedPacket)
        evl.start_timer("A", self.estimated_rtt)

a = A()
