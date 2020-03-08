## 基金套利提醒脚本

### 文件说明
* `bondReminder.py` : 可转债打新提醒，每个交易日的 9:30 推送消息。
* `fundReminder.py` : LOF基金和QDII基金的溢价提醒，每个交易日的 14：00 推送消息。

### 第三方服务
* 数据来源：[集思录](https://www.jisilu.cn/)
* 消息提醒服务：[WxPusher](http://wxpusher.zjiecode.com/docs/#/)
* 项目部署环境：[Heroku](https://www.heroku.com/)