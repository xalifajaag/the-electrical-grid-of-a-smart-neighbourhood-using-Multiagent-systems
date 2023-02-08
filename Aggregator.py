
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from Home import Home
from init import  domain,pwd,Ns,AggregatorPath
from spade.message import Message

from ast import literal_eval # It is used to convert the string of a List into List, since SPADE only sends strings type /text 
import numpy as np 
import matplotlib.pyplot as plt


class Aggregator(Agent):
    agID=""
    numHome=0
    HomeList=[]

    # Aggregator Initialization 

    async def setup(self):
        print(f"{self.name} created.")


      
    ##############################################################################################################################
    ##############################################################################################################################

    # BEHAVIOURS -------------------------------------------------------------------

    # The createHome behaviour is the Aggregator's behaviour that creates homes
    def CreateHome(self):
        class CreateHome(OneShotBehaviour): # This behaviour is used to create Homes
            async def run(CreateHome):
                print(self.name+" Creating Homes")
                numHome=self.numHome
                agID=self.agID
                for i in range(numHome):
                    home = Home("home"+str(i+1)+agID+"@"+domain,pwd)
                    # This start is inside an async def, so it must be awaited
                    await home.start(auto_register=True)
                    self.HomeList.append(home)
        return CreateHome()

    ##############################################################################################################################
    ##############################################################################################################################
    # The Receive  behaviour is the behaviour to run when the agent has to receive a message
    def Receive(self):
        class Receive(OneShotBehaviour):
            content=None
            Data=None
            async def run(Receive):
                print(self.name + " waiting for message ")
                msg = await Receive.receive(timeout=10) # wait for a message for 10 seconds
                if msg:
                    print(msg.body + " Received ! ")
                    Receive.content=msg.metadata
                    Receive.Data=np.array(literal_eval(Receive.content.get("value"))).tolist()
                else:
                    print("Did not received any message after 10 seconds")

        behav=Receive
        return behav()
                

    ##############################################################################################################################
    ##############################################################################################################################
    # The send function returns the behaviour that permits to send a Data to a Receiver with ReceiverJID as JID

    def sendData(self,dataName,dataValue,ReceiverJID):
        class InformBehav(OneShotBehaviour):
            async def run(senddata):
                print(self.name + " sending "+ dataName)
                msg = Message(to=str(ReceiverJID))     # Instantiate the message
                msg.set_metadata("value", str(dataValue))  # Set the "inform" FIPA performative
                msg.body = dataName      # Set the message content
                await senddata.send(msg)
                print(dataName+" sent to " + ReceiverJID+ " !")
        behav=InformBehav
        return behav()
    
    ##############################################################################################################################
    ##############################################################################################################################
    #  This is used to import values of a variable from a file
    # The behaviour is created with a Data attribute to get the values after the behaviour is completed (done), so after the join() method
    
    # Example : 
    #       behav2=Home.importData(path,filename,extension)    
    #       aggregatoragent.add_behaviour(behav2)
    #       behav2.join()
    #       k=behav2.Data   k is a variable that contains all  the values of the variable imported (The PV Generated power for example)

    def importData(self,path,filename,extension):
        import numpy as np
        from ast import literal_eval
        class Import(OneShotBehaviour):
            Data=None
            async def run(Import):

                print(self.name +  " importing "+ filename)
            
                Filename=filename + '.'+ extension  #file name 

                f=open(path+'/'+Filename,'r') #open the folder in read method ('r'), error if the file does not exist

                dcon=f.read() #save the data in the file in dcon

                f.close() #close the file

                Import.Data=np.array(literal_eval(dcon)) #--------------converts the text into list then into an array

            
        
        return Import()


     ##############################################################################################################################
    ##############################################################################################################################

    def Plot(self,dataName,dataValue):
        class Plot(OneShotBehaviour):
            async def run(Plot):
                print(self.name + "plotting "+ dataName)
                t=[i for i in range(len(dataValue))]

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

    def saveData(self,data,path,filename,extension):

        import os

        class Save(OneShotBehaviour):
            async def run(Save):
                print( self.name +" Saving "+ filename )

                if not os.path.exists(path):
                    os.makedirs(path)
                
                file=filename + '.'+ extension

                with open(os.path.join(path, file), 'w') as fp:
                
                    fp.write(str(data))
    
        behav=Save
        return behav()
    
    ##############################################################################################################################
    ##############################################################################################################################

 # In the chargeHomes behaviour, we assume that all the exported power is shared between homes with battery
    
    def chargeHomes(self):

        class charge(OneShotBehaviour):

            async def run(charge):

                print(self.name + " Charging Homes !")

                # Import Exported powers and compute the total  


                ToCharge=[]

                SOCs=[]


                for home in self.HomeList:

                    if round(home.battery.cap)!=0:

                        ToCharge.append(home)

                        SOCs.append(np.array(home.battery.soc))


                print(str(len(ToCharge)))



                Export=[]

                for home in ToCharge:

                    Path=AggregatorPath+'\ ' + str(home.name)

                    aggimport=self.importData(Path,"Pexported","txt")
                    
                    self.add_behaviour(aggimport)

                    await aggimport.join()

                    Export.append(aggimport.Data)

                TotalExport=sum(Export)



                Import=[]

                for home in ToCharge:

                    Path=AggregatorPath+'\ ' + str(home.name)

                    aggimport1=self.importData(Path,"Pimported","txt")

                    self.add_behaviour(aggimport1)

                    await aggimport1.join()

                    Import.append(aggimport1.Data)

                TotalImport=sum(Import)
                charge.FirstImportation=TotalImport 


                # for home in ToCharge:
                                    
                #     Path=AggregatorPath+'\ ' + str(home.name)
                
                #     aggimport2=self.importData(Path,"SOC","txt")
                
                #     self.add_behaviour(aggimport2)
                
                #     await aggimport2.join()
                
                #     SOCs.append(aggimport2.Data)
                    

                # TotalSOC=sum(SOCs)

                


                # SOCmoy=TotalSOC/u

                RemPower=(TotalExport-TotalImport).tolist()

                
                
                Psurplus=[0]*Ns

                ToImport=[0]*Ns

                for i in range(Ns):

                    if RemPower[i]>=0:

                        Psurplus[i]=RemPower[i]
                        ToImport[i]=0

                    else: 

                        Psurplus[i]=0
                        ToImport[i]=-RemPower[i]

                RemPower=np.array(Psurplus)

                charge.Rempowerbeforecharge=np.array(Psurplus)

                

                charge.ToImport=np.array(ToImport)

                RemPowermoy=RemPower/len(ToCharge)

                r=0
                SOCmoy=np.array([0.5]*(Ns+1))


                while True:

                    ChargePowers=[]

                    r=r+1
  

                    SOCfin=[]
                

                    for home in ToCharge:
                        
            
                        Pch=[0]*Ns
                        

                        for t in range(Ns):

                            if SOCmoy[t]>home.battery.soc[t]:

                                pch=min((SOCmoy[t]-home.battery.soc[t])*home.battery.cap,RemPowermoy[t])

                                if pch > 0 :

                                    Pch[t]=pch
                                
                                else:

                                    Pch[t]=0


                        pch=np.array(Pch)

                        homeCharge=home.ChargeBattery(pch)

                        home.add_behaviour(homeCharge)

                        await homeCharge.join()

                        soc2=home.battery.soc


                        SOCfin.append(np.array(soc2))

                    
                        ChargePowers.append(np.array(Pch))

                        
                        for b in range(Ns):

                            if RemPowermoy[b]-Pch[b] > 0:

                                RemPower[b]=RemPower[b]-Pch[b]
                            
                            else:

                                RemPower[b]=0


                            RemPowermoy=RemPower/len(ToCharge)


                    sumCharge=sum(ChargePowers)

                    if (sumCharge==0).all() or (RemPower==0).all():

                        break
                    
                charge.RemPower=RemPower
        return charge()









    

