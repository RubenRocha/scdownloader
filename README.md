scdownloader
============

Soundcloud downloader, supporting playlists and usernames, and also metadata downloading with the `-m` switch.

Please remember to edit the client_id in `sc.py`.
You can achieve this by opening the network tab of your browser, and performing pretty much any action, like clicking play on a song. You will get something similar to this, with one of the parameters being client_id.
![client_id demonstration](http://i.imgur.com/aQTOPYi.png "Demonstration")


usage
=====

`./sc.py -h`

  Displays usage help.
    
`./sc.py -u christchilds`

  Gets tracks for user `christchilds`
    
`./sc.py -p https://soundcloud.com/user146407550/sets/drum-and-bass`

  Gets tracks from playlist `drum-and-bass` by user `user146407550`
  
`./sc.py -m -u christchilds`

  Gets tracks for user `christchilds` also downloading the metadata.
    
    
sample output
=============
`./sc.py -u christchilds`


[0] Found: Christchilds - Bass Set

[1] Found: Christchilds - Storm

[2] Found: Christchilds - Make It Bun Dem (Christchilds Beatport Contest Remix)

[3] Found: Christchilds - Pure Drum & Bass/Hardcore (MIX)

[4] Found: Christchilds - Winter

[5] Found: Christchilds - Be Strong - HalleluJAH (Drum Remix)

[6] Found: Christchilds - Dubstep Melody - DEMO

Enter the numbers to download, separated by commas (no spaces)
"all" if you want to download them all.

"x" if you want to exit.

Choice(s): 1,2


Downloading Christchilds - Storm... [##########] 100%

Downloading Christchilds - Make It Bun Dem (Christchilds Beatport Contest Remix)
... [#####     ] 59%
