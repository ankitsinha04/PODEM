# reading Text file
import sys
import logging
import random
import matplotlib.pyplot as plt

class PODEM:
    def __init__(self):
        self.gateData ={}
        self.numberOfNets=0
        self.netValues = []
        self.Dfrontier = []
        self.POs=[]
        self.PIs = []
        self.flag = 0
        self.outputgates = {}
        self.historylist=[]
        self.historygate=[]        

    def GetGateData(self):
        count=1
        inputfile = sys.argv[1] + ".txt"
        self.GateFile = open(inputfile,"r")
        for line in self.GateFile:
            line_split = line.split("\r\n")[0]
            l=[]
            l1= ((line_split.split(' '))[1: ])
            for i in l1:
                l.append(int(i));
            if line_split.split(' ')[0] == "INPUT" or line_split.split(' ')[0] == 'OUTPUT':
                self.gateData[line_split.split(' ')[0] ] = l
            else:
                self.gateData[str(count) + ":" + line_split.split(' ')[0] ] = l
            count=count+1;
        for v in self.gateData.values():
            if v:
                self.numberOfNets = max(self.numberOfNets , max(v))    
        self.POs = self.gateData['OUTPUT']
        self.PIs = self.gateData['INPUT']
        
        
    def InitializeNetData(self):
        for i in xrange(self.numberOfNets):
            self.netValues.append('x')
            self.outputgates[i] = []
        
        self.outputgates[self.numberOfNets] =[]
            
        for i in xrange(self.numberOfNets +1):
            for key in self.gateData:
                if not(key=='INPUT' or key=="OUTPUT"):
                    gate = key[key.index(':')+1 : ]
                    pos=2
                    if gate == 'INV' or gate =='BUF':
                        pos=1
                    if self.gateData[key]==[]:
                        continue
                    if self.gateData[key][pos] == i:
                        l = self.outputgates[i]
                        l.append(key)
                        self.outputgates[i]=l
            
    
    def AND(self,a ,b):
        if a=='0' or b=='0':
            return '0'
        if a=='x' or b=='x':
            return 'x'
        if a=='1' :
            return b
        if b=='1':
            return a
        if a == b:
            return a
        return '0'
    
    def OR(self,a,b):
        if a=='1' or b=='1':
            return '1'
        if a=='x' or b=='x':
            return 'x'
        if a=='0':
            return b
        if b=='0':
            return a
        if a == b:
            return a
        return '1'
    
    def NAND(self,a,b):
        if a=='0' or b=='0':
            return '1'
        if a=='x' or b=='x':
            return 'x'
        if a=='1':
            if b =='1':
                return '0'
            if b == 'D':
                return 'Dbar'
            return 'D'
        if b=='1':
            if a=='D':
                return 'Dbar'
            return 'D'
        if a=='D' and b=='D':
            return 'Dbar'
        if a=='Dbar' and b=='Dbar':
            return 'D'    
        return '1'
    
    def NOR(self,a,b):
        if a=='1' or b=='1':
            return '0'        
        if a=='x' or b=='x':
            return 'x'
        if a=='0':
            if b =='0':
                return '1'
            if b == 'D':
                return 'Dbar'
            return 'D' 
        if b=='0':
            if a=='D':
                return 'Dbar'
            return 'D'        
        if a=='D' and b=='D':
            return 'Dbar'
        if a=='Dbar' and b=='Dbar':
            return 'D'    
        return '0'        
        
    def INV(self,a):
        if a=='x':
            return a
        if a=='0':
            return '1'
        if a=='1':
            return '0'
        if a=='D':
            return 'Dbar'
        return 'D'
    
    def BUF(self,a):
        return a
    
    
        

    
    def UpdateDfrontier(self):
        self.Dfrontier=[]
        for key in self.gateData:
            if key == "INPUT" or key == "OUTPUT":
                continue          
            gate = key[key.index(':')+1 : ]
            if gate == 'INV' or gate =='BUF':  
                continue
            templist = self.gateData[key]
            
            if self.netValues[templist[2]-1] == 'x':
                if (self.netValues[templist[0]-1] == 'D' or self.netValues[templist[0]-1] == 'Dbar') and self.netValues[templist[1]-1] == 'x' :
                    self.flag=1
                    self.Dfrontier.append(key)
                if (self.netValues[templist[1]-1] == 'D' or self.netValues[templist[1]-1] == 'Dbar') and self.netValues[templist[0]-1] == 'x':
                    self.Dfrontier.append(key)   
                    self.flag=1
            self.Dfrontier=self.Dfrontier[::-1] 
        return
    
    def ForwardXPath(self):
        for key in self.gateData:
            if key == "INPUT" or key == "OUTPUT":
                continue          
            gate = key[key.index(':')+1 : ]
            if gate == 'INV' or gate =='BUF':  
                continue
            templist = self.gateData[key]
            
            if (self.netValues[templist[0]-1] == 'D' or self.netValues[templist[0]-1] == 'Dbar') and (self.netValues[templist[2]-1] == 'D' or self.netValues[templist[2]-1] == 'Dbar') :
                    return 
            if (self.netValues[templist[1]-1] == 'D' or self.netValues[templist[1]-1] == 'Dbar') and (self.netValues[templist[2]-1] == 'D' or self.netValues[templist[2]-1] == 'Dbar'):
                return 
        self.flag=1        
        return    
        
    
    

    def Objective(self , fault_node , stuck_at_value):
               
            
        if self.netValues[fault_node -1] == 'x' or self.netValues[fault_node -1] == stuck_at_value :
            if stuck_at_value=='0':
                return [fault_node , '1']
            else:
                return [fault_node ,'0']
            
        else:
            gate = self.Dfrontier[0]
            i=0
            netID=0
            while(True):
                gate = self.Dfrontier[i]
                gatelist = self.gateData[gate]
                if(self.netValues[gatelist[1]-1] == 'x'):
                    netID=gatelist[1]
                    break
                if(self.netValues[gatelist[0]-1] == 'x'):
                    netID=gatelist[0]
                    break
                i+=1
                if i==len(self.Dfrontier):
                    break
            if netID==0:
                print 'No X Path possible'
            
            key = gate[gate.index(':')+1 : ]
            if key=="AND" or key =="NAND":
                return [netID , '1']
            if key=="OR" or key == "NOR":
                return [netID , '0']  
            
        
    def BackTrace(self, netID, value):
        self.historylist=[]
        self.historygate=[]
        paritylist=[]
        node = netID
        value=value
        backtrace = False
        while True:
            if self.outputgates[node] == []:
                break
            gate1 = self.outputgates[node]
            gate = gate1[0][gate1[0].index(':')+1: ]
            if gate == "INV" or gate ==  "NAND" or gate=="NOR":
                paritylist.append(1)
            else:
                paritylist.append(0)
            self.historygate.append(gate1[0])
            lista = self.gateData[gate1[0]]
            if gate == 'INV' or gate =='BUF':
                node = lista[0]
                self.historylist.append(0)
                continue
            
            if not backtrace:
                if self.netValues[lista[0]-1] == 'x':
                    node = lista[0]
                    self.historylist.append(1)
                    continue
            backtrace=False
            if self.netValues[lista[1]-1] == 'x':
                node = lista[1]
                self.historylist.append(0)
                continue
            
            backtrace = True
            i=-1
            k=0
            while(k==0):
                k= self.historylist[i]
                i=i-1
            
            node = self.gateData[self.historygate[i]][2]  
            self.historygate=self.historygate[:i]
            self.historylist=self.historylist[:i]
            paritylist=paritylist[:i]
            
            backtrace=True
        
        count = 0
        for i in paritylist:
            if i==1:
                count+=1
                
        if count%2==1 and value=='1':
            value = '0'
        elif count%2==1 and value=='0':
            value ='1'
        
        return [node , value]              
     
    def XPATHCheck(self, node):
        #if self.netValues[node-1]=='x':
            #return 0
        inputlist = self.gateData['INPUT']
        if node in inputlist and(self.netValues[node-1]=='x'):
            return 1
        if node in inputlist and not(self.netValues[node-1]=='x'):
            return 0
        while True:
            if node in inputlist:
                return 1
            gate1 = self.outputgates[node]
            gate = gate1[0][gate1[0].index(':')+1: ]
            if gate=="BUF" or gate=="INV":
                if self.netValues[self.gateData[gate1[0]][0]-1]=='x':
                    node = self.gateData[gate1[0]][0]
                else:
                    return 0
            else:
                if self.netValues[self.gateData[gate1[0]][0]-1]=='x':
                    node = self.gateData[gate1[0]][0]
                elif self.netValues[self.gateData[gate1[0]][1]-1]=='x':
                    node = self.gateData[gate1[0]][1]
                else:
                    return 0
            
            
    def Imply(self,netnum,value,stuck_at_net,stuck_at_value):
        
        self.netValues[netnum-1]=value
        if netnum == stuck_at_net:
            if not(value == stuck_at_value):
                
                if value=='0':
                    self.netValues[netnum-1]='D'
                else:
                    self.netValues[netnum-1]='Dbar'
                
        for i in xrange(0,30):
            netdata = self.netValues
            
            for key in self.gateData:
                if key == "INPUT" or key=="OUTPUT":
                    continue
                gate = key[key.index(':')+1 : ]
                a = self.netValues[self.gateData[key][0]-1]
                if not(gate =='INV' or gate == 'BUF'):
                    b = self.netValues[self.gateData[key][1]-1]
                if  gate ==  "AND":
                    output = self.AND(a,b)
                if  gate ==  "NAND":
                    output = self.NAND(a,b)
                if  gate ==  "OR":
                    output = self.OR(a,b)
                if  gate ==  "NOR":
                    output = self.NOR(a,b)
                if  gate ==  "INV":
                    output = self.INV(a)
                if  gate ==  "BUF":
                    output = self.BUF(a)
                
                index=2
                if (gate =='INV' or gate == 'BUF'):
                    index=1 
                
                if self.gateData[key][index]==179 and not(output=='x'):
                    ajdhsjweg=10
                if not(output=='x'):
                    if self.gateData[key][index] == stuck_at_net:
                        if not(output==stuck_at_value):
                            if stuck_at_value == '0':
                                output = 'D'
                            else:
                                output = 'Dbar'                
                
                self.netValues[self.gateData[key][index]-1]  = output

    def PODEMfunction(self , faultnode , stuck_at_value):
        
        self.UpdateDfrontier()
        #localnetvalues=self.netValues
        outputlist = self.gateData["OUTPUT"]
        for i in outputlist[:-1]:
            if self.netValues[i-1] == 'D'  or self.netValues[i-1] == 'Dbar' :
                return 'Success'
            
        if 'D' in self.netValues or 'Dbar' in self.netValues:
            self.ForwardXPath()  
        k= self.XPATHCheck(faultnode)
        #print k
        if len(self.Dfrontier) < 1 and k==0:
            #self.netValues=localnetvalues
            return 'Failure'
    
        [a,b]=self.Objective( faultnode , stuck_at_value)
        [c,d] = self.BackTrace(a,b)
        self.Imply(c,d,faultnode,stuck_at_value)
        if(self.PODEMfunction( faultnode , stuck_at_value) == 'Success'):
            return 'Success'
        if d == '0':
            d='1'
        elif d=='1':
            d='0' 
        self.Imply(c,d, faultnode,stuck_at_value)
        if(self.PODEMfunction( faultnode , stuck_at_value) == 'Success'):
            return 'Success'
        self.Imply(c,'x', faultnode,stuck_at_value)
        
        #self.netValues=localnetvalues
        return 'Failure'
                
    def Cleanup(self):
        self.gateData ={}
        self.numberOfNets=0
        self.netValues = []
        self.Dfrontier = []
        self.POs=[]
        self.PIs = []
        self.flag = 0
        self.outputgates = {}
        self.historylist=[]
        self.historygate=[]          
        
