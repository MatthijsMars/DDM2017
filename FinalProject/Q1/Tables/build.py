import numpy as np 
import sqlite3 as lite
from astropy.table import Table

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
        if (s != 'nan' and s!= 'NaN'):
            return True
        else:
            return False
    except ValueError:
        return False

def create_observationDB(con, ID, filename):
    table = 'Data'
    data = Table().read(filename)

    command = """CREATE TABLE IF NOT EXISTS {0} (ObservationID INT, RunningID INT,
    Ra DOUBLE, Dec DOUBLE, X INT, Y INT, Flux1 DOUBLE, dFlux1 DOUBLE, Flux2 DOUBLE,
    dFlux2 DOUBLE, Flux3 DOUBLE, dFlux3 DOUBLE, Class INT, Mag1 DOUBLE, Mag2 DOUBLE, 
    Mag3 DOUBLE, dMag1 DOUBLE, dMag2 DOUBLE, dMag3 DOUBLE, StarID INT, 
    FOREIGN KEY(ObservationID) references Observations(ID))""".format(table)
    con.execute(command)

    for i in range(len(data['RunningID'].data)):
        row = data[i]
        command = "INSERT INTO Data VALUES(" + str(ID)
        for idx, i in enumerate(row):
            if isNumber(i):
                arg = str(i)
            else:
                arg = "'" + i + "'"
            command += "," + arg 

        command += ")"
        #print command
        con.execute(command)


    
def create_observationsDB():
    database = 'observations.db'
    con = lite.connect(database)
    with con:
        table = 'Observations'
        # Create the command to create the table. I use a
        # multiline string to ease readability here.
        command = """CREATE TABLE IF NOT EXISTS {0} (ID INT, FieldID INT, 
        Filename varchar(20), Filter varchar(5), MJD DOUBLE, Airmass DOUBLE, 
        Exptime DOUBLE, UNIQUE(ID), PRIMARY KEY(ID))""".format(table)
        # Next, actually execute this command.
        con.execute(command)
        # Now that this is working, let us loop over the table entries
        # and insert these into the table.
        for i in range(len(ID)):
            row = observations[i]
            command = "INSERT INTO Observations VALUES({0},{1},'{2}','{3}',{4},{5},{6})".format(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            con.execute(command)
            create_observationDB(con, row[0], row[2])
        

create_observationsDB()
    