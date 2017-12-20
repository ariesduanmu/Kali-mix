use strict;
use warnings;
use DBI;

my $dbh = DBI->connect("DBI:mysql:database=test;host=localhost",
                       "","",
                       {'RaiseError' => 1});
$dbh->do("CREATE TABLE foo (username VARCHAR(100), password VARCHAR(100))");
$dbh->do("INSERT INTO foo VALUES (natas31, ".$dbh->quote("natas31").")");

my $sth = $dbh->prepare("SELECT * FROM foo");
$sth->execute();
while(my $ref = $sth->fetchrow_hashref()) {
    print "Found a row: id = $ref->{'username'}, name = $ref->{'password'}\n";
}
$sth->finish();
$dbh->disconnect();