# Tushare新浪财经新闻API插件

这是一个用于Dify平台的插件，通过接入Tushare API获取新浪财经新闻数据。

## 功能特点

- 获取指定日期范围内的新浪财经新闻
- 支持按新闻类别筛选
- 支持限制返回条数

## 安装方法

在Dify平台中，通过GitHub仓库URL安装此插件。

## 配置说明

安装后需配置环境变量：
- `TUSHARE_TOKEN`: 您的Tushare API令牌

## 使用方法

调用`get_sina_news`工具，传入以下参数：
- `start_date`: 开始日期(YYYYMMDD)
- `end_date`: 结束日期(可选)
- `category`: 新闻类别(可选)
- `limit`: 返回条数(可选)