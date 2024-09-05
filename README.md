# Header
Alex King,CSCI4211S23,03/27/2023\
Python3,go_back_n/main.py,,stop_and_wait/main.py

# Compilation
1. install python3
* No additional libraries are required (outside of the standard python libraries)

# Execution
1. Launch the terminal
2. `cd` into the go_back_n folder or the stop_and_wait folder, depending on which of the two simulations you want to run.
    * The following steps will be demonstrating how to run the 'go_back_n' simulation. If you want to run the 'stop_and_wait' simulation instead, simply `cd` into the 'stop_and_wait' folder, and follow the same steps.
3.  If you enter the `ls` command in the terminal, you should see a main.py file along with a pj2 folder.
    * notice there are two main.py files, one for running the **go_back_n** sim, and one for running the **stop_and_wait** sim. Make sure the main.py file you are using corresponds to the sim you intend to run.
    * go_back_n/main.py vs. stop_and_wait/main.py
4. To start the simulation, enter the following command in the terminal: `python3 main.py`
    * You should see a series of output messages describing the events of the simulation, such as which messages have been successfully received and which have been dropped or corrupted: 
5. The settings of the simulations can be adjusted within the simulation.py file that is located in the pj2 folder. (see the **Description** section below for more details)

# Description
This program demonstrates how reliable data-transer protocols (Stop-and-wait & Go-Back-N) can be used to ensure the reliability of messages that are being sent over unreliable networks. This is done by running simulations where messages are being sent from a client to a server (from node A to node B) over a 'simulated' unreliable network. This 'simulated' network tests how robust the protcols are by problematic events such as packet loss or corruption, which are an inherent part of real-life communication over unreliable networks. If the protocols are implemented correctly, the messages being sent from node A should still arrive at node B, despite these simulated 'events'. 
* Each protocol has its own simulation and are run separately. The Stop_and_wait protocol is the more rudimentary, less efficient approach, while the Go-Back-N protocol allows for messages to be sent faster, but has a more complex implentation.
* Adjust the following four variables at the top of the simulation.py file to change the intensity or difficulty of the simulation: self.nsimmax, self.lossprob, self.corruptprob, self.lambda. (see the 4 example tests displayed in the Evaluation section)

# Stop-And-Wait
STOP_AND_WAIT PROTOCOL: with the stop_and_wait protocol, the sender will send one packet and then wait for the acknowledgement (ACK) from the receiver before sending the next packet. The acknowledgement is a mechanism for the sender to know the packet was received. The sender also uses a timer which will resend a packet if there is no ACK from the receiver within a reasonable amount of time. This protocol should be able to handle the scenario when a packet is lost, an ACK is lost and/or a premature timeout. 
* I tried to have my implementation centered around the different states outlined in the stop_and_wait FSM. Some areas of the code my appear inefficient, (such as having multiple if/else sections that could instead be combined into 1 or using a helper function to flip the 1 and 0 sequence numbers instead of hard-coding them) however mirroring the implementation to the FSM states seemed like the better option. 
* **A initialization**: The initialization of A requires more than B because it must maintain a timer, as well as a saved packet in case it needs to be re-sent after a timeout. This self.seq and self.state are used to represent the different states of A. 
* **A_output** implementation: A_ouput accepts a message from the application layer, builds a packet() and sends it to B, depending upon which state it was in, which are what the 2 if/elif conditions are doing. There is also some bookkeepping involved in saving the message with self.savedPacket and maintaining the timer. Once the packet is sent, the state is updated via the self.seq and self.state variables. 
* **A_input** implementation: A_input accepts a pkt from B (aka an ACK), and then verify it's ACK needed to be able to send the next pkt. A_input is setup to first identify which state A is in and then have it's state dictate what the right action for pkt is. If the given pkt passes both the checksum and acknum tests, then we know it's the correct pkt and can cancel the associated timer to prevent the timeout/resend. The state is also updated appropriately like the FSM diagram shows. For example, notice how the state only changes when the given pkt passes the checksum and acknum conditions.
* **A_handle_timer** implementation: In the event of a timeout, we only need to re-send the one packet back to B, which is possible because it's saved as self.savedPacket. Then a timer is started in case the re-sent packet is lost.
* **B initialization**: The initialization of B needs enough variables to be able to define the 'states', which was only the self.seq variable for the expected sequence number and a string self.state to represent the "waiting for ack" or "waiting for msg" state.
* **B_output implementation**: The B_ouput function is setup to first identify which 'state' B currently is in, and then interpret what the given input/packet means based on that state. The main if/else involved are meant represent the two states of the receiver FSM: "wait for 0" or "wait for 1". The packet is sent to layer 5 if it's determined to be what B was waiting for, along with the ACK back, and then most importantly an update to the state.

