##Create User
* adduser aries

##Change password
* passwd

##Delete User
* deluser aries

##Install Openvpn
* yum update 
* yum install epel-release -y
* yum install -y openvpn wget

##Install Metasploit
* curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall && chmod 755 msfinstall && ./msfinstall

##Install nmap(also nc)
* yum install nmap

##Install gobuster
* git clone https://github.com/OJ/gobuster.git
* as /root is my GOPATH so these are in my /root/src
* github.com/hashicorp/go-multierror  
* github.com/OJ/gobuster  
* github.com/satori/go.uuid  
* golang.org/x/crypto  : https://github.com/golang/crypto.git
* golang.org/x/sys : https://github.com/golang/sys.git

###Install go
* wget https://dl.google.com/go/go1.10.3.linux-amd64.tar.gz
* tar -xvf go1.10.3.linux-amd64.tar.gz
* mv go /usr/local
* export GOROOT=/usr/local/go
* export GOPATH=$HOME
* export PATH=$GOROOT/bin:$PATH

##Install python3.6
* yum -y install yum-utils
* yum -y groupinstall development
* yum -y install https://centos7.iuscommunity.org/ius-release.rpm
* yum -y install python36u

##Install googler
* wget -c https://github.com/jarun/googler/archive/v2.9.tar.gz
* tar -xvf  v2.9.tar.gz
* cd  googler-2.9
* make install 
* cd auto-completion/bash/
* cp googler-completion.bash  /etc/bash_completion.d/

##Install npm
* yum install npm

##Install pageres
* npm install -g pageres-cli(this is stupid)