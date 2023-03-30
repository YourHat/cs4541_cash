############################################
#       CS4541
#       Cache Simulator
#       Yutaroh Tanaka
#       yutaroh.tanaka@wmich.edu
###########################################

import sys #to get argv 

h = False #optional help flag that prints usage info
v = False #optional verbose flag that displays trace info
s = 0 #Numberof set index bits (2**s)
e = 0 #Associativity (number of lines per set)
b = 0 #Number of block bits (2**b)
t = "" #Name of the valgrind trace to play

cache_2d = [] #cache 2d list

h_n = 0 #amount of hit
m_n = 0 #amount of miss
e_n = 0 #amount of eviction

#class for each block of cache memory
class C_set:
    def __init__(self):
        self.v = 0
        self.tag = None
        self.block = None

    def get_v(self):
        return self.v

    def set_v(self):
        self.v = 1

    def get_tag(self):
        return self.tag

    def set_tag(self, tag):
        self.tag = tag


#main function called at the begining
def main(arg):
    try: #error handing for bad input
        set_arg(arg) #get and assign value from the command line arguments
        cache(s,e) #create virtual cache memory 

    
        if h: #if user put -h
            print("Usage: python3 cache.py  [-hv] -s <s> -E <E> -b <b> -t <tracefile>\n-h: Optional help flag that prints usage info\n-v: Optional verbose flag that displays trace info\n-s <s>: Number of set index bits (S = 2 s is the number of sets)\n-E <E>: Associativity (number of lines per set)\n-b <b>: Number of block bits (B = 2 b is the block size)\n-t <tracefile>: Name of the valgrind trace to replay)")
        elif v: #if user put -v
            with open(t,"r") as f: #open file with with
                for line in f: # read everyline
                    if line[0] == " ":
                        resul = line[:-1] #either L,S,or M
                        match line[1]:
                            case "L":
                                resul += load(line[3:])
                            case "S":
                                resul += store(line[3:])
                            case "M":
                                resul += load(line[3:])
                                resul += store(line[3:])
                        print(resul)
        else: #if user did not put -h nor -v
            with open(t,"r") as f: #open file with with
                for line in f: #read every line
                    if line[0] == " ":
                        resul = line[:-1] #either L,S, or M
                        match line[1]:
                            case "L":
                                resul += load(line[3:])
                            case "S":
                                resul += store(line[3:])
                            case "M":
                                resul += load(line[3:])
                                resul += store(line[3:])
                
        print("hits:{} misses:{} evictions:{}".format(h_n,m_n,e_n)) #print the result
    except: #if user input is bad
        print("Bad input\nUsage: python3 cache.py  [-hv] -s <s> -E <E> -b <b> -t <tracefile>\n-h: Optional help flag that prints usage info\n-v: Optional verbose flag that displays trace info\n-s <s>: Number of set index bits (S = 2 s is the number of sets)\n-E <E>: Associativity (number of lines per set)\n-b <b>: Number of block bits (B = 2 b is the block size)\n-t <tracefile>: Name of the valgrind trace to replay)")

def set_arg(arg): #get the command line argumants and then assign them
    global h,v,s,e,b,t
    for i in range(len(arg)):
        match arg[i]:
            case "-h":
                h = True 
            case "-v":
                v = True
            case "-s":
                s = int(arg[i+1])
            case "-E":
                e = int(arg[i+1])
            case "-b":
                b = int(arg[i+1])
            case "-t":
                t = arg[i+1]
            

def cache(s,e): # create virtual cache
    global cache_2d
    for i in range(2**s):
        cache_1d = []
        for j in range(e):
            cache_1d.append(C_set())
        cache_2d.append(cache_1d)


def load(addr): # if type of memory access is L
    global cache_2d, h_n, m_n, e_n
    result = ""
    s1 = addr.split(",")[0] #get the address
    s2 = int(s1, 16) #chenge from hex to int
    s3 = s2>>b # right shift number of bit for block
    s4 = s3&((2**s)-1) # get which set of cache it fits by using & 111....
    s5 = s3>>s # shift number of bit for set to get tag value
    #print(s1)
    #print("set ",s4, " tag ",s5)
    for i in cache_2d[s4]:
        if i.get_tag() == s5:
            result += " hit"
            #print("hit")
            h_n += 1
        if i.get_tag() != s5:
            #print("miss")
            result += " miss"
            m_n += 1
            i.set_tag(s5)
            if i.get_v() == 1:
                #print("eviction")
                result += " eviction"
                e_n += 1
            i.set_v()
    return result

def store(addr): #if type of memory access is M
    global cache_2d, h_n, m_n, e_n
    result = ""
    s1 = addr.split(",")[0] #get the address
    s2 = int(s1, 16) #change from hex to int
    s3 = s2>>b #right shift number of bit for block
    s4 = s3&((2**s)-1) #get which set of cache it fits by using & 11....
    s5 = s3>>s #shift number of bit for set to get tag value
    #print(s1)
    #print("set ",s4, " tag ",s5)
    for i in cache_2d[s4]:
        if i.get_tag() == s5:
            result += " hit"
            #print("hit")
            h_n += 1
        if i.get_tag() != s5:
            #print("miss")
            result += " miss"
            m_n += 1
            i.set_tag(s5)
            if i.get_v() == 1:
                #print("eviction")
                result += " eviction"
                e_n += 1
            i.set_v()
    return result


if __name__ == "__main__": 
    main(sys.argv) #call main with command line arguments

