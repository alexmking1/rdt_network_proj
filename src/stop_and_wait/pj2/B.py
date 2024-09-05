from pj2.simulator import to_layer_five
from pj2.packet import send_ack

class B:
    def __init__(self):
        # stop and wait, the initialization of B
        # The state only need to maintain the information of expected sequence number of the packet
        self.seq = 0 #expected seq num...
        self.state = "WAIT_0"

    def output(self, m):
        print("output in B...(not supposed to be used)")

    def B_input(self, pkt):
        # stop and wait, B_input
        # you need to verify the checksum to make sure that packet isn't corrupted
        # If the packet is the right one, you need to pass to the fifth layer "to_layer_five(entity,payload)"
        # Send acknowledgement using "send_ack(entity,seq)" based on the correctness of received packet
        # If the packet is the correct one, in the last step, you need to update its state ( update the expected sequence number)
        if self.state == "WAIT_0" and self.seq == 0:
            # waiting for seq 0 case...still need to check for corruption AND pkt.seq#...
            if pkt.checksum == pkt.get_checksum() and pkt.seqnum == self.seq:
                # both seq and checksum valid so send ack
                to_layer_five("B",pkt.payload.data)
                send_ack("B", self.seq)
                self.state = "WAIT_1"
                self.seq = 1
            else:
                #corrupted/bad packet found... do xyz
                #send packet with ack 1
                send_ack("B",1)

        elif self.state == "WAIT_1" and self.seq == 1:
            # waiting for seq 1 case...
            if pkt.checksum == pkt.get_checksum() and pkt.seqnum == self.seq:
                # both seq and checksum valid so send ack
                to_layer_five("B",pkt.payload.data) # SHOULD I 'MAKE' THIS PACKET HERE?
                send_ack("B", self.seq)
                self.state = "WAIT_0"
                self.seq = 0
            else:
                #corrupted/bad packet found... do xyz
                # send packet with ack 0
                send_ack("B",0)

        else:
            print("ERROR-IMPOSSIBLE state REACHED in B")


    def B_handle_timer(self):
        print("timer handler in B, (shouldnt be used)")


b = B()
