import numpy as np 
import sqlite3 as lite
from astropy.table import Table
import time

observations = Table().read('file_info_for_problem.csv' )


ID = observations['ID'].data
FieldID = observations['FieldID'].data
Filename = observations['Filename'].data
Filter = observations['Filter'].data
MJD = observations['MJD'].data
Airmass = observations['Airmass'].data
Exptime = observations['Exptime'].data

# changes filenames to the names of the fits tables
# gives observations with multiple observations an extension 'E[# of exposure]'
filters = set(Filter)
for filter in filters:
    for id in set(FieldID[Filter == filter]):
        counter = 1
        dates = MJD[ (Filter == filter) & (FieldID == id)]
        for date in np.sort(dates ):
            i = np.where((MJD == date) & (Filter == filter) & (FieldID == id)) 
            if (len(dates) > 1 or filter == 'Ks'):
                extension = "-E" + format(counter, '03') + ".fits"
                counter += 1
            else:
                extension = ".fits"
            observations['Filename'][i] = "Field-" + str(FieldID[i][0]) + "-" + str(Filter[i][0]) + extension

print observations


def isNumber(s):
    try:      
        float(s)
        return True
    except ValueError:
        return False

def create_filter_table(con, field, filter, data):
    table = filter 
    #TODO remove unnecessary data like: runningID, ObservationID, X, Y; move StarID to front
    command = """CREATE TABLE IF NOT EXISTS {0} (FieldID INT, StarID INT, 
    Ra DOUBLE, Dec DOUBLE, Flux1 DOUBLE, dFlux1 DOUBLE, Mag1 DOUBLE, dMag1 DOUBLE, 
    PRIMARY KEY(StarID) )""".format(table)
    con.execute(command)
    for i in data['StarID']:
        command = "INSERT INTO {} VALUES(".format(table) + str(field) + ',' + str(i)
        for col in ['Ra', 'Dec', 'Flux1', 'dFlux1', 'Mag1', 'dMag1']:
            j = data[col][data['StarID'] == i][0]
            if np.isnan(j):
                arg = "NULL"
            elif isNumber(j):
                arg = str(j)
            else:
                arg = "'" + j + "'"
            command += "," + arg 

        command += ")"
        con.execute(command)

def create_data_table(con, ID, filename):
    table = 'Data'
    data = Table().read(filename)

    command = """CREATE TABLE IF NOT EXISTS {0} (ObservationID INT, RunningID INT,
    X INT, Y INT, Flux1 DOUBLE, dFlux1 DOUBLE, Flux2 DOUBLE, dFlux2 DOUBLE, 
    Flux3 DOUBLE, dFlux3 DOUBLE, Ra DOUBLE, Dec DOUBLE, Class INT, Mag1 DOUBLE, 
    Mag2 DOUBLE, Mag3 DOUBLE, dMag1 DOUBLE, dMag2 DOUBLE, dMag3 DOUBLE, StarID INT, 
    FOREIGN KEY(ObservationID) references Observations(ID))""".format(table)
    con.execute(command)

    for i in range(len(data['RunningID'].data)):
        row = data[i]
        command = "INSERT INTO Data VALUES(" + str(ID)
        for j in row:
            if np.isnan(j):
                arg = "NULL"
            elif isNumber(j):
                arg = str(j)
            else:
                arg = "'" + j + "'"
            command += "," + arg 

        command += ")"
        #print command
        con.execute(command)
    
def create_observationsDB():
    database = 'observations.db'
    con = lite.connect(database)
    with con:
        table = 'Observations'
        command = """CREATE TABLE IF NOT EXISTS {0} (ID INT, FieldID INT, 
        Filename varchar(20), Filter varchar(5), MJD DOUBLE, Airmass DOUBLE, 
        Exptime DOUBLE, UNIQUE(ID), PRIMARY KEY(ID))""".format(table)
        
        con.execute(command)

        for i in range(len(ID)):
            row = observations[i]
            command = "INSERT INTO Observations VALUES({0},{1},'{2}','{3}',{4},{5},{6})".format(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            con.execute(command)
            create_data_table(con, row[0], row[2])

        #flux_mag = ['Flux1','Flux2','Flux3','Mag1','Mag2','Mag3']
        #dflux_dmag = ['dFlux1','dFlux2','dFlux3','dMag1','dMag2','dMag3']
        
        #create different tables for the different filters, 
        for field in set(FieldID):
            for filter in set(Filter[field == FieldID]):
                files = Filename[(filter==Filter) & (field == FieldID)] 
                data = Table().read(files[0])

                datax = {}
                StarIDx = {}
                data_table = {}
                for col in ['StarID', 'Ra', 'Dec', 'Flux1', 'dFlux1', 'Mag1', 'dMag1']:
                    data_table[col] = data[col].data

                for file in files[1:]:
                    datax[file] = Table().read(file)
                    StarIDx[file] = datax[file]['StarID'].data
                    #print datax[file]['Flux1'][0],datax[file]['dFlux1'][0]
                if len(filter) > 1:
                    StarID = data_table['StarID']
                    #print data_table['Flux1'][0], data_table['dFlux1'][0],data_table['Mag1'][0],data_table['dMag1'][0]
                    for id in StarID:
                        for i in ['dFlux1','dMag1']:
                            data_table[i][StarID == id] **= 2 
                        for file in files[1:]:
                            for j in ['Flux1','Mag1']: #rows with flux or mag
                                data_table[j][StarID == id] += datax[file][j][StarIDx[file] == id]
                            for k in ['dFlux1','dMag1']: #rows with dflux or dmag
                                data_table[k][StarID == id] += datax[file][k][StarIDx[file] == id]**2
                        for l in ['Flux1', 'Mag1']:
                            data_table[l][StarID == id] = data_table[l][StarID == id] / len(files)
                        for m in ['dFlux1','dMag1']:
                            data_table[m][StarID == id] = data_table[m][StarID == id]**0.5 / len(files)
                    data = data_table
                    #print data_table['Flux1'][0], data_table['dFlux1'][0],data_table['Mag1'][0],data_table['dMag1'][0]

                '''Where there are multiple exposures, the data in the filter tables are of the first entry,
                 except for the magnitudes and fluxes and their uncertainties, those are averaged among the files '''
                print filter, field, len(files)
                #print time.time() - t0
                create_filter_table(con, field, filter, data)


t0 = time.time()
create_observationsDB()
