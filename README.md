#15.4 release tag

#developers user

#1.edit ~/.ssh/config
HOST cr.deepin.io
	Port 29418
	User 用户名

cp pre-commit .git/hooks/

#2.git clone deepin-code-project
 git submodule init
 git submodule update project/$project 
##you can download module code
## $project can review and push for normal and without interference 
　
#3.version project
##deepin-code-project review use to control the release version
