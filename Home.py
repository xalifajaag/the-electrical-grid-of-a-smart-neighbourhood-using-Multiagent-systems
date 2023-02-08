from spade.agent import Agent
import numpy as np
from numpy.random import normal
from ast import literal_eval 
from homeComponents import EV,homeBattery,PV
import matplotlib.pyplot as plt
from init import Irradience, Temperature, Ns,appliances , batteryCharacteristics, EVcharacteristics
from tools import ExcelAppliances,defer
from spade.behaviour import OneShotBehaviour
from spade.message import Message


###################################################################################################################################################

class Home(Agent):

    # Initialization of the Home agent

    async def setup(self):

        print(self.name+" created.")

       

     #---------------------Home components-----------------------------------------

        # *******************************************PV system *******************
        
        Npv=min(1,abs(round(normal(1,1.5)))) # Number of PV systems of a home : 0 or 1
        
       
        M=abs(round(normal(5,1))) # Number of module per string
        
        N=abs(round(normal(10,5)))  # Number of string

        Nm=N*M*Npv # Number of modules of the PV system 

        pv=PV(normal(Irradience,0.001),normal(Temperature,5),Nm)
      

        self.pv=np.array(pv)

    #--------------------Appliances-------------------------------------------------

        Appliances=ExcelAppliances(appliances)

        self.NFA_list=Appliances.NFA_List
        self.FA_list=Appliances.FA_List

        NFA_load=0
        FA_load=0

        for y in self.NFA_list:
            NFA_load=np.array(y.consumption)+NFA_load

        for z in self.FA_list:
         FA_load=np.array(z.consumption)+FA_load

        
        # ************************ EV ****************************************************************
        Nev=min(1,abs(round(normal(1,1.5))))  # Number of EV of a home : 0 or 1

            # To generate differrent start and stop time of the electric vehicle charging 
        while True:
            stev=normal(EVcharacteristics.st,30) 
            etev=normal(EVcharacteristics.et,30)

            if 0<=stev<etev<=Ns:

                break

        self.EV=EV(stev,etev,Nev*normal(EVcharacteristics.Rate,2),(Nev+0.0001e-80)*normal(EVcharacteristics.cap,50),Nev*EVcharacteristics.socm,Nev*EVcharacteristics.socM)
        self.Pev=np.array(self.EV.Pev)
       
        #*********************************************************************************************



        self.pl=NFA_load+FA_load+self.Pev
        self.ps=self.pv-self.pl

        Nbat=Npv # if we have a pv system we have battery 


        #**********************************BATTERY***********************************************************

        self.battery=homeBattery(Nbat,normal(batteryCharacteristics.cap,10),self.ps)
       
        
        

        # ----------------- HOME POWER FLOW ---------------------------------------------

        self.Pexported=[0]*Ns #------------exported Power

        self.Pimported=[0]*Ns #------------Power consumed from the grid or elsewhere

        for k in range(Ns):

            if self.ps[k]>=0 and  self.battery.soc[k]<self.battery.socM:

                self.Pexported[k]=self.ps[k]

            elif self.ps[k]>=0 and self.battery.soc[k]<=self.battery.socM:

                self.Pexported[k]=self.ps[k]-self.battery.Pch[k]

            
            elif self.ps[k]<=0 and self.battery.soc[k]<=self.battery.socm:

                self.Pimported[k]=abs(self.ps[k])

            elif self.ps[k]<=0 and self.battery.soc[k]<=self.battery.socm:

                self.Pimported[k]=abs(self.ps[k])-abs(self.battery.Pdis[k])

        #------------------------------------------------------------------------------------

        # We convert the pv, pl and ps matrixes into lists beacause the send_data() function converts lists into string/ text (since SPADE only sends strings)
        # The string received are then reconverted into lists and then into matrix to make simple computations

        self.PV=self.pv.tolist()    
        self.PL=self.pl.tolist()
        self.Ps=self.ps.tolist()


    ##############################################################################################################################
    ##############################################################################################################################
      
       # Behaviours of the Home Agent

    ##############################################################################################################################
    ##############################################################################################################################

    # The send function returns the behaviours that permits to send a value to a Receiver with ReceiverJID as JID

    def sendData(self,dataName,dataValue,ReceiverJID):
        class Send(OneShotBehaviour):
            async def run(Send):
                print( self.name +" sending " + dataName )
                msg = Message(to=str(ReceiverJID))     # Instantiate the message
                msg.set_metadata("value", str(dataValue))  # Set the "inform" FIPA performative
                msg.body = dataName      # Set the message content
                await Send.send(msg)
                print(dataName+" sent to " + str(ReceiverJID)+ " !")
        behav=Send
        return behav()

    ##############################################################################################################################
    ##############################################################################################################################

    def saveData(self,data,path,filename,extension):

        import os

        class Save(OneShotBehaviour):
            async def run(Save):
                
                print(self.name+" Saving "+ filename )

                if not os.path.exists(path):
                    os.makedirs(path)
                
                file=filename + '.'+ extension

                with open(os.path.join(path, file), 'w') as fp:
                
                    fp.write(str(data))
    
        behav=Save
        return behav()

    ##############################################################################################################################
    ##############################################################################################################################
    #  This is used to import values of a variable from a file
    # The behaviour is created with a Data attribute to get the values after the behaviour is completed (done), so after the join() method
    
    # Example : 
    #       behav2=Home.importData(path,filename,extension)    
    #       homeagent.add_behaviour(behav2)
    #       behav2.join()
    #       k=behav2.Data   k is a list that contains all  the values of the variable imported (The PV Generated power for example)



    def importData(self,path,filename,extension):
        import numpy as np
        from ast import literal_eval
        class Import(OneShotBehaviour):
            Data=None
            async def run(Import):

                print(self.name+ " importing "+ filename)
            
                Filename=filename + '.'+ extension  #file name 

                f=open(path+'/'+Filename,'r') #open the folder in read method ('r'), error if the file does not exist

                dcon=f.read() #save the data in the file in dcon

                f.close() #close the file

                Import.Data=np.array(literal_eval(dcon)) #--------------converts the text into list then into an array

            
        
        return Import()
        
    
    ##############################################################################################################################
    ##############################################################################################################################
    # THIS Behaviour is used  to charge the Home Battery From an aggregated power, by the Aggregator 
    
    def ChargeBattery(self,chargingPower):
         
        class charge(OneShotBehaviour):

            async def run(charge):

                if (round(self.battery.cap)>0):

                    print (self.name+" Charging battery")

                    self.ps=self.ps+np.array(chargingPower)

                    self.battery=homeBattery(1,self.battery.cap/1000,self.ps)

                    self.Pimported=self.Pimported+np.array(chargingPower)

                else:

                    print(self.name + " Doesn't have a battery")

        behav=charge

        return behav()


    ##############################################################################################################################
    ##############################################################################################################################
    

    def Plot(self,dataName,dataValue):
        class Plot(OneShotBehaviour):
            async def run(Plot):
                t=[i for i in range(len(dataValue))]
                print(self.name +" Plotting "+ dataName)
                plt.plot(t,dataValue)
                plt.grid()
                plt.title(dataName)
                plt.xlabel(" Time ")
                plt.ylabel(dataName)
                plt.show()
        behav=Plot
        return behav()

    ##############################################################################################################################
    ##############################################################################################################################
    # The Receive  behaviour is the behaviour to run when the agent has to receive a message
    def Receive(self):
        class Receive(OneShotBehaviour):
            content=None
            Data=None
            async def run(Receive):
                print(self.name +" Waiting for Message ")
                msg = await Receive.receive(timeout=10) # wait for a message for 10 seconds
                if msg:
                    print(msg.body + " Received !")
                    Receive.content=msg.metadata
                    Receive.Data=np.array(literal_eval(Receive.content.get("value"))).tolist()
                else:
                    print("Did not received any message after 10 seconds")

        behav=Receive
        return behav()
    


