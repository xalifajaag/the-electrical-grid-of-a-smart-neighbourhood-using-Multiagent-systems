
import numpy as np
import random
import matplotlib.pyplot as plt
Ns=96


t=[i for i in range(Ns)]





class Task:

    
    def __init__(self,st,duration,Rate):

           
        self.st=st               #--------------------start time of the task
        self.duration=duration   #--------------------duration of the task
        self.Rate=Rate           #--------------------Power consumed to perform the task

        self.consumption=[0]*Ns  # -------------------profile of the task's global consumption
        self.status=[0]*Ns       # -------------------Status of the task 1 if running and 0 if not
        self.et=st+duration      #--------------------end time of the task
   
        for i in range(Ns):

            if st <= i < st+duration :
                self.status[i]=1
            else:
                self.status[i]=0

            self.consumption[i]=Rate*self.status[i]

def shiftTask(start,task):
    
    class shifted:
        def __init__(self,st,duration,Rate):
            
            self.st=task.st               #--------------------start time of the task
            self.duration=task.duration   #--------------------duration of the task
            self.Rate=task.Rate           #--------------------Power consumed to perform the task
            
            self.consumption=[0]*Ns  # -------------------profile of the task's global consumption
            self.status=[0]*Ns       # -------------------Status of the task 1 if running and 0 if not
            self.et=st+duration      #--------------------end time of the task
       
            for i in range(Ns):

                if st <= i < st+duration :
                    self.status[i]=1
                else:
                    self.status[i]=0

                self.consumption[i]=Rate*self.status[i]
                
    st=random.choice(range(start,Ns,1))
                
    while st+task.duration>Ns:
        
        st=random.randint(start,Ns)
        
    return shifted(st,task.duration,task.Rate)

# ----------------------------------NON INTERRUPTIBLE AND NON SHIFTABLE APPLIANCE ---------------------------------------
class NIappliance:

    tasks=[]

    def __init__(self,operationWindow,*task):

        # operationWindow is a list: [start-time ; end time]  

        # operationWindow[0]=predefined start of the appliance

        # operationWindow[1]=predefined start of the appliance

        self.operationWindow=operationWindow
        self.consumption=[0]*Ns
        k=0

        #-------------------------CREATION OF TASKS AS ATTRIBUTES OF THE APPLIANCE---------------------
        for t in task:
            globals()[f'task{k+1}']=t
            NIappliance.tasks.append(globals()[f'task{k+1}'])
            k=k+1

        duration=0     #----------operation time of the appliance
        for n in range(k):
            duration =duration+globals()[f'task{n+1}'].duration
    
        if (operationWindow[0]<0 or operationWindow[1]>Ns) or operationWindow[0]+duration>operationWindow[1]:

            globals()[f'task{1}']=Task(operationWindow[0],globals()[f'task{1}'].duration,0)

            print("The predefined operation time of the NINSappliances is not enough or is invalid !")

            for i in range(1,k):

                globals()[f'task{i+1}']=Task(globals()[f'task{i}'].et,globals()[f'task{i+1}'].duration,0)
        
        else:
            globals()[f'task{1}']=Task(operationWindow[0],globals()[f'task{1}'].duration,globals()[f'task{1}'].Rate)

         #---The line codes below permits to make task2 start after task1, task3 after task2 and etc...
        for i in range(1,k):

            globals()[f'task{i+1}']=Task(globals()[f'task{i}'].et,globals()[f'task{i+1}'].duration,globals()[f'task{i+1}'].Rate)

        #-------------Determination of the global consumption----------------------------------------------------
        c=[]
        
        for l in range(k):
            c.append(np.array(globals()[f'task{l+1}'].consumption))

        self.consumption=sum(c).tolist()
    
   

# ----------------------------------NON INTERRUPTIBLE AND SHIFTABLE APPLIANCE ---------------------------------------

