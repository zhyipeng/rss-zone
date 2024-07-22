BUILD_TIME=$(shell date  '+%Y%m%d')

build:
	docker build -t rss-zone --platform=linux/amd64 .

push:
	docker tag rss-zone registry.cn-hangzhou.aliyuncs.com/azhyipeng/rss-zone:$(BUILD_TIME)
	docker push registry.cn-hangzhou.aliyuncs.com/azhyipeng/rss-zone:$(BUILD_TIME)
	docker tag rss-zone registry.cn-hangzhou.aliyuncs.com/azhyipeng/rss-zone:latest
	docker push registry.cn-hangzhou.aliyuncs.com/azhyipeng/rss-zone:latest

