```
工学云&蘑菇钉支持任意地区打卡，周报提交,本月打卡补签,周报补交。
```
**2023-12-4**  
**看v2.0分支**    
**2023-12-2**  
决定还是重构一下代码   
**2023-11-27**

post请求参数可能对不上(但是加密没变),代码仅供参考
  
**2023-9-16**  （对称加密的密钥居然还没改）    

**答主打卡已经结束,不想改之前写的"史"了，有什么问题可以issues**   
1. 目前好像改一下代码中的sign就可以用    
2. 打卡的sign好像还是没变
3. 改变的sign    
**title是写报告时标题**

    <1> **周报**sign解密    
        title 可以自己随便填   
        title = '第一周'   
        week_sign = user_id + "week" + plan_id + title + "3478cbbc33f84bd00d75d7dfa69e0daa"
    
   <2> **日报** sign 解密   
       title 可以自己随便填    
        title = '第一周'    
        week_sign = user_id + "day" + plan_id + title + "3478cbbc33f84bd00d75d7dfa69e0daa"
   
    <3> **月报** sign 解密   
        title 可以自己随便填   
        title = '第一周'  
        week_sign = user_id + "month" + plan_id + title + "3478cbbc33f84bd00d75d7dfa69e0daa"  
**2022-12-7**    
       新增自动登录
## 下载配置
先将文件下载到本地，执行pip install -r requirement.txt安装需要的库  

配置：basic_info文件夹下user.txt

模板：  
{"phone":"138 xxxx xxxx", \
"password":"123456",\
"地址全称":"北京市 xxx xxx xxx",\
"经度":"23.xxxxx",\
"纬度":"114.xxxxx"，\
"start_time":"08",\
"end_time":"20"，      
 buqian:false ，//若为true，则会补签**本月**所有未签到的日期，！！！是所有(只支持补签上班或下班)  
 weekly:false,//若为true,则提交当前周周报  
 remedy:false, //是否补交周报(只有weekly为true的时候才能用,同时本周周报也会提交)  
 requirement_week_num:5,//需要补交前几周周报的数量,
 }     
默认是早8和晚8打卡，可以自行跟改,是否提交周报默认false
经纬度可以用 https://api.map.baidu.com/lbsapi/getpoint/ 来获取
## 声明

**仅供学习交流使用**，项目遵循GPL协议，请勿拿来盈利、诈骗和违法之事！

项目产生的所有结果皆由使用者负责，本项目仅提供Python学习参考价值，本人不进行任何运行和调试。

- [x] 运行和调试本项目则表示为默认同意以上声明
## 使用
运行**local_clock.py**   
week_diary中可以添加周报的内容,里面有默认配置   
提交周报时，会按照之前提交周报的总数量依次往下推,提交的内容则会按照现在是第几篇取basic_info/week_diary数组的索引
### 自动打卡
**某鱼上有几块一个月的移某云,可以用安卓模拟器的(不是打广告,我也不是卖云服务器的)**    
买代理(有点贵)，免费的代理不太稳定     
某讯和某里的云服务器大概率不行(deny了)     
有条件上**树莓派**挂寝室里   
没条件买**挂机宝**，**云手机**也可以 
