#! /usr/bin/sh

install -d /root/rpmbuild/SOURCES/

\cp /root/data/pngquant-old_libpng.patch /root/rpmbuild/SOURCES/pngquant-old_libpng.patch

rpmbuild --undefine=_disable_source_fetch -bs /root/data/pngquant.spec

# mock user can't access /root/rpmbuild/SRPMS/, cp to /tmp where it can access.
\cp /root/rpmbuild/SRPMS/pngquant-2.12.5-1.el7.src.rpm /tmp/pngquant-2.12.5-1.el7.src.rpm

id -u mock &>/dev/null || useradd mock -g mock

su --login mock --command "mock -r epel-7-x86_64 /tmp/pngquant-2.12.5-1.el7.src.rpm --old-chroot"

# use --no-clean for debugging
# su --login mock --command "mock -r custom_repos_centos-7-x86_64 /tmp/pngquant-2.12.5-1.el7.src.rpm --old-chroot --no-clean"

rm -rf /root/result/*

cp -r /var/lib/mock/epel-7-x86_64/result/* /root/result

bash /root/scripts/test-rpm-pngquant.sh