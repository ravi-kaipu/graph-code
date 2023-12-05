# graph-code

Visualize your code flow. <br><br>

**OUTPUT:** <br>

```
Comp1                          Comp2                          Comp3                          Comp4 
|                              |                              |                              | 
|                              |             add_subscriber(): init_subscriber_cb            |
|                              |------------------------------------------------------------>|
|             add_resource(): init and release cb             |                              |
|------------------------------------------------------------>|                              |
|                              |                              |   add_component_resource()   |
|                              |                              |----------------------------->|
|                              |                              |   component resource added   |
|                              |                              |<-----------------------------|
|                        resource added                       |                              |
|<------------------------------------------------------------|                              |
|                              |                     init_subscriber_cb()                    |
|                              |<------------------------------------------------------------|
|       execute init_cb        |                              |                              |
|<-----------------------------|                              |                              |
```