# Go-Back-N
GO-BACK-N PROTOCOL: Unlike the stop_and_wait approach, go_back_n allows for a certain amount of messages to be sent in a row without needing to wait for the corresponding ACK to come back. This is done with a sliding window of sequence numbers that are tied to packets being sent. The window can be understood as a list, and the size of the window represents the number of packets that can be sent without having an ACK, or another way to put it is the number of un-ACK'd packets allowed to be in the air at one time. Because the packets are being sent almost simultaneously, it creates a 'burst' effect that appears as though many packets were sent at the same. If the window size = 16, then as many as 16 packets can be sent to B at the same time, which is a big improvement from the 'one at a time' approach that stop_and_wait uses. The receiver side handles these bursts by only ACKing the next in-order packet. This helps the sender side as well because if it gets an ACK(n) from the receiver, it knows that any unACK'd packets in the window that come before this 'n', must have already been received, so it also mark those packets as well. This is known as a 'cumulative' ACK, because it's not only expressing that packet 'n' was received, it's also saying that all packets leading up to 'n' were received too. 
* **A initialization**: the instantiation of the buffer is needed to for A's use of the window. The estimated_rtt value is to represent the timer duration. The two variables self.base and self.nextSeqNum represent pointers to help implement the window functionality and the self.timerCheck is a variable I used to ensure at most 1 timer was active.
* **A_output** implementation: A_ouput is meant to accept a message from the application layer, build the packet, add the packet to the buffer/window via a call to push() and start a timer only if this packet was the 'oldest transmitted but not yet ACK'd' packet currently in the window. However, all of this functionality had to be couched in an if/else because we only want to do this if the window has space for more packets (aka isn't currently full)
* **A_input** implementation: A_input accepts a packet (or an ACK) and updates the window accordingly. The difficult part of the implementation was getting the cumulative-ACK behavior because we couldn't simply pop() once for every acknum received. We also had to pop() for each of the packets leading up to a given acknum and after self.base since that's what a cumulative-ACK is for. This is what my loop is doing and the expression to determine the number of times we want to call pop(): numIterations = (pkt.acknum - self.base) + 1. After the pop() calls, we want to make sure to update self.base to be (acknum+1) instead of the basic +1 increment since the new base value could have changed by more than 1 from the multiple pop() calls associated with the cumulative-ACK implementation. 
* **A_handle_timer** implementation: the A_handle_timer function should re-send all un-ACK'd packets from pkt 'n' to all higher sequence number packets that are still within the window. Using the given read_all() function to put these packets into a list and then iterating through the list to re-send each packet. A timer must also be started again since any of these re-sent packets could also timeout and need to be re-sent again. (There is still only 1 timer though)
* **B initialization**: Because B is not maintaining a window like A is, B only needs to know what is the next expected sequence number and how to update it accordingly. This is why the initialization only has the one self.expectedSeqNum variable set to 0. 
* **B_output** implementation: Aside from the basic corruption check with checksum, B's primary job is to examine a packet it receives from A to determine if it's the 'expected' one, then ACK() back if it is the 'expected', otherwise just ACK back the most recent in-order packet that was already ACK'd, which is what the ( 'self.expecteSeqNum' - 1 ) is representing. When the pkt does match the self.expectedSeqNum, then the packet is passed to the fifth layer, the send_ack() is called for A and then the self.expectedSeqNum is incremented since the current one was just ACK'd.

# Evaluation
    TEST-SUITE: the four different test case scenarios below were simulated on both the 'stop_and_wait' and 'go_back_n' protocols. The expected output and analysis is outlined in the PDF.

        TEST-CASE 1 of 4: (no disruptions)
        self.nsimmax = 20
        self.lossprob = 0.0
        self.corruptprob = 0.0
        self.Lambda = 1000

        TEST-CASE 2 of 4: (only packet-loss)
        self.nsimmax = 20 
        self.lossprob = 0.2
        self.corruptprob = 0.0
        self.Lambda = 1000

        TEST-CASE 3 of 4: (only packet-corruption)
        self.nsimmax = 20 
        self.lossprob = 0.0
        self.corruptprob = 0.3
        self.Lambda = 1000 
               
        TEST-CASE 4 of 4: (both packet-loss and packet-corruption)
        self.nsimmax = 20
        self.lossprob = 0.3
        self.corruptprob = 0.3
        self.Lambda = 1000






