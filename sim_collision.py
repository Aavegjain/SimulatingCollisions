def find_velocity_after_collision(m1,m2,u1,u2,x1,x2):
    v1 = ((m1-m2)*u1)/(m1+m2) +  ((2*m2)*u2)/(m1+m2) 
    v2 = ((2*m1)*u1)/(m1+m2) - ((m1-m2)*u2)/(m1+m2)  
    return (v1,v2)

def find_time_after_collision(u1,u2,x1,x2):
    if (u1 - u2 > 0):
        t =(x2 - x1)/(u1 - u2) 
    else:
        t = None 
    return t

# def find_position_after_collision(u1,u2,x1,x2):

#     if (u1 - u2 > 0):
#         return (u1 * x2 - u2 * x1) / (u1 - u2) 
#     else:
#         return None 


class PriorityQueue: # priority queue implementation using heaps
    def __init__(self,A):
        self.A = A   # array to store heap indexes .
        self.size = 0
        self.heap = []  # heap 
    
    def heapdown(self,x): # x is the heap index
        child1 = 2*x + 1
        child2 = 2*x + 2
        n = len(self.heap)
        child = x 
        while (True):
            if (child1 < n and (self.heap[child1][1] < self.heap[child][1] or (self.heap[child1][1] == self.heap[child][1] and self.heap[child1][0]<self.heap[child][0]))):
                child = child1 
            if (child2 < n and (self.heap[child2][1] < self.heap[child][1] or (self.heap[child2][1] == self.heap[child][1] and self.heap[child2][0]<self.heap[child][0]))):
                child = child2 

            if (child == x):   
                break 
            else:
                i = self.heap[child][0] 
                j = self.heap[x][0] 
                self.heap[x],self.heap[child] = self.heap[child],self.heap[x]
                self.A[i] = x
                self.A[j] = child
                x = child 
                child1 = 2*x + 1
                child2 = 2*x + 2

    

    def heapup(self,x): # x is the index 
        parent = (x - 1) // 2
        while (x > 0 and (self.heap[x][1] < self.heap[parent][1] or (self.heap[x][1] == self.heap[parent][1] and self.heap[x][0]<self.heap[parent][0]))):
            i = self.heap[parent][0] 
            j = self.heap[x][0]
            self.heap[parent],self.heap[x] = self.heap[x],self.heap[parent]
            
            self.A[i] = x 
            self.A[j] = parent 
            x = parent 
            parent = (x - 1) // 2
        
    
    def enqueue(self,new):   # enqueues a new tuple in the heap
        n = len(self.heap)
        self.heap.append(new)
        i = new[0]
        self.A[i] = n
        
        self.heapup(n) 
    
    def extract_min(self): # removes the min from the heap and updates the heap
        if (self.heap):
            n = len(self.heap)
            i = self.heap[0][0]
            j = self.heap[n-1][0]
            self.A[j] = 0 
            self.A[i] = None

            self.heap[0],self.heap[n-1] = self.heap[n-1],self.heap[0] 
            answer = self.heap.pop() 
            self.heapdown(0) 
            
            return answer 
        else:
            return None
    
    def change_key(self,i,new):  # changes the time of the element, but not the index of collision
        # i is the heap index, t is the new time
    
        initial = self.heap[i]
        index = initial[0] 
        final = (index,new) 
        self.heap[i] = final 

        if (final[1] < initial[1]):
            self.heapup(i)
        elif (initial[1] < final[1]):
            self.heapdown(i)
        else:
            return 
        
    def buildheap(self) : # converts self.heap to a heap
        for i in range((len(self.heap) - 2)//2,-1,-1):
            self.heapdown(i)
    

def listCollisions(M,x,v,m,T):

        if (m == 0 or T == 0):
            return []
        n = len(M) 
        if (n <= 1):
            return [] 
        A = [None] * (n-1)
        times = PriorityQueue(A) 

        #making heap 
        cnt = 0
        for i in range(n-1):

            t = find_time_after_collision(v[i],v[i+1],x[i],x[i+1]) 
            if (t):
                
                times.heap.append((i,t))
                A[i] = cnt 
                cnt += 1 
        times.buildheap()
         
        # heap made
        last_updated = [0] * n 
        answer = []
        cnt = 0
        while (True):
            
            #print(times.heap)
            result = times.extract_min()
            if (result and cnt < m and result[1] <= T):
                cnt += 1
                
                
                index = result[0]
                
                position = x[index]+ v[index]*(result[1] - last_updated[index])
                position2 = x[index+1] + v[index+1]*(result[1] - last_updated[index+1])
                
                vel = find_velocity_after_collision(M[index],M[index+1],v[index],v[index+1],x[index],x[index+1])
                x[index] = position
                x[index+1] = position2 
                v[index] = vel[0] 
                v[index+1] = vel[1] 
                


                last_updated[index] = last_updated[index+1] = result[1]
                answer.append((round(result[1],4),result[0],round(position,4))) 

                if (index > 0):
                    
                    new_position =  x[index-1] + v[index-1] * (result[1] - last_updated[index-1])
                    t1 = find_time_after_collision(v[index-1],v[index],new_position,x[index])
                    if (t1): 
                        new_time = t1 + result[1]
                        if (A[index-1] != None):
                            times.change_key(A[index-1],new_time)
                        else:
                            times.enqueue((index-1,new_time))
                    #last_updated[index-1] = result[1] 

                if (index + 1 < n - 1):
                    
                    
                    new_position = x[index+2] + v[index+2] *( result[1] - last_updated[index+2])
                    t2 = find_time_after_collision(v[index+1],v[index+2],x[index+1],new_position)
                    if (t2): 
                        new_time = t2 + result[1]
                        if (A[index+1]):
                            times.change_key(A[index+1],new_time)
                        else:
                            times.enqueue((index+1,new_time))
                    #last_updated[index+2] = result[1] 
                
                
            else:
                break 
            
        return(answer) 