class LogicSimulator:
    def __init__(self):
        self.gateLibrary = []
        self.gateData ={}
        self.numberOfPrimaryInputs = 0
        self.numberOfPrimaryOutputs = 0
        self.numberOfNets = 0;
        self.inputdatapattern = [];
        self.netValues = []
        self.line=""
        self.faultlist = {}
        self.userfaultlist = {}
        self.originaluserfaultlist = {}


    def GetGateData(self):
        count=1
        inputfile = sys.argv[1] + ".txt"
        self.GateFile = open(inputfile,"r")
        for line in self.GateFile:
            line_split = line.split("\r\n")[0]
            l=[]
            l1= ((line_split.split(' '))[1: ])
            for i in l1:
                l.append(int(i));
            if line_split.split(' ')[0] == "INPUT" or line_split.split(' ')[0] == 'OUTPUT':
                self.gateData[line_split.split(' ')[0] ] = l
            else:
                self.gateData[str(count) + ":" + line_split.split(' ')[0] ] = l
            count=count+1;
        for v in self.gateData.values():
            if v:
                self.numberOfNets = max(self.numberOfNets , max(v))


    def GetInputData(self):
        line_split= self.line.split("b")[0]
        l1= line_split.split(' ')
        for i in l1:
            self.inputdatapattern.append(int(i))

    def InitializeNetData(self , randomvar = False , randomlist = None ):

        for i in xrange(self.numberOfNets):
            self.netValues.append(-1)
        i=0;
        list1 = self.gateData['INPUT'][ :-1]

        if randomvar:
            for data in list1:
                self.netValues[data-1] = randomlist[i]
                i=i+1
        else:
            for data in list1:
                self.netValues[data-1] = self.inputdatapattern[i]
                i=i+1


    def AND(self, a ,b):
        return a&b & 0x1

    def OR(self , a ,b):
        return a|b & 0x1

    def INV(self, a):
        return ~a & 0x1

    def NAND(self, a ,b):
        return ~(a&b) & 0x1

    def BUF(self, a):
        return a

    def NOR(self,a,b):
        return ~(a|b) & 0x1


    def Evaluate(self):
        while(self.netValues.count(-1)):
            for key1 in self.gateData:
                if key1 == 'OUTPUT' or key1 == "INPUT":
                    continue
                key = key1[key1.index(':')+1 : ]
                gate= self.gateData[key1]
                #if key1 == '51:AND':
                   # print 'here'
                for i in xrange(len(gate)):
                    gate[i]=gate[i]-1;

                if key == 'INV':
                    if not self.netValues[gate[0]]==-1:
                        self.netValues[gate[1]]= self.INV(self.netValues[gate[0]])
                        self.faultlist[gate[1]].extend(self.faultlist[gate[0]])
                        self.faultlist[gate[1]]= list(set(self.faultlist[gate[1]]))

                if key == 'BUF':
                    self.netValues[gate[1]] = self.netValues[gate[0]]
                    self.faultlist[gate[1]].extend(self.faultlist[gate[0]])
                    self.faultlist[gate[1]]= list(set(self.faultlist[gate[1]]))                    

                if key == "AND":
                    if not (self.netValues[gate[0]] == -1 or self.netValues[gate[1]] == -1):
                        self.netValues[gate[2]] = self.AND(self.netValues[gate[0]],self.netValues[gate[1]])
                        self.deductivefaultsimulation(gate[0], gate[1], gate[2], 0)
                    else:
                        pass

                if key == "NAND":
                    if not (self.netValues[gate[0]] == -1 or self.netValues[gate[1]] == -1):
                        self.netValues[gate[2]] = self.NAND(self.netValues[gate[0]], self.netValues[gate[1]])   
                        self.deductivefaultsimulation(gate[0], gate[1], gate[2], 0)
                    else:
                        pass


                if key == "OR":
                    if not (self.netValues[gate[0]] == -1 or self.netValues[gate[1]] == -1):
                        self.netValues[gate[2]] = self.OR(self.netValues[gate[0]],self.netValues[gate[1]])
                        self.deductivefaultsimulation(gate[0], gate[1], gate[2], 1)

                if key == "NOR":
                    if not (self.netValues[gate[0]] == -1 or self.netValues[gate[1]] == -1):
                        self.netValues[gate[2]] = self.NOR(self.netValues[gate[0]],self.netValues[gate[1]])
                        self.deductivefaultsimulation(gate[0], gate[1], gate[2], 1)


                for i in xrange(len(gate)):
                    gate[i]=gate[i]+1;         

    def InitializeFaultList(self):
        for i in xrange(self.numberOfNets):
            self.faultlist[i] = [];
        for i in xrange (self.numberOfNets):
            self.faultlist[i].append(str(i) + ": net " + str(i + 1) +"  stuck at  "+str (~self.netValues[i] & 0x1))

    def deductivefaultsimulation(self, a , b , c , controlling_value):
        
        if self.netValues[a]==controlling_value and self.netValues[b] == ~controlling_value &0x1 :
            for i in self.faultlist[b]:
                if self.faultlist[a].count(i):
                    self.faultlist[a].remove(i)
            self.faultlist[c] = list(set(self.faultlist[c] + (self.faultlist[a])))
            return

        if self.netValues[b]==controlling_value and self.netValues[a] == ~controlling_value &0x1:
            for i in self.faultlist[a]:
                if self.faultlist[b].count(i):
                    self.faultlist[b].remove(i)
            self.faultlist[c] = list(set(self.faultlist[c] + (self.faultlist[b])))
            return      

        if self.netValues[a] == controlling_value and self.netValues[b] == controlling_value :
            if (len(set(self.faultlist[a]) & set(self.faultlist[b]))):
                self.faultlist[c] = list(set(self.faultlist[c] + (list(set(self.faultlist[a]) & set(self.faultlist[b])))))
                return

        else:
            input_list = self.gateData['INPUT'] 
            self.faultlist[c] = list(set(self.faultlist[c] + (self.faultlist[a]) + (self.faultlist[b])))
            return

    def GetFaultListFromUser(self):
        Inputfile = sys.argv[1] + "_stuckatfaults.txt"
        data = open(Inputfile , "r")
        for line in data:
            line_split1 = line.split('\n')[0]
            line_split = line_split1.split(' ')
            self.userfaultlist[int(line_split[0]) -1] = int(line_split[1])
        temp = []
        for i in self.userfaultlist:
            self.originaluserfaultlist[i] = self.userfaultlist[i]
            if self.netValues[i] == self.userfaultlist[i]:
                temp.append(i)

        for i in temp:
            self.userfaultlist.pop(i)


    def Cleanup(self):
        self.gateLibrary = []
        self.gateData ={}
        self.numberOfPrimaryInputs = 0
        self.numberOfPrimaryOutputs = 0
        self.numberOfNets = 0;
        self.inputdatapattern = [];
        self.netValues = []
        self.line=""        