class NISappliance:

    tasks=[]

    def __init__(self,operationWindow,*task):

        # operationWindow is a list: [start-time ; end time]  

        # operationWindow[0]=predefined start of the appliance

        # operationWindow[1]=predefined start of the appliance

        self.operationWindow=operationWindow
        self.consumption=[0]*Ns
        k=0

        st=random.choice([i for i in range(operationWindow[0],operationWindow[1]-duration,1)])

        #-------------------------CREATION OF TASKS AS ATTRIBUTES OF THE APPLIANCE------------------------
        for t in task:
            globals()[f'task{k+1}']=t
            NISappliance.tasks.append(globals()[f'task{k+1}'])
            k=k+1

    
        duration=0     #----------operation time of the appliance
        for n in range(k):
            duration =duration+globals()[f'task{n+1}'].duration
            
        NISappliance.duration=duration
    
        if (operationWindow[0]<0 or operationWindow[1]>Ns) or st+duration>operationWindow[1]:

            globals()[f'task{1}']=Task(0,globals()[f'task{1}'].duration,0)
            
            NISappliance.tasks[0]=globals()[f'task{1}']

            print("The predefined operation time of the NISappliances is not enough or is invalid !")

            for i in range(1,k):

                globals()[f'task{i+1}']=Task(globals()[f'task{i}'].et,globals()[f'task{i+1}'].duration,0)
        
        else:
            globals()[f'task{1}']=Task(st,globals()[f'task{1}'].duration,globals()[f'task{1}'].Rate)

         #---The line codes below permits to make task2 start after task1, task3 after task2 and etc...
        for i in range(1,k):

            globals()[f'task{i+1}']=Task(globals()[f'task{i}'].et,globals()[f'task{i+1}'].duration,globals()[f'task{i+1}'].Rate)

        #-------------Determination of the global consumption----------------------------------------------------
        c=[]
        
        for l in range(k):
            c.append(np.array(globals()[f'task{l+1}'].consumption))

        self.consumption=sum(c).tolist()
        
# ----------------------Load Shifting-----------------------------------------------

def shiftNIS(App):
    
    class shifted:
        
        tasks=[]
        
        def __init__(self,operationWindow,task):
            self.operationWindow=App.operationWindow
            self.task=App.tasks
            self.consumption=[0]*Ns
            k=0
    
            #-------------------------CREATION OF TASKS AS ATTRIBUTES OF THE APPLIANCE---------------------
            for t in task:
                globals()[f'task{k+1}']=t
                shifted.tasks.append(globals()[f'task{k+1}'])
                k=k+1
    

            globals()[f'task{1}']=Task(operationWindow[0],globals()[f'task{1}'].duration,globals()[f'task{1}'].Rate)
            
            shifted.tasks[0]=globals()[f'task{1}']
    
            #---The line codes below permits to make task2 start after task1, task3 after task2 and etc...
            for i in range(1,k):
    
                globals()[f'task{i+1}']=Task(globals()[f'task{i}'].et,globals()[f'task{i+1}'].duration,globals()[f'task{i+1}'].Rate)
    
            #-------------Determination of the global consumption----------------------------------------------------
            c=[]
            
            for l in range(k):
                c.append(np.array(globals()[f'task{l+1}'].consumption))
    
            self.consumption=sum(c).tolist()
            

    st=random.randint(App.operationWindow[0],App.operationWindow[1])
    
    while st+App.duration>=App.operationWindow[1]:
        
        st=random.randint(App.operationWindow[0],App.operationWindow[1])
            
    return shifted([st,App.operationWindow[1]],App.tasks)




# # ----------------------------------INTERRUPTIBLE AND SHIFTABLE APPLIANCE -------------------------------------------------------
# class Interruptibleappliance:

#     tasks=[]

#     def __init__(self,operationWindow,*task):

#         # operationWindow is a list: [start-time ; end time]  

#         # operationWindow[0]=predefined start of the appliance

#         # operationWindow[1]=predefined start of the appliance

#         # st is the Shifted start time

#         self.operationWindow=operationWindow
        
#         self.consumption=[0]*Ns
#         k=0
#         #-------------------------CREATION OF TASKS (task1 , task2 .... taskn) AS ATTRIBUTES OF THE APPLIANCE---------------------
#         for t in task:
#             globals()[f'task{k+1}']=t
#             Interruptibleappliance.tasks.append(globals()[f'task{k+1}'])
#             k=k+1

#          # ----------------------Load Shifting Control-------------------------------------------------

#         duration=0     #----------operation time of the appliance
#         for n in range(k):
#             duration =duration+globals()[f'task{n+1}'].duration

        
#         Interruptibleappliance.duration=duration
      
     
#         if (operationWindow[0]<0 or operationWindow[1]>Ns) or operationWindow[0]+duration>operationWindow[1]:

#             globals()[f'task{1}']=Task(0,globals()[f'task{1}'].duration,0)

#             print("The predefined operation time of the ISappliances are not enough or is invalid !")

#             for i in range(1,k):

