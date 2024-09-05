from pj2.simulator import sim
from pj2.simulator import to_layer_three
from pj2.event_list import evl
from pj2.packet import *
from pj2.circular_buffer import circular_buffer

class A:
    def __init__(self):
        # go back n, the initialization of A
        # Initialize the initial sequence number to 0.
        # You need to initialize the circular buffer, using "circular_buffer(max)". max is the number of the packets that the buffer can hold
        # You can set the estimated_rtt to be 30, which is used as a parameter when you call start_timer
        self.seq = 0
        self.estimated_rtt = 30

        self.myMax = 8
        self.myBuff = circular_buffer(self.myMax)

        #OPTION1: using LOCAL variables for 'base' and 'nextseqnum'
        self.base = 0
        self.nextSeqNum = 0
        #self.nextSeqNum = self.base + self.myMax

    def A_output(self, m): # 2 BASIC CASES TO HANDLE...
        # go back n, A_output
        # If the buffer is full, just drop the packet
        # Construct the packet based on the message. Make sure that the sequence number is correct
        # Send the packet and save it to the circular buffer using "push()" of circular_buffer
        # Set the timer using "evl.start_timer(entity, time)", and the time should be set to estimated_rtt. Make sure that there is only one timer started in the event list
        
        #CASE: 'window IS full'...
        if self.myBuff.isfull(): # window IS full, so cannot send another packet (bc GBN allows to send a 'window-size' num of packets at a time before needing any ACKs) 
            print("DROPPED BC WINDOW FULL?:" + m.data)
        
        #CASE: 'window NOT full'...
        else: #window is NOT full... so we CAN send another packet b4 reaching the max num packets that can be sent b4 requiring ACK's 
            #make pkt, send it via to_layer_three(), add it to buffer via circular_buffer.push(), 
            myPacket = packet(self.nextSeqNum, 0, m) # NOT SURE ABOUT 2nd ARG HERE which is supposed to be 'acknum'
            self.myBuff.push(myPacket) # CHANGING THE 'self.SAVE-PACKET' step of stop&wait, into the 'ADD-PKT-TO-BUFFER' step for 'goBackN'. ---- DONT NEED THIS LINE BC WE DONT NEED TO SAVE PKT FOR RE-SEND like in rdt3.0 bc they'll already be saved/avail in the buffer in case we need to re-send ...
            to_layer_three("A", myPacket) #sending pkt

            if self.myBuff.count == self.myBuff.write: #(aka checking if base == nextseqnum) --- this means the pkt we're dealing with IS the 'oldest transmitted, but not yet ACK'd' pkt, and therefore we want to tie it to the timer
                #quick check to make sure there isn't an active timer already...
                if self.timerCheck == 0: # this means currently no timer active
                    evl.start_timer("A", self.estimated_rtt)
                    self.timerCheck = 1
                elif self.timerCheck == 1: #this means there IS an active timer --(so should remove it b4 starting new one in order to maintain the 'at most 1' timer req...)
                    evl.remove_timer()
                    self.timerCheck = 0
                    # now can add the new timer...
                    evl.start_timer("A", self.estimated_rtt)
                    self.timerCheck = 1
            self.nextSeqNum = (self.nextSeqNum + 1) #incrementing nextseqnum now that we added/sent another packet
            #self.myBuff.write = (self.myBuff.write + 1) #incrementing the 'nextseqnum' variable so it stays representing the next avail index for push()
            
            












    def A_input(self, pkt):
        # go back n, A_input
        # Verify that the packet is not corrupted
        # Update the circular buffer according to the acknowledgement number using "pop()"

        # CASE: rcv pkt and it's NOT corrupt...[box2 on FSM]
        if pkt.checksum == pkt.get_checksum(): #this means packet is NOT corrupt...
            self.base = (pkt.acknum + 1) # Update base variable/ptr
            self.myBuff.pop()

            # checking if we should remove or start a timer...
            if self.base == self.nextSeqNum: # this means we must REMOVE() timer...
                if self.timerCheck == 1: #check timer exists before remove() call
                    evl.remove_timer()
                    self.timerCheck = 0 # '0' indicates there's no active timer
            else:
                if self.timerCheck == 0: #check no timer exists before starting new one...
                    evl.start_timer("A", self.estimated_rtt)
                    self.timerCheck = 1 # '1' indicates there IS an active timer (so DONT start another until this one is removed)
        
        # CASE: rcv pkt and IS corrupt... [box1 on FSM]
        else:# this means packet IS corrupt, so should ignore/do-nothing...
            print("received a packet that IS corrupt, so ignoring it...")



    def A_handle_timer(self):
        # go back n, A_handle_timer
        # Read all the sent packet that it is not acknowledged using "read_all()" of the circular buffer and resend them
        # If you need to resend packets, set a timer after that
        # CASE: timeout: [box3 on FSM]
        tempList = self.myBuff.read_all() # this should be a list of the packets we need to re-send, so just need to iterate through the list & do 'resend' call for each elem
        for i in range(len(tempList)): # loop to re-send all the un-ack'd packets from 'seq# of pkt tied to timeout' to (nextSeqNum -1)
            to_layer_three("A", tempList[i]) # RE-SENDING the PACKET at index 'i' in list...
            if i == 0: # this means we are re-sending the 'oldest transmitted but not yet ACKd' pkt, so should start the timer here, instead of before the loop or after the loop finishes)
                if self.timerCheck == 1: print("WARNING FIX ME!!: we started a new timer w/o removing the current one...")
                evl.start_timer("A", self.estimated_rtt)
                self.timerCheck = 1
        
        

        



a = A()
