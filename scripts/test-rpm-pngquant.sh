#! /usr/bin/sh

# pngquant requires epel repo for libimagequant-2.12.5-1.el7.x86_64
yum install epel-release -y

# remove pngquant if installed
rpm -e pngquant

# install built rpm package
yum install /root/result/pngquant-2.12.5-1.el7.x86_64.rpm -y

echo "/usr/bin/pngquant -h"
/usr/bin/pngquant -h

echo "ldd /usr/bin/pngquant"
ldd /usr/bin/pngquant