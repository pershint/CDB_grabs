The scripts contained here are for accessing the slow control couchDB for
miscillaneous data viewing.  

To use this file:

  1) Go to ./conf/ and create a file named couchcred.conf
  2) In this file insert the following lines:

     username XXXXXXXX
     password XXXXXXXX

     where the X's are to be filled with the SNO+ collaboration credentials.


  3) For GrabCavityTemps.py: enter the file an modify the number of days back
     into the couchDB database you want to acquire temperature data for.  You
     can also modify how many data points you want for each day into the past. 
