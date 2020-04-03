import pylatlon
a = pylatlon.latlon(10.425,-20.004)
#d = pylatlon.latlon.strp('34 54','%dlon %dlat')
d = pylatlon.latlon.strp('54N 30 15.0 -45.3E 30 40','%dlat%NS %mlat %slat %dlon%EW %mlon %slon')
#d = pylatlon.latlon.strp('45.3E','%ddlonEW')
#d = pylatlon.latlon.strp('45.3E','%ddlonE')
#d = pylatlon.latlon.strp('34','%dlon')
print(d.strf(format=1))
print(d.strf(format=2))
