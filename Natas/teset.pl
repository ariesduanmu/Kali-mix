use warnings;
use strict;


use DBI;
my $db="...";
my $host="localhost";
my $user="root";
my $password="toor"; # Standard Kali

# connect
my $dbh   = DBI->connect ("DBI:mysql:database=$db:host=$host",
                           $user,
                           $password) 
                           or die "Can't connect to database: $DBI::errstr\n";

#disconnect
$dbh->disconnect or warn "Disconnection error: $DBI::errstr\n";
exit;