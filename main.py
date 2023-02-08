

from init import domain, Ns,pwd, path,HomePath,AggregatorPath
from Home import Home
from Aggregator import Aggregator
import matplotlib.pyplot as plt
from tools import saveData

t1=[i for i in range(0,Ns)]
t2=[i for i in range(0,(Ns+1))]

AggregatorList=[]

def CreateAgregator(numAggregator,numHome):
   
    for j in range(numAggregator):
        
        Aggregator.agID="ag"+str(j+1) #----------------------------------------------added to home JIDs to identify their related aggregator
        Aggregator.numHome=numHome
        Aggregator.jid="aggregator"+str(j+1)+"@"+domain
        aggregator=Aggregator(Aggregator.jid, pwd)
        AggregatorList.append(aggregator)
        globals()[f"Aggregator{j+1}_Home_List"]=Aggregator.HomeList # ---------globals()[f"Aggregator{j+1}_Home_List"] permits us to dynamically create home agent list for each aggregator
        
        aggregator.start()

        createHome= aggregator.CreateHome()
        aggregator.add_behaviour(createHome)
        createHome.join()

    
                 
if __name__ == "__main__":

    ################################################################################
    #----------------- CREATING AGGREGATORS AND RELATED HOMES----------------------                                                      
    ################################################################################

    CreateAgregator(1,10)



    aggregator= AggregatorList[0]

    for m in range (1):  # This for loop perpits to skip a part of the line codes

        # ########################## SEND HOME CONSUMPTIONS TO AGGREGATOR ####################################


        print("################  HOMES SEND INITIAL CONSUMPTIONS TO AGGREGATOR ########################################")

        for home in aggregator.HomeList:

            # Home send  PL to Aggregator

            print("\n #######################################################################\n")

            print(home.name)

            homepath=HomePath + str(home.name)

            homeSave=home.saveData(home.PL,homepath,"PL","txt")

            home.add_behaviour(homeSave)

            homeSave.join()

            homePlot=home.Plot("Consumption "+str(home.name)+ (" (Watts)"),home.PL)

            home.add_behaviour(homePlot)

            homePlot.join()

            aggReceive = aggregator.Receive()

            homeSend=home.sendData("PL",home.PL,aggregator.jid)

            aggregator.add_behaviour(aggReceive)
            
            home.add_behaviour(homeSend)

            aggReceive.join()

            homeSend.join()

            PL=aggReceive.Data

            aggpath=AggregatorPath + '\ ' + str(home.name)

            aggSave=aggregator.saveData(PL,aggpath,"PL","txt")

            aggregator.add_behaviour(aggSave)

            aggSave.join()

        # ########################## SEND PV GENERATIONS TO AGGREGATOR ####################################

        print("# ########################## HOMES SEND PV GENERATIONS TO AGGREGATOR ####################################")

        for home in aggregator.HomeList:

            print("\n #######################################################################\n")

            print(home.name)

            homepath=HomePath + str(home.name)

            homeSave=home.saveData(home.PV,homepath,"PV","txt")

            home.add_behaviour(homeSave)

            homeSave.join()

            homePlot=home.Plot("PV Generation "+str(home.name)+ (" (Watts)"),home.PV)

            home.add_behaviour(homePlot)

            homePlot.join()

            aggReceive = aggregator.Receive()

            homeSend=home.sendData("PV",home.PV,aggregator.jid)

            aggregator.add_behaviour(aggReceive)

            home.add_behaviour(homeSend)

            aggReceive.join()

            homeSend.join()

            PV=aggReceive.Data

            aggpath=AggregatorPath + '\ ' + str(home.name)

            aggSave=aggregator.saveData(PV,aggpath,"PV","txt")

            aggregator.add_behaviour(aggSave)

            aggSave.join()

        # ########################## SEND IMPORTED POWER TO AGGREGATOR ####################################

        print("# ########################## SEND IMPORTED POWER TO AGGREGATOR ####################################")

        for home in aggregator.HomeList:

            print("\n #######################################################################\n")

            print(home.name)

            homepath=HomePath + str(home.name)

            homeSave=home.saveData(home.Pimported,homepath,"Pimported","txt")

            home.add_behaviour(homeSave)

            homeSave.join()

            homePlot=home.Plot("Imported Power "+str(home.name)+ (" (Watts)"),home.Pimported)

            home.add_behaviour(homePlot)

            homePlot.join()

            aggReceive = aggregator.Receive()

            homeSend=home.sendData("Pimported",home.Pimported,aggregator.jid)

            aggregator.add_behaviour(aggReceive)
            
            home.add_behaviour(homeSend)

            aggReceive.join()

            homeSend.join()

            PV=aggReceive.Data

            aggpath=AggregatorPath + '\ ' + str(home.name)

            aggSave=aggregator.saveData(PV,aggpath,"Pimported","txt")

            aggregator.add_behaviour(aggSave)

            aggSave.join()

        # ########################## SEND EXPORTED POWER TO AGGREGATOR ####################################

        print("########################## HOMES SEND EXPORTED POWER TO AGGREGATOR ####################################")

        for home in aggregator.HomeList:

            print("\n #######################################################################\n")

            print(home.name)

            homepath=HomePath + str(home.name)

            homeSave=home.saveData(home.Pexported,homepath,"Pexported","txt")

            home.add_behaviour(homeSave)

            homeSave.join()

            homePlot=home.Plot("Exported Power "+str(home.name)+ (" (Watts)"),home.Pexported)

            home.add_behaviour(homePlot)

            homePlot.join()

            aggReceive = aggregator.Receive()

            homeSend=home.sendData("Pexported",home.Pexported,aggregator.jid)

            aggregator.add_behaviour(aggReceive)
            
            home.add_behaviour(homeSend)

            aggReceive.join()

            homeSend.join()

            P=aggReceive.Data

            aggpath=AggregatorPath + '\ ' + str(home.name)

            aggSave=aggregator.saveData(P,aggpath,"Pexported","txt")

            aggregator.add_behaviour(aggSave)

            aggSave.join()


        # ########################## SEND INITIAL STORED ENERGY TO AGGREGATOR ####################################

        print("################  SEND INITIAL STORED ENERGY TO AGGREGATOR ########################################")

        for home in aggregator.HomeList:

            print("\n #######################################################################\n")

            print(home.name)

            homepath=HomePath + str(home.name)

            homeSave=home.saveData(home.battery.initialEnergy,homepath,"initialStoredEnergy","txt")

            home.add_behaviour(homeSave)

            homeSave.join()

            aggReceive = aggregator.Receive()

            homeSend=home.sendData("initialStoredEnergy",home.battery.initialEnergy,aggregator.jid)

            aggregator.add_behaviour(aggReceive)
            
            home.add_behaviour(homeSend)
           
            aggReceive.join()

            homeSend.join()

            IE=aggReceive.Data

            aggpath=AggregatorPath + '\ ' + str(home.name)

            aggSave=aggregator.saveData(IE,aggpath,"initialStoredEnergy","txt")

            aggregator.add_behaviour(aggSave)

            aggSave.join()

        # ########################## SEND BATTERY CAPACITY TO AGGREGATOR ####################################


        print("# ########################## SEND BATTERY CAPACITY TO AGGREGATOR ####################################")

        for home in aggregator.HomeList:

            print("\n #######################################################################\n")

            print(home.name)

            homepath=HomePath + str(home.name)

            homeSave=home.saveData(home.battery.cap,homepath,"Battery Capacity","txt")

            home.add_behaviour(homeSave)

            homeSave.join()

            aggReceive = aggregator.Receive()

            homeSend=home.sendData("Battery Capacity",home.battery.cap,aggregator.jid)

            aggregator.add_behaviour(aggReceive)

            home.add_behaviour(homeSend)
            
            aggReceive.join()

            homeSend.join()

            CB=aggReceive.Data

            aggpath=AggregatorPath + '\ ' + str(home.name)

            aggSave=aggregator.saveData(CB,aggpath,"Battery Capacity","txt")

            aggregator.add_behaviour(aggSave)

            aggSave.join()


        # ########################## SEND SOC TO AGGREGATOR ####################################

        print("########################## HOMES SEND SOC TO AGGREGATOR ####################################")

        for home in aggregator.HomeList:

            print("\n #######################################################################\n")

            print(home.name)

            homepath=HomePath + str(home.name)

            homeSave=home.saveData(home.battery.soc,homepath,"SOC","txt")

            home.add_behaviour(homeSave)

            homeSave.join()

            homePlot=home.Plot("SOC battery "+str(home.name)+ (" (Watts)"),home.battery.soc)

            home.add_behaviour(homePlot)

            homePlot.join()

            aggReceive = aggregator.Receive()

            homeSend=home.sendData("SOC",home.battery.soc,aggregator.jid)

            aggregator.add_behaviour(aggReceive)
            
            home.add_behaviour(homeSend)

            aggReceive.join()

            homeSend.join()

            soc=aggReceive.Data

            aggpath=AggregatorPath + '\ ' + str(home.name)

            aggSave=aggregator.saveData(soc,aggpath,"SOC","txt")

            aggregator.add_behaviour(aggSave)

            aggSave.join()


        
        # ########################## SEND OPERATION WINDOW OF HOME'S FLEXIBLE APPLIANCES TO AGGREGATOR ####################################

        print("# ########################## SEND OPERATION WINDOW OF HOME'S FLEXIBLE APPLIANCES TO AGGREGATOR ####################################")

        for home in aggregator.HomeList:

            print("\n #######################################################################\n")

            print(home.name)

            homepath=HomePath + str(home.name)

            i=0

            for appliance in home.FA_list:

                i=i+1

                homeSave=home.saveData(appliance.operationWindow.tolist(),homepath,"Operation Window FA_"+str(i)+" " +str(home.name),"txt")

                home.add_behaviour(homeSave)

                homeSave.join()

                aggReceive = aggregator.Receive()

                homeSend=home.sendData("Operation Window FA_"+str(i)+" " +str(home.name),appliance.operationWindow.tolist(),aggregator.jid)

                aggregator.add_behaviour(aggReceive)

                home.add_behaviour(homeSend)

                aggReceive.join()

                homeSend.join()

                CB=aggReceive.Data

                aggpath=AggregatorPath + '\ ' + str(home.name)

                aggSave=aggregator.saveData(CB,aggpath,"Operation Window FA_"+str(i)+" " +str(home.name),"txt")

                aggregator.add_behaviour(aggSave)

                aggSave.join()

        # ########################## SEND START TIME OF HOME'S FLEXIBLE APPLIANCES TO AGGREGATOR ####################################


        print("# ########################## SEND START TIME OF HOME'S FLEXIBLE APPLIANCES TO AGGREGATOR ####################################")

        for home in aggregator.HomeList:

            print("\n #######################################################################\n")

            print(home.name)

            homepath=HomePath + str(home.name)

            i=0

            for appliance in home.FA_list:

                i=i+1

                homeSave=home.saveData(appliance.st,homepath,"Start Time FA_"+str(i)+" " +str(home.name),"txt")

                home.add_behaviour(homeSave)

                homeSave.join()

                aggReceive = aggregator.Receive()

                homeSend=home.sendData("Start Time FA_"+str(i)+" " +str(home.name),appliance.st,aggregator.jid)

                aggregator.add_behaviour(aggReceive)

                home.add_behaviour(homeSend)

                aggReceive.join()

                homeSend.join()

                CB=aggReceive.Data

                aggpath=AggregatorPath + '\ ' + str(home.name)

                aggSave=aggregator.saveData(CB,aggpath,"Start Time FA_"+str(i)+" " +str(home.name),"txt")

                aggregator.add_behaviour(aggSave)

                aggSave.join()

