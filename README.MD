## 当前功能
## 有问题issues
**2023-12-11**
+ 修改bug
+ 完善日报和周报

**2023-12-9**  
+ 1 新增提交日报
+ 2 新增提交周报
  
**2023-12-4**
1. 打卡
2. 补签(补前未30天打卡)
## 声明

**仅供学习交流使用**，项目遵循GPL协议，请勿拿来盈利、诈骗和违法之事！

项目产生的所有结果皆由使用者负责，本项目仅提供Python学习参考价值，本人不进行任何运行和调试。

- [x] 运行和调试本项目则表示为默认同意以上声明

## 基本使用
>1.pip install -r requirements.txt   

>2.配置 user_config.json 文件

```angular2html
"password": "li hua", \\ 密码
"phone": "1111xxxx",   \\ 手机号
"address": "山东省菏泽市曹县某某街道",
"latitude": "34.830624",   \\ 纬度
"longitude": "115.545005", \\ 经度
"start_time": "08", \\ 打卡开始时间
"end_time": "21",    \\ 打卡结束位置
"city": "菏泽市",
"province": "山东省",
"is_repeat_clock_in": false \\ 默认不补签
"is_submit_daily": false, \\ 默认不提交日报
"is_submit_weekly": false,\\ 默认不提交周报
"submit_weekly_time": 1 \\ 星期几提交周报
```

## **补签说明**：
1. 默认补签前30天的数据(只能补签到前30天的)
2. 默认只补签上班(app默认只支持上班,保存和app统一原则),若学校有要求只需要修改请求的type改END,变成打下班卡
3. 补签时间说明,默认是早上8或9点随机时间,随机秒打卡,若修改则自行修改
### 自动打卡
验证该环境能否打卡最简单的方法,看该环境能不能登录网页版   
**某鱼上有几块一个月的移某云,可以用安卓模拟器的(不是打广告,我也不是卖云服务器的)**    
买代理(有点贵)，免费的代理不太稳定(频繁切换ip好像会封号)     
某讯和某里的云服务器大概率不行(deny了)     
有条件上**树莓派**挂寝室里   
没条件买**挂机宝**，**云手机**也可以 
## start
[![Stargazers over time](https://starchart.cc/github123666/gonxueyun.svg)](https://starchart.cc/github123666/gonxueyun)
