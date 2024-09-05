class circular_buffer:
    # you may want to use this data structure to implement the window for the sender
    # do not modify this
    def __init__(self,n):
        self.read=0 #represents the next 'currently occupied' index, for when we POP() [aka det the index of the elem we remove when pop() is called]
        self.write=0 # seems to rep 'nextseqnum' variable --- #represents the next avail index to add pkt to when we PUSH() [aka det the index of the elem we add when push() is called]
        self.max= n 
        self.count=0 #this 'count' seems to act as the 'base' variable
        self.buffer=[]
        for i in range(n):
            self.buffer.append(None)

    # do not modify this
    def push(self,pkt):
        if(self.count==max):#if the list is full, dont push new elem...
            return -1
        else:# if the list is NOT full, then add the given pkt to the list, at index self.write...
            self.buffer[self.write]=pkt

        self.write=(self.write+1)% self.max #increment self.write (but use mod to ensure it stays w/i buff bounds)
        self.count=self.count+1 

    # do not modify this
    def pop(self):
        if(self.count==0):
            return -1

        temp=self.buffer[self.read]
        self.read=(self.read+1)%self.max
        self.count=self.count-1

    # do not modify this
    def read_all(self):
        temp=[]
        read=self.read
        for i in range(self.count):
            temp.append(self.buffer[read])
            read=(read+1)%self.max
        return temp

    # do not modify this
    def isfull(self):
        if(self.count==self.max):
            return True
        else:
            return False
