from pj2.simulator import to_layer_five
from pj2.packet import send_ack


class B:
    def __init__(self):
        # go back n, the initialization of B
        # The state only need to maintain the information of expected sequence number of packet
        self.expectedSeqNum = 0
        return

    def B_output(self, m):
        print("output in B...(not supposed to be used)") #aka LEAVE THIS FUNCTION EMPTY
        return

    def B_input(self, pkt):
        # go back n, B_input
        # You need to verify the checksum to make sure that packet isn't corrupted
        # If the packet is the right one, you need to pass to the fifth layer using "to_layer_five(entity,payload)"
        # Send acknowledgement using "send_ack(entity, seq)" based on the correctness of received packet
        # If the packet is the correct one, in the last step, you need to update its state ( update the expected sequence number)
        
        # CASE1: rcv pkt that's NOT corrupt and has the EXPECTED seqnum --- [box1 of FSM]
        if pkt.checksum == pkt.get_checksum() and pkt.seqnum == self.expectedSeqNum:
                to_layer_five("B",pkt.payload.data)
                send_ack("B", self.expectedSeqNum)
                self.expectedSeqNum = (self.expectedSeqNum + 1) #incrementing expectedSeqNum since we just recevied the 'expected' one
        
        # CASE2: rcv 'corrupt pkt' or 'UNexpected seq' --- [box2 of FSM]
        else:
            # discard the pkt and re-send an ACK for the most recently received 'in-order' pkt
            send_ack("B", (self.expectedSeqNum -1))
        return

    def B_handle_timer(self): #
        print("timer handler in B, (should NOT be being used)") #aka LEAVE THIS FUNCTION EMPTY
        return
b = B()
