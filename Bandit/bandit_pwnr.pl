#!/usr/bin/perl

use strict;
use warnings;

use Net::SSH::Perl;

my $hostname = "bandit.labs.overthewire.org";
my $username = "bandit0";
my $password = "bandit0";
my $port = "2220";
my $command = "";

my $bandit_count = 10;

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


# I tried to hash this... PERL debugging is shit
# sub read_file {
#     my %hash;
#     open my $fh, "commands.txt" or die;
#     while (my $line = <$fh>) {
#         chomp $line;
#         print $line . "\n";
#         my ($lvl, $cmd) = split /:/, $file;
#         $hash{$lvl} = $cmd;
#     }
#     return $hash;
# }

sub next_command {
    my ($user) = @_;
    my ($num) = $user =~ /(\d+)/;
    if ($num == 0){
        return "cat readme";
    }
    elsif ($num == 1){
        return "cat ./-";
    }
    elsif ($num == 2){
        return "cat 'spaces in this filename'";
    }
    elsif ($num == 3){
        return "cd inhere && cat .hidden";
    }
    elsif ($num == 4){
        return "cd inhere && cat ./-file07";
    }
    elsif ($num == 5){
        return "cd inhere && cat ./maybehere07/.file2";
    }
    elsif ($num == 6){
        return "cat /var/lib/dpkg/info/bandit7.password";
    }
    elsif ($num == 7){
        return "cat data.txt | grep millionth | sed -e 's/^millionth//'";
    }
}

while ($bandit_count > 0)
{
    print "$username:$password\n";
    $command = next_command($username);
    $password = bandit_level($password, $username, "$command");
    chomp $password;
    $password =~ s/\s//g;
    $username = next_level($username);
    $bandit_count--;
}
