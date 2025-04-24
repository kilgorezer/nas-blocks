# NASB (Not Awesome Script Blocks)
This language adds blocks to NAS\
Instead of your conditionals looking like this:
```
using local_packages
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
using local_packages
#onJoin
    if a|=|5 then
        msg a is 5
        msg condition accepted
    end
    quit
```
This language is compatible with existing NAS code without modification, and compiles directly into NAS code.\
Primary differences are the file extension is .nasb instead of .nas, and the `then` and `end` commands now exist.\
\
Usage:\
`[standard conditional with conditions] then` - start block\
`end` - end block\
\
It is recommended to enable [local packages](https://notawesome.cc/docs/nas/documentation.nas#:~:text=using%20local_packages%0A).