#   ################### AGGREGATOR IMPORT ALL THE PV POWER RECEIVED, SAVES THE TOTAL THEN SENDS IT TO HOMES ##########


    print("################### AGGREGATOR IMPORT ALL THE PV POWER RECEIVED, SAVES THE TOTAL THEN SENDS IT TO HOMES ##########")



    values=[]    #    Temporarily keep the imported values to compute the sum 


    for i in range( len(aggregator.HomeList)):

        home=aggregator.HomeList[i]

        Path=AggregatorPath+'\ ' + str(home.name)

        aggimport=aggregator.importData(Path,"PV","txt")

        aggregator.add_behaviour(aggimport)

        aggimport.join()

        values.append(aggimport.Data)

        # aggPlot=aggregator.Plot("PV Generation "+str(home.name)+ (" (Watts)"),values[i])

        # aggregator.add_behaviour(aggPlot)

        # aggPlot.join()

    # 

    aggSave=aggregator.saveData(sum(values).tolist(),AggregatorPath,"TotalPV","txt")

    aggregator.add_behaviour(aggSave)

    aggSave.join()

    aggPlot=aggregator.Plot("Total PV Generation (Watts)",sum(values))

    aggregator.add_behaviour(aggPlot)

    aggPlot.join()

    # AGGREGATOR SENDS TOTAL PV TO HOMES


    for home in aggregator.HomeList:

        print("\n #######################################################################\n")

        print(home.name)

        homepath=HomePath + str(home.name)

        homeReceive = home.Receive()

        aggSend=aggregator.sendData("TotalPV",sum(values).tolist(),str(home.jid))
        
        home.add_behaviour(homeReceive)

        aggregator.add_behaviour(aggSend)

        homeReceive.join()

        aggSend.join()

        PV=homeReceive.Data

        homeSave=home.saveData(PV,homepath,"TotalPV","txt")

        home.add_behaviour(homeSave)

        homeSave.join()


