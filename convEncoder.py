class convEncoder:

    def __init__(self, K, rate, input):
        #number of registers = K-1
        self.numRegisters = K-1
        self.iteration = (self.numRegisters+ len(input))
        self.numParities = 1/rate
        self.input = self.numRegisters * '0' + input + self.numRegisters * '0'
        self.registersoccupation = ""
        self.parities = []
        self.work()

    def createP1(self,x):
        if int(x[1]) + int(x[0]) > 1:
          return 0
        else:
          return 1
        
    
    def createP2(self,x):
        return int(x[1])
        
    
    def createP3(self,x):

         if int(x[2]) + int(x[0]) > 1:
          return 0
         else:
          return 1

    def createParities(self):
        p1 = self.createP1(self.registersoccupation)
        p2 = self.createP2(self.registersoccupation)
        p3 = self.createP3(self.registersoccupation)

        parities = {"p1":p1, "p2":p2, "p3":p3}
        return [p1, p2, p3]

    def work(self):
        
        for i in range(self.iteration):
            self.registersoccupation = self.input[i:self.numRegisters + i+1]
            self.parities.append( self.createParities())
        print(self.parities)