#                 globals()[f'task{1}']=Task(0,globals()[f'task{1}'].duration,0)


#         else:

#             ET=[]
#             for y in Interruptibleappliance.tasks:
#                 ET.append(y.et)

#             if max(ET)>Ns:
#                 print("Check the operation windows of the tasks of the ISappliances ")
            
#                 globals()[f'task{1}']=Task(0,globals()[f'task{1}'].duration,0)


#             #-------------Determination of the global consumption----------------------------------------------------
#             c=[]
            
#             for l in range(k):
#                 c.append(np.array(globals()[f'task{l+1}'].consumption))
    
#             self.consumption=sum(c).tolist()







class Interruptibleappliance:



    def __init__(self,Rate,operationWindow,*startANDduration):

        # operationWindow is a list: [start-time ; end time], the start and end times are flexible

        # operationWindow[0]=predefined start time of the operation window

        # operationWindow[1]=predefined end time of the operation window

        # Rate  is the rated power of the appliance
        
        # *startANDduration are lists [starttime,duration], this appliance is considered as an appliance that operates several times in a day
        # it can start at 8 and finish at 15 then restart at 18 and finish at 22; and so on
        
        

        self.operationWindow=operationWindow
        
        self.consumption=[0]*Ns
        
        self.duration=0 # global duration of the appliance
        
        for i in startANDduration:
            
            self.duration=self.duration+i[1]
            
        
        
        if self.duration > (operationWindow[1]-operationWindow[0]):
            
            print("The required duration doesn't match the authorized duration of the operation window")
            
            self.duration=0

        else:
            
            self.duration=self.duration
            
            Load=[]
            for p in startANDduration:
                
                load=[0]*Ns
                k=0
                
                for i in range(Ns):
                    
                    if p[0]<=i<p[0]+p[1]:
                        
                        load[i]=Rate
                        
                    else:
                        load[i]=0
                k=k+1
                
                globals()[f"Load{k}"]=load
                
                Load.append(np.array(globals()[f"Load{k}"]))
                    
            self.consumption=sum(Load).tolist()
                    
        
    


























        
class appliance:

    tasks=[]

    def __init__(self,operationWindow,st,*task):

        # operationWindow is a list: [start-time ; end time]  

        # operationWindow[0]=predefined start of the appliance

        # operationWindow[1]=predefined start of the appliance

        # st is the Shifted start time

        self.operationWindow=operationWindow
        self.st=st          #---------------------Shifted start time
        self.consumption=[0]*Ns
        k=0
        #-------------------------CREATION OF TASKS (task1 , task2 .... taskn) AS ATTRIBUTES OF THE APPLIANCE---------------------
        for t in task:
            globals()[f'task{k+1}']=t
            appliance.tasks.append(globals()[f'task{k+1}'])
            k=k+1
        
        # ----------------------Load Shifting Control-------------------------------------------------

        duration=0     #----------operation time of the appliance
        for n in range(k):
            duration =duration+globals()[f'task{n+1}'].duration
    
      
     
        if (operationWindow[0]<0 or operationWindow[1]>Ns) or operationWindow[0]+duration>operationWindow[1]:

            globals()[f'task{1}']=Task(st,globals()[f'task{1}'].duration,0)

            print("The predefined operation time is not enough or is invalid !")

            for i in range(1,k):

                globals()[f'task{i+1}']=Task(globals()[f'task{i}'].et,globals()[f'task{i+1}'].duration,0)

        elif st >= operationWindow[0] and st+duration<=operationWindow[1]:

            globals()[f'task{1}']=Task(st,globals()[f'task{1}'].duration,globals()[f'task{1}'].Rate)

        else:
            globals()[f'task{1}']=Task(operationWindow[0],globals()[f'task{1}'].duration,globals()[f'task{1}'].Rate)

            print("The Appliance can't be started out of the predefined operation window .It's started at the predefined start time")

        # ------------------------------------------------------------------------------------------------------------------------
          #---The line codes below permits to make task2 start after task1, task3 after task2 and etc...
        for i in range(1,k):

            globals()[f'task{i+1}']=Task(globals()[f'task{i}'].et,globals()[f'task{i+1}'].duration,globals()[f'task{i+1}'].Rate)

        #-------------Determination of the global consumption--------------------------------------------------------------------
        c=[]
        
        for l in range(k):
            c.append(np.array(globals()[f'task{l+1}'].consumption))

        self.consumption=sum(c).tolist()












