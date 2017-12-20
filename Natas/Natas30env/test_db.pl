use warnings;
use strict;


use DBI;
my $db="Natas30";
my $host="localhost";
my $user="root";
my $password="toor"; # Standard Kali

#create database
# my $dbh   = DBI->connect ("DBI:mysql:",
#                            $user,
#                            $password);
# $dbh->do("create database Natas30")

# connect
my $dbh   = DBI->connect ("DBI:mysql:database=$db;host=$host",
                           $user,
                           $password) 
                           or die "Can't connect to database: $DBI::errstr\n";


eval{ $dbh->do("Drop Table foo") };
$dbh->do("CREATE TABLE foo (name VARCHAR(100), password VARCHAR(20))");
$dbh->do("INSERT INTO foo VALUES(".$dbh->quote("natas30").", ".$dbh->quote("password").")");

my $sth = $dbh->prepare("SELECT * FROM foo");
$sth->execute();
while(my $ref = $sth->fetchrow_hashref()) {
    print "Found a row: name = $ref->{'name'}, password = $ref->{'password'}\n";
}
$sth->finish();

#disconnect
$dbh->disconnect or warn "Disconnection error: $DBI::errstr\n";
exit;
