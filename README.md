# mobile_usefulness_annotation

## MobileSearch
* Android Project. 
* 其实主要部分就是一个Webbrowser，当时主要是用来记录日志，对于usefulness标注应该不需要，只是提供一个视图

## relevance_annotation
* Django Project.
* 这是标注时用的实验平台，usefulness标注的平台在此基础上按照我们的需求进行修改即可
* usefulness标注流程：
    + 实验指导
    + 任务描述
    + SERP展示（Dwell Time，Max Depth）及标注（usefulness）
    + 点击结果展示（Snippet，Dwell Time，用户需要点击landing page）及标注（usefulness，注意是landing page的usefulness）
    + satisfaction标注

## mobilesearchuserstudy
* 罗哥sigir2017的工作
* data中是实验数据的汇总，包括mobile_logs
* utils中是日志解析相关代码，解析的内容并不是特别多
* work中是罗哥的研究工作，跟mobile实验相关的主要是在user_behaviour中
