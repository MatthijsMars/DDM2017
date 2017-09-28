import sqlite3 as lite

con = lite.connect("simple_tables.db")

rows = con.execute("select * from MagTable;")
print "MagTable"
print "|{0:10}|{1:10}|{2:12}|{3:10}|{4:10}|".format('Name','Ra','Dec','B','R')
for row in rows:
    print "|{0:10}|{1:10}|{2:12}|{3:10}|{4:10}|".format(row[0],row[1],row[2],row[3],row[4])
    
print ""
print '\n', "PhysTable"
rows2 = con.execute("select * from PhysTable;")
print "|{0:10}|{1:10}|{2:10}|".format('Name','Teff','FeH')
for row in rows2:
    print "|{0:10}|{1:10}|{2:10}|".format(row[0],row[1],row[2])

print ""
print "Ra & Dec of objects with B > 16"
rows3 = con.execute("select Name, Ra, Dec from MagTable where B > 16 ;")
print "|{0:10}|{1:10}|{2:12}|".format('Name','Ra','Dec')
for row in rows3:
    print "|{0:10}|{1:10}|{2:12}|".format(row[0],row[1],row[2])

print ""
print "B, R, Teff and FeH of all stars"
rows4 = con.execute("select m.Name, m.B, m.R, p.Teff, p.FeH from MagTable as m left join PhysTable as p on m.Name=p.Name ;")
print "|{0:10}|{1:10}|{2:10}|{3:10}|{4:10}|".format('Name','B','R', 'Teff','FeH')
for row in rows4:
    print "|{0:10}|{1:10}|{2:10}|{3:10}|{4:10}|".format(row[0],row[1],row[2],row[3],row[4])
    
print ""
print "table with B-R"
rows5 = con.execute("select Name, B-R as BR from MagTable;")
print "|{0:10}|{1:10}|".format('Name','B-R')
for row in rows5:
    print "|{0:10}|{1:10}|".format(row[0],row[1])    
    
