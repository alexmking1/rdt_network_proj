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
        #self.seq = 0
        self.estimated_rtt = 30

        self.myMax = 8
        self.myBuff = circular_buffer(self.myMax)

        self.base = 0
        self.nextSeqNum = 0
        self.timerCheck = 0
    





    def A_output(self, m): # 2 BASIC CASES TO HANDLE...
        # go back n, A_output
        # If the buffer is full, just drop the packet
        # Construct the packet based on the message. Make sure that the sequence number is correct
        # Send the packet and save it to the circular buffer using "push()" of circular_buffer
        # Set the timer using "evl.start_timer(entity, time)", and the time should be set to estimated_rtt. Make sure that there is only one timer started in the event list

        #CASE: 'window IS full'...
        if self.myBuff.isfull(): # OR USE THIS CONDITIONAL: if self.myBuff.isfull(): 
            print("DROPPED PKT: (WINDOW FULL) ===> " + m.data) # window IS full, so cannot send another packet (bc GBN allows to send a 'window-size' num of packets at a time before needing any ACKs) 

        #CASE: 'window is NOT full'...
        else: #window is NOT full... so we CAN send another packet b4 reaching the max num packets that can be sent b4 requiring ACK's 
            #make pkt, send it via to_layer_three(), add it to buffer via circular_buffer.push(), 
            self.nextSeqNum = self.base + self.myBuff.count #updating nextSeqNum CORRECTLY...(not just incrementing)
            myPacket = packet(self.nextSeqNum, 0, m) 
            self.myBuff.push(myPacket) # CHANGING THE 'self.SAVE-PACKET' step of stop&wait, into the 'ADD-PKT-TO-BUFFER' step for 'goBackN'. ---- DONT NEED THIS LINE BC WE DONT NEED TO SAVE PKT FOR RE-SEND like in rdt3.0 bc they'll already be saved/avail in the buffer in case we need to re-send ...
            to_layer_three("A", myPacket) #sending pkt

            if self.base == self.nextSeqNum: #(aka checking if base == nextseqnum) --- this means the pkt we're dealing with IS the 'oldest transmitted, but not yet ACK'd' pkt, and therefore we want to tie it to the timer
                #quick check to make sure there isn't an active timer already...
                if self.timerCheck == 0: # this means currently no timer active
                    evl.start_timer("A", self.estimated_rtt)
                    self.timerCheck = 1
                elif self.timerCheck == 1: #[THIS elif IS PROBABLY NOT NEEDED SINCE SHOULD BE UNREACHABLE, but keeping for now] #this means there IS an active timer --(so should remove it b4 starting new one in order to maintain the 'at most 1' timer req...)
                    evl.remove_timer()
                    self.timerCheck = 0
                    # NOW can start the new timer...
                    evl.start_timer("A", self.estimated_rtt)
                    self.timerCheck = 1

            #self.nextSeqNum = (self.nextSeqNum + 1) #incrementing nextseqnum now that we added/sent another packet
            
            

    def A_input(self, pkt): 
        # go back n, A_input
        # Verify that the packet is not corrupted
        # Update the circular buffer according to the acknowledgement number using "pop()"
        # CASE: rcv pkt and its NOT corrupt...[box2 on FSM]
        if pkt.checksum == pkt.get_checksum(): #this means packet is NOT corrupt...
            #print("A SIDE ::: "+ "[base => " + str(self.base) + "]---[pkt.acknum => " + str(pkt.acknum) + "]<---- end") 
            if self.base <= pkt.acknum:
                #print("base is reading as..."+str(self.base))
                #print("pkt.acknum is reading as..."+str(pkt.acknum))

                #numIterations = (pkt.acknum - self.base)
                numIterations = (pkt.acknum - self.base) + 1

                self.base = (pkt.acknum + 1)
                for i in range(numIterations):
                    self.myBuff.pop()
                            
                #check if the updated base is the 'oldest transmitted etc...' pkt...
                if self.base == self.nextSeqNum: 
                    if self.timerCheck == 1: #checking to make sure a timer exists before we call remove_timer()... 
                        evl.remove_timer()
                        self.timerCheck = 0 # '0' indicates there's no active timer
                else:
                    if self.timerCheck == 0:
                        evl.start_timer("A", self.estimated_rtt)
                        self.timerCheck = 1 # '1' indicates there IS an active timer (so DONT start another until this one is removed)
            elif self.base > pkt.acknum or pkt.acknum > (self.base + self.myMax):
                # this means the given packet is outside window bounds (either too low or too high)
                # LIKELY CAN REMOVE THIS elif ALL TOGETHER and ONLY HAVE THE IF() up top
                # print("acknum out of bounds")
                x = 1+2


        # CASE: rcv pkt and IS corrupt... [box1 on FSM]
        else:# this means packet IS corrupt, so should ignore/do-nothing...
            print("*****[CORRUPT PKT]***** ")
            # print(pkt) # <pj2.packet.packet object at 0x7f8b2cbeffa0>
            # print(pkt.acknum) # 0
            # print(pkt.payload) # 0
            #print(pkt.payload.data) # ERROR
            #print(">>>>>>data recieved：{}".format(pkt.payload.data))
            #print(">>>>>>data recieved：{}".format(pkt.payload))


















    def A_handle_timer(self):
        # go back n, A_handle_timer
        # Read all the sent packet that it is not acknowledged using "read_all()" of the circular buffer and resend them
        # If you need to resend packets, set a timer after that
        # CASE: timeout: [box3 on FSM]
        self.timerCheck = 0 # the timer is automatically removed when it times out, so i need to update this flag to reflect that...
        tempList = self.myBuff.read_all() # this should be a list of the packets we need to re-send, so just need to iterate through the list & do 'resend' call for each elem
        #print("TIMEOUT EVENT!! Size of Resend List is reading as ==> " + str(len(tempList)))

        for i in range(len(tempList)): # loop to re-send all the un-ack'd packets from 'seq# of pkt tied to timeout' to (nextSeqNum -1)
            #print("seq num: " + str(tempList[i].seqnum))
            #print("RESENDING PACKET w seqnum == " + str(tempList[i].seqnum))
            print("RESENDING THIS PACKET: ==> " + str(tempList[i].payload.data))
            to_layer_three("A", tempList[i]) # RE-SENDING the PACKET at index 'i' in list...
            
            if i == 0: # this means we are re-sending the 'oldest transmitted but not yet ACKd' pkt, so should start the timer here, instead of before the loop or after the loop finishes)
                #starting new timer, but first checking if need to remove any active timer beforehand...
                if self.timerCheck == 0:
                    evl.start_timer("A", self.estimated_rtt)
                    self.timerCheck = 1
                elif self.timerCheck == 1:
                    evl.remove_timer()
                    self.timerCheck = 0
                    evl.start_timer("A", self.estimated_rtt)
                    self.timerCheck = 1
                else:
                    print("INVALID STATE REACHED!!!!!")


    # # this function should ensure we only have 1 timer at a time, and handle all the cases
    # def improvedStartTimer(self, tCheck):
    #     #CASE 1: start a timer when no other timer's exist (aka when tCheck == 0)
    #     if tCheck == 0:
    #         evl.start_timer("A", self.estimated_rtt)
    #         self.timerCheck = (self.timerCheck + 1)

    #     #CASE 2: [aka RESTART timer] start timer when there's another active timer (aka when tCheck == 1)
    #     elif tCheck == 1:
    #         evl.remove_timer
    #         self.timerCheck = (self.timerCheck - 1)

    #         evl.start_timer("A", self.estimated_rtt)
    #         self.timerCheck = (self.timerCheck + 1)
        
    #     else:
    #         print("________timerCheck holds INVALID IMPOSSIBLE value, FIX ME!!!_______")
        

    # # this function should ensure we stop/remove a timer correctly...
    # def improvedStopTimer(self, tCheck):
    #     # CASE 1: stop a timer when there are no active timers to stop...
    #     if tCheck == 0:
    #         x = 1+2
    #     # CASE 2: stop a timer that does exist...
    #     elif tCheck == 1:
    #         evl.remove_timer
    #         self.timerCheck = (self.timerCheck - 1)
    #     else:
    #         print("timerCheck in REMOVE TIMER holds INVALID IMPOSSIBLE value, FIX ME!!!")



a = A()
