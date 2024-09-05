from pj2.event import event


class event_list:
    # do not modify this
    def __init__(self):
        self.head = None

    # do not modify this
    def insert(self, p):
        q = self.head
        if (q == None):  # if head is None
            self.head = p
            self.head.next = None
            self.head.prev = None
        else:
            qold = q
            while (q != None and p.evtime > q.evtime):
                qold = q
                q = q.next

            # now qold.next==q, p.evtime<=q.evtime
            if (q == None):
                qold.next = p
                p.prev = qold
                p.next = None

            else:
                if (q == self.head):
                    p.next = q
                    p.prev = None
                    q.prev = p
                    self.head = p
                else:
                    p.next = q
                    p.prev = q.prev
                    p.prev.next = p
                    q.prev = p

    # do not modify this
    def print_self(self):
        q = self.head
        print("--------------\nEvent List Follows:\n")
        while (q != None):
            print("Event time:{} , type: {} entity: {}\n".format(q.evtime, q.evtype, q.eventity))
            q = q.next

        print("--------------\n")

    # do not modify this
    def remove_head(self):
        temp = self.head
        if temp == None:
            return None
        if (self.head.next == None):
            self.head = None
            return temp
        else:
            self.head.next.prev = None
            self.head = self.head.next
            return temp

    # you should call this method to start the timer
    # Make sure that there is only a timer at a time
    # do not modify this
    def start_timer(self, AorB, time):
        from pj2.simulator import sim
        self.insert(event(sim.time+time, "TIMER_INTERRUPT", AorB))

    # you should call this method to remove the timer
    # do not modify this
    def remove_timer(self):
        q = self.head
        while (q.evtype != "TIMER_INTERRUPT"):
            q = q.next

        if q.prev == None:
            self.head = q.next
        elif q.next == None:
            q.prev.next = None
        else:
            q.next.prev = q.prev
            q.prev.next = q.next

evl = event_list()