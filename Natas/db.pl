use strict;
use warnings;
use DBI;


my $dbh = DBI->connect("DBI:mysql:database=MooCow;host=localhost",
                       "root","toor",
                       {'RaiseError' => 1});
eval{ $dbh->do("Drop Table foo") };
$dbh->do("CREATE TABLE foo (name VARCHAR(100), password VARCHAR(20))");
$dbh->do("INSERT INTO foo VALUES(".$dbh->quote("natas30").", ".$dbh->quote("password").")");

my $sth = $dbh->prepare("SELECT * FROM foo");
$sth->execute();
while(my $ref = $sth->fetchrow_hashref()) {
    print "Found a row: name = $ref->{'name'}, password = $ref->{'password'}\n";
}
$sth->finish();
$dbh->disconnect();