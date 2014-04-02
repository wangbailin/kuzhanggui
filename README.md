rocket
======

weixin platform for business


##deploy
服务器上使用了[virtualenv](http://virtualenv.org)，在部署之前，需要修改一些环境变量
```bash
#执行这个脚步可快速修改环境变量
source /path/to/ENV/bin/activate
```
项目当中有一些预先加入的一些资源（包括主题资源和预先写好的文案，在resources目录里），需要放到MEDIA_ROOT下
```bash
./manage.py deploy_resources
```
