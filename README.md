NASB
This language adds blocks to NAS
Instead of your conditionals looking like this:
```
#onJoin
    if a|=|5 jump #1
    jump #2
    #1
    msg a is 5
    msg condition accepted
    #2
    quit
```
they look like this:
```
#onJoin
    if a|=|5 then
        msg a is 5
        msg condition accepted
    end
    quit
```
This language is compatible with existing NAS code without modification, and compiles directly into NAS code.
