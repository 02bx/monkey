How to create a monkey build environment:

Windows:
1. Install python 2.7. Preferably you should use ActiveState Python which includes pywin32 built in. 
	You must use an up to date version, atleast version 2.7.10
	http://www.activestate.com/activepython/downloads
	https://www.python.org/downloads/release/python-2712/
2. install pywin32-219.win32-py2.7.exe at least
	http://sourceforge.net/projects/pywin32/files/pywin32/Build%20219/
3. a. install VCForPython27.msi
	http://www.microsoft.com/en-us/download/details.aspx?id=44266
   b. if not installed, install Microsoft Visual C++ 2010 SP1 Redistributable Package
    32bit: http://www.microsoft.com/en-us/download/details.aspx?id=8328
    64bit: http://www.microsoft.com/en-us/download/details.aspx?id=13523
4. Download & Run get-pip.py
	https://bootstrap.pypa.io/get-pip.py
5. Run:
	setx path "%path%;C:\Python27\;C:\Python27\Scripts"
	python -m pip install enum34
	python -m pip install impacket
	python -m pip install PyCrypto
	python -m pip install pyasn1
	python -m pip install cffi
	python -m pip install twisted
	python -m pip install rdpy
	python -m pip install requests
	python -m pip install odict
	python -m pip install paramiko
	python -m pip install psutil
	python -m pip install netifaces
	python -m pip install PyInstaller
	type > C:\Python27\Lib\site-packages\zope\__init__.py
7. Download and extract UPX binary to [source-path]\monkey\chaos_monkey\bin\upx.exe:
	http://upx.sourceforge.net/download/upx391w.zip
8. Run [source-path]\monkey\chaos_monkey\build_windows.bat to build, output is in dist\monkey.exe

Linux (Tested on Ubuntu 12.04):
1. Run:
	sudo apt-get update
	sudo apt-get install python-pip python-dev libffi-dev upx libssl-dev libc++1
	sudo pip install enum34
	sudo pip install impacket
	sudo pip install PyCrypto --upgrade
	sudo pip install pyasn1
	sudo pip install cffi
	sudo pip install zope.interface --upgrade
	sudo pip install twisted
	sudo pip install rdpy
	sudo pip install requests --upgrade
	sudo pip install odict
	sudo pip install paramiko
	sudo pip install psutil
	sudo pip install netifaces
	sudo pip install PyInstaller
	sudo apt-get install winbind
2. Put source code in /home/user/Code/monkey/chaos_monkey
3. To build, run in terminal:
	cd /home/user/Code/monkey/chaos_monkey
	chmod +x build_linux.sh
	./build_linux.sh
   output is in dist/monkey