#   ################### AGGREGATOR IMPORT ALL THE CONSUMPTIONS RECEIVED, SAVES THE TOTAL THEN SENDS IT TO HOMES ##########


    print("   ################### AGGREGATOR IMPORT ALL THE CONSUMPTIONS RECEIVED, SAVES THE TOTAL THEN SENDS IT TO HOMES ##########")



    values=[]    #    Temporarily keep the imported values to compute the sum 


    for i in range( len(aggregator.HomeList)):

        home=aggregator.HomeList[i]

        Path=AggregatorPath+'\ ' + str(home.name)

        aggimport=aggregator.importData(Path,"PL","txt")

        aggregator.add_behaviour(aggimport)

        aggimport.join()

        values.append(aggimport.Data)

        # aggPlot=aggregator.Plot("PV Generation "+str(home.name)+ (" (Watts)"),values[i])

        # aggregator.add_behaviour(aggPlot)

        # aggPlot.join()

    # 

    aggSave=aggregator.saveData(sum(values).tolist(),AggregatorPath,"TotalPL","txt")

    aggregator.add_behaviour(aggSave)

    aggSave.join()

    aggPlot=aggregator.Plot("Total Consumption (Watts)",sum(values))

    aggregator.add_behaviour(aggPlot)

    aggPlot.join()

    # AGGREGATOR SENDS TOTAL PV TO HOMES


    for home in aggregator.HomeList:

        print("\n #######################################################################\n")

        print(home.name)

        homepath=HomePath + str(home.name)

        homeReceive = home.Receive()

        aggSend=aggregator.sendData("TotalPL",sum(values).tolist(),str(home.jid))
        
        home.add_behaviour(homeReceive)

        aggregator.add_behaviour(aggSend)

        homeReceive.join()

        aggSend.join()

        PV=homeReceive.Data

        homeSave=home.saveData(PV,homepath,"TotalPL","txt")

        home.add_behaviour(homeSave)

        homeSave.join()

    import numpy as np
    socsbefore=[]

    for home in aggregator.HomeList:

        socsbefore.append(np.array(home.battery.soc))
        
    


    ch=aggregator.chargeHomes()

    aggregator.add_behaviour(ch)

    ch.join()
    

    socsAfter=[]

    for home in aggregator.HomeList:
        socsAfter.append(home.battery.soc)


    a=0
    for w in socsbefore:
        a=a+1
        plt.plot(np.array(t2)/4,w,label= "home "+str(a))
        
        plt.rc('legend',fontsize=8) # using a size in points

        plt.legend(loc=2)

    plt.title("SOCS Before")

    plt.grid()

    plt.xlabel("Time of the day ")
    plt.ylabel("SOC ")
    plt.savefig("SOCS Before charge.svg", dpi=300, bbox_inches='tight')
    plt.show()
    
    u=0
    for j in socsAfter:
        u=u+1
        plt.plot(np.array(t2)/4,j,label= "home "+str(u))
        
        plt.rc('legend',fontsize=8) # using a size in points
    

        plt.legend(loc=2)
    plt.title("SOCS After")
    plt.grid()
    plt.xlabel("Time of the day ")
    plt.ylabel("SOC ")
    plt.savefig("SOCS After.svg", dpi=300, bbox_inches='tight')
    plt.show()



    plt.figure()
    
    plt.plot(np.array(t1)/4,ch.Rempowerbeforecharge)
    
    plt.title(" Remaining Power before charge")

    plt.grid()

    plt.xlabel("Time of the day ")
    plt.ylabel("Remaining power (watts) ")
    plt.savefig("Remaining Power before charge.svg", dpi=300, bbox_inches='tight')
    plt.show()

    
    plt.figure()
    
    plt.plot(np.array(t1)/4,ch.RemPower)
    
    plt.title(" Remaining Power after charge")

    plt.grid()

    plt.xlabel("Time of the day ")
    plt.ylabel("Remaining power (watts) ")
    plt.savefig("Remaining power after.svg", dpi=300, bbox_inches='tight')
    plt.show()



    print("########## STOPPING AGENTS !!! #################")

    aggregator.stop()

    print ("aggregator stopped ! ")

    for home in aggregator.HomeList:

        home.stop()

        print(home.name+" stopped ! ")
    