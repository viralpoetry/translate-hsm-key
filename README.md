# translate-hsm-key  

import, export multiple key cryptograms with Thales payShield 9000 using both TCP, Serial interface  

## How  
See `keys/config.csv` on how to define an example job with keys to be imported / exported.  

Anatomy of a job file:  
```
TCP; 192.168.1.3; 1500; ik; UAAAAAAAABBBBBBBCCCCCCCCCCCDDDDDD; keys_under_zcmk.txt; keys_under_lmk.txt
```

Where:  
`TCP / COM` - user TCP or Serial  
`x.x.x.x; 1500` - IP and Port for the TCP connection. In the case of COM, put just the port there  
`ik / ke` - (i)mport (k)ey or (k)ey (e)xport  
`UAAAAAAAABBBBBBBCCCCCCCCCCCDDDDDD` - some random looking transport key cryptogram under which the key on the input are encrypted  
`keys_under_zcmk.txt` - keys to import under HSM's Local Master Key  
`keys_under_lmk.txt` - output file  

Run `python batch_translate.py`  

## TODO:  
 - detect automatically if X/U prefix is required for Zone Control Master Key  
 - check if Key Check Values are the same after key translation  
 - create `collect_config` function that will collect all the configuration settings for audit purposes  