#initialize logging

LogFileName = 'Result_of_PODEM_for_' + sys.argv[1] +'.log'
logging.basicConfig(level=logging.DEBUG,
                    format='%(message)s',
                    filename=LogFileName,
                    filemode='w')
logging.info("\n\n########## Logging for the input file name {}.txt ############ \n\n" .format(sys.argv[1]))

#Getting the input file with stuck at faults
input_file_name = sys.argv[1] + '_stuckatfaults.txt'
input_file = open(input_file_name,"r")
LogicSimulator = LogicSimulator()
PODEM = PODEM()
for line in input_file:

    netnumber = int(line.split(' ')[0])
    stuck_at_value = line.split(' ')[1].split('\n')[0]
    logging.info("")
    logging.info("The fault is net {} stuck at {}".format(netnumber,stuck_at_value))
    PODEM.GetGateData()
    PODEM.InitializeNetData()
    a=[0,1]
    #for k in xrange(1,PODEM.numberOfNets+1):
        #for i in a:
            #logging.info('{} {}'.format(k,i))    
    Result=PODEM.PODEMfunction(netnumber , stuck_at_value)
    print "PODEM result is"
    print Result
    logging.info("\nThe PODEM result is --> [{}] \n".format(Result))
    if Result=='Success':
        inputlist = PODEM.gateData["INPUT"]
        input_vector =[]
        for i in inputlist[:-1]:
            if PODEM.netValues[i-1]=='Dbar':
                PODEM.netValues[i-1]='1'
            if PODEM.netValues[i-1]=='D':
                PODEM.netValues[i-1]='0'
            input_vector.append(PODEM.netValues[i-1])
            
        s =""
        for i in input_vector:
            s=s+i+' '
            
        logging.info("The test vector generated by PODEM is --> [{}]".format(s[:-1]))
        print input_vector
        inputString_DFS = ""
        for i in input_vector[:-1]:
            if i =='x':
                a = random.randint(0,1)
                inputString_DFS = inputString_DFS + str(a)+' '
            else:
                inputString_DFS = inputString_DFS + str(i)+' '
        
        if input_vector[-1]=='x':
            inputString_DFS = inputString_DFS + str(random.randint(0,1))+'b'
        else:
            inputString_DFS = inputString_DFS + str(input_vector[-1])+'b'
        
        print inputString_DFS
                
        print "Going for DFS check"
        
        #logging.info("Performing a Deductive fault simulation check with input vector[{}].\n".format(inputString_DFS[:-1]))
        
        LogicSimulator.GetGateData() 
        LogicSimulator.inputdatapattern=[]
        LogicSimulator.line = inputString_DFS
        LogicSimulator.GetInputData()
        LogicSimulator.numberOfPrimaryInputs = len(LogicSimulator.gateData['INPUT']) -1
        LogicSimulator.numberOfPrimaryOutputs = len( LogicSimulator.gateData['OUTPUT']) -1
        if not len(LogicSimulator.inputdatapattern) == LogicSimulator.numberOfPrimaryInputs:
            raise "Error : Number of inputs provided is not equal to the number of primary inputs for the logical circuit"
        
        LogicSimulator.InitializeNetData()
        LogicSimulator.InitializeFaultList()
        LogicSimulator.Evaluate()
        LogicSimulator.InitializeFaultList()
        LogicSimulator.netValues=[]
        LogicSimulator.InitializeNetData()
        
        LogicSimulator.Evaluate()

        outputgatenets= LogicSimulator.gateData['OUTPUT'][ :-1]
        outputgatedata = []
        faultfound =[];
        for i in outputgatenets:
            outputgatedata.append(LogicSimulator.netValues[i-1])
            faultfound = list(set(faultfound + LogicSimulator.faultlist[i-1]))
        
        finalfaults={}
        for i in faultfound:
            finalfaults[int(i.split(":")[0])] = i.split(":")[1]
            
        
        faultlist=[]
        for key in finalfaults:
            faultlist.append(finalfaults[key])
        
        input_fault = ' '+'net '+ str(netnumber) +'  stuck at  '+ stuck_at_value
        
        if input_fault in faultlist:
            logging.info("The Deductive Fault Simulator check has passed for the vector [{}]" .format(inputString_DFS[:-1]))
            print "The DFS check has passed for the vector {}" .format(inputString_DFS)
        else:
            logging.info('\n The DFS check has failed \n')
        
        
        
    logging.info("\n\n - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n\n")
    LogicSimulator.Cleanup()
    PODEM.Cleanup()

logging.info("##################### THE END #####################")
print "\n\n\n###########Exiting the code###########\n\n\n"





