#!/usr/bin/python

#When ran, this code grabs the set amount of data points for the
#DeltaV cavity temperatures and plots them using matplotlib.

import lib.couchutils as cu
import matplotlib.pyplot as plt

onemindb = "slowcontrol-data-1min"
oneminview = "pi_db"
ctdb = "slowcontrol-data-cavitytemps"
ctview = "by_timestamp"

##### MODIFY AS DESIRED FOR TEMPERATURE PLOTS ########
numdays = 2        #rough number of days of data you want to plot
ppd_desired = 10  #Number of data points you want for each day
DATARESOLUTION = 60   #Distance in time between database entries in sec
                      #This is 60 for 1min databases, 300 for the temp. sensor ropes
#### END MODIFICATION REGION ######



DAYTOSEC = 86400  # Num. days in a second
querylen = 1000
POINTSPERDAY = DAYTOSEC/DATARESOLUTION

num_queries = int(POINTSPERDAY*numdays/querylen) + 1

Index_resolution = POINTSPERDAY/ppd_desired

def getRecentCavityTemps(dbname,viewname):
    timestamps = []
    temps = []
    querynum=0
    firstquery = True
    nextquerykey = None
    dbDataStatus, dbData = cu.connectToDB(dbname)
    if dbDataStatus is "ok":
        while querynum < num_queries:
            if viewname is not None:
                if firstquery:
                    queryresults = dbData.view(dbname+"/"+viewname,descending=True,limit=querylen)
                    firstquery = False
                    querynum+=1
                else:
                    queryresults = dbData.view(dbname+"/"+viewname,startkey=nextquerykey, \
                            descending=True,limit=querylen)
                    querynum+=1
                try:
                    j=0
                    print("IN TRY LOOP")
                    for row in queryresults:    #Why couchDB, why you do this
                        j+=1
                        if int(j/(Index_resolution)) == (float(j)/float(Index_resolution)):
                            print(int(j/Index_resolution))
                            timestamps.append(row.value["timestamp"])
                            temps.append(row.value["cavity_water_temp"]["values"][0])
                        elif j==querylen-1:
                            nextquerykey = timestamps[len(timestamps)-1]
                            break
                        else:
                            continue
                except:
                    print("There was a problem trying to read the query results.")
                    dbDataStatus = "bad"
    else:
        print("NO CONNECTION TO COUCHDB AT ALL.  RETURNING WHAT I GOT BEFORE DUMPING")
    return timestamps, temps

if __name__ == "__main__":
    timestamps, temps = getRecentCavityTemps(onemindb, oneminview)
    print(timestamps)
    print(temps)
    plt.plot(timestamps,temps)
    plt.show()



