FROM centos:7
ENV container docker

# Install packages 
RUN yum update -y

# EPEL releases are required
# otherwise mock 1.2.17-1.el7.centos is installed which date backs to 2016
# later versions of mock include required repositories for devtoolset
# allowing us to install devtoolset-7-gcc via BuildRequires in spec.
RUN yum install epel-release -y
RUN yum update -y

RUN yum install git wget nano -y

# Required RPM tools
RUN yum install mock rpm-build rpm-sign rpmdevtools rpmlint -y

# nspawn can't run inside a docker currently
RUN echo "config_opts['use_nspawn'] = False" >> /etc/mock/site-defaults.cfg
