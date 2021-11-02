# libraryreservations
Automatically book library reservations for USC's trash system. Need 12 accounts in a logins.csv formatted as 

Name | USCID | Password

Also please change the room you book to (initURL) as I own 202B :|

For fully automatic cronjob

>00 00 * * * cd path/to/libraryreservations && python3 bot.py
