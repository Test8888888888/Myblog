## 一个注重创作的轻博客系统

作为一名技术人员一定要有自己的**博客**，用来记录平时技术上遇到的问题，把**技术分享**出去就像滚雪球一样会越來越大，可以使用博客平台（简书、博客园、开源中国、CSDN等）来写博客，但我总感觉少了点什么，于是就在网上找了很多了博客系统，其实大同小异，于是就用业余时间用**python**开发了[h3blog](http://www.h3blog.com)，一个使用python开发的**轻量博客**系统，麻雀虽小但五脏也快长全了，功能一直都会不断更新...，你也可以先睹为快地址：[http://www.h3blog.com](http://www.h3blog.com)

## 用到的技术

- python
- flask
- flask-wtf
- flask-sqlalchemy
- markdown
- bootstrap4
- 支持sqlite、mysql等

数据库默认使用sqlite3，正式使用时请自行切换到mysql数据库

## 博客功能

- 撰写文章
- 文章列表
- 文章分类
- 标签管理
- 推荐文章
- 内置图床（使用七牛云做存储）
- 简单文字图片创造
- 网站设置
- 百度推送
- 会员注册
- 邀请码
- 搜索引擎抓取统计
- Diy定制模板

## 运行

h3blog一旦环境配置好 就是傻瓜式安装，根据提示操作就可以了

Linux 下运行环境配置
```bash
$ git clone https://gitee.com/pojoin/h3blog.git
$ cd h3blog
$ python -m venv venv  #创建python虚拟环境
$ source venv/bin/activate
$ 
$ pip install -r requirements.txt # 安装项目依赖，可能不全，根据提示自行安装即可
$ export FLASK_ENV=development
$ flask run # 启动
```

windows 下运行环境配置

```bash
> git clone https://gitee.com/pojoin/h3blog.git
> cd h3blog
> python -m venv venv  #创建python虚拟环境
> .\venv\Scripts\activate.bat #激活虚拟环境
> 
> pip install -r requirements.txt # 安装项目依赖，可能不全，根据提示自行安装即可
> set FLASK_ENV=development
> flask run # 启动
```

初次启动提示`连接数据库失败或setting表不存在`是正常的，因为还没有配置数据库及数据表

这时候打开浏览器访问地址：`http://127.0.0.1:5000` 根据提示初始化数据库及账户就可以开始使用了

后台管理登录入口地址：`http://127.0.0.1:5000/admin`

如果想重新配置数据库可删除app/config.py文件，重新访问`http://127.0.0.1:5000`根据提示进行即可


**项目配置文件推荐是.env进行私密配置，这也可以减少配置文件的修改**

## 博客部分截图

![初始化](https://images.gitee.com/uploads/images/2021/1105/151955_58428f31_120583.png "a1.png")
![设置数据库](https://images.gitee.com/uploads/images/2021/1105/152017_b6bfebfa_120583.png "sjk.png")
![设置账户](https://images.gitee.com/uploads/images/2021/1105/152032_022ce020_120583.png "zh.png")
![开始初始化](https://images.gitee.com/uploads/images/2021/1105/152100_0f2184dd_120583.png "安装.png")
![安装成功](https://images.gitee.com/uploads/images/2021/1105/152114_f45fc070_120583.png "安装成功.png")

![博客](https://images.gitee.com/uploads/images/2021/1105/151033_aa8a0b15_120583.png "wzsy.png")

![登录](https://images.gitee.com/uploads/images/2021/1105/151006_403e9961_120583.png "login.png")

![编辑](https://images.gitee.com/uploads/images/2021/1105/151100_eb3439d4_120583.png "write.png")
![图库](https://images.gitee.com/uploads/images/2021/1105/151119_8888e8f3_120583.png "tuchuang.png")
![Diy图片](https://images.gitee.com/uploads/images/2021/1105/151131_d769fb95_120583.png "diy_img.png")
![文章列表](https://images.gitee.com/uploads/images/2021/1105/151154_383a17bc_120583.png "wzlb.png")
![抓取日志](https://images.gitee.com/uploads/images/2021/1105/151213_e5454c67_120583.png "zqrz.png")

我的博客 [何三笔记](http://www.h3blog.com)
