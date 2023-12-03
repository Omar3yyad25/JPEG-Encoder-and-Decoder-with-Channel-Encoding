import heapq 

class Huffman:
    class node: 
        def __init__(self, freq, symbol, left=None, right=None):  
            self.freq = freq 
 
            self.symbol = str(symbol) 
 
            self.left = left 

            self.right = right 

            self.huff = '' 

        def __lt__(self, nxt): 
            return self.freq < nxt.freq 

    def __init__(self, arr):
        nodes = []
        for val, freq in self.calculate_frequency(arr).items():
            heapq.heappush(nodes, self.node(freq, val))
        #self.freq_tables = self.calculate_frequency(arr)
        self.nodes = nodes
        self.freq_table = self.calculate_frequency(arr)
        self.table = dict()
        self.create_table()
        
      
    def create_table(self):
        while len(self.nodes) > 1:  
            left = heapq.heappop(self.nodes) 
            right = heapq.heappop(self.nodes) 

            left.huff = 0
            right.huff = 1

            newNode = self.node(left.freq+right.freq, left.symbol+right.symbol, left, right) 

            heapq.heappush(self.nodes, newNode) 
        printNodes(self, self.nodes[0]) 
        

    def calculate_frequency(self, arr):
            freq_dict = dict()
            counter = 0;
            for elem in arr:
                if elem in freq_dict:
                    freq_dict[elem] += 1
                    counter +=1
                else:
                    freq_dict[elem] = 1
                    counter +=1
            for element in freq_dict:
                freq_dict[element] = freq_dict[element] / counter
            return freq_dict

def printNodes(self, node, val=''): 

    newVal = val + str(node.huff) 

    # if node is not an edge node 
    # then traverse inside it 
    if(node.left): 
        printNodes(self, node.left, newVal) 
    if(node.right): 
        printNodes(self, node.right, newVal) 

    if(not node.left and not node.right): 
        #print(f"{node.symbol} -> {newVal}")
        self.table[newVal] = node.symbol