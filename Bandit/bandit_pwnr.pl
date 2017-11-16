#!/usr/bin/perl

use strict;
use warnings;

use Net::SSH::Perl;

my $hostname = "bandit.labs.overthewire.org";
my $username = "bandit0";
my $password = "bandit0";
my $port = "2220";
my $command = "";



sub next_level {
    my ($user) = @_;
    $user =~ s/(\d+)\z/ $1 + 1 /e;
    return $user;
}

sub bandit_level {
    my ($pass, $user, $c) = @_;
    my $ssh = Net::SSH::Perl->new("$hostname", port=>$port, debug=>0);
    $ssh->login("$user","$pass");
    my ($stdout, $stderr, $exit) = $ssh->cmd("$c");
    my $new_pass = $stdout;
    return $new_pass;
}


sub read_file {
    my %hash;
    open CONFIG, "commands.txt" or die;
    while (my $line = <CONFIG>) {
        chomp $line;
        my ($lvl, $cmd) = split /:/, $line;
        $hash{$lvl} = $cmd;
    }
    close CONFIG;
    return %hash;
}


my %hash = read_file;
my $bandit_count = scalar(keys %hash);

while ($bandit_count-- > 0)
{
    print "$username:$password\n";
    $command = $hash{$username};
    $password = bandit_level($password, $username, "$command");
    chomp $password;
    $password =~ s/\s//g;
    $username = next_level($username);
}
