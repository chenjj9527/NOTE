Scrapy+mongodb循环递归爬取知乎用户信息

环境:python3

效果:见效果.png

缺陷:爬到一定数量，请求会失去相应。
	错误如下:
	2018-01-18 10:16:47 [scrapy.spidermiddlewares.httperror] INFO: Ignoring response <403 https://www.zhihu.com/api/v4/members/excited-vczh?include=loca。。。
	
待改进:可能需要动态IP和识别验证码
