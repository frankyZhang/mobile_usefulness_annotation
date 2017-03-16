# 类的设计 #

## Action ##
Action 表示一个具体的用户行为。比如用户的点击，有一些基本的信息，比如行为发生的时间戳，task，
具体info中的字段可以用一个字典表示

Action中的主要方法parseFromLine是从一行日志中抽取出来相关的信息；
Action的Task字段有可能是空的，这样的应该丢弃；


## ActionSeries ##
Action 有两种可能，一种是在SERP上，另外一种可能是在LandingPage上，因此我们采用一个ActionSeries进行封装
最终Parse的结果是：
一个日志文件对应一个字典，字典的key是用户的task id；value是一个list
    list里面是一系列的ActionSeries对象，ActionSeries里面有一个list，里面对应一系列具体的Action
    
重要的TODO：ActionSeries里面的Action是可以极大的压缩的，例如，一个 scroll对象后面跟着一个或者多个ychange action，其实可以压缩，这样方便后面分析；
所以ActionSeries里面有一个方法，compress，这里面的逻辑可能比较复杂。 
