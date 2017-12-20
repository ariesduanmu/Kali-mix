use strict;
use warnings;


{
    package MyWebServer;

    use DBI;
    use HTTP::Server::Simple::CGI;
    our @ISA = qw(HTTP::Server::Simple::CGI);

    my %dispatch = (
	'/index.pl' => \&resp_index,
	# ...
    );

    sub handle_request {
	my $self = shift;
	my $cgi  = shift;
      
	my $path = $cgi->path_info();
	my $handler = $dispatch{$path};

	if (ref($handler) eq "CODE") {
	    print "HTTP/1.0 200 OK\r\n";
	    $handler->($cgi);
	    
	} else {
	    print "HTTP/1.0 404 Not found\r\n";
	    print $cgi->header,
		  $cgi->start_html('Nothing here'),
		  $cgi->h1('Move along sir'),
		  $cgi->h2('You can got to localhost:8080/index.pl?username=user&password=pass'),
		  $cgi->end_html;
	}
    }

    sub resp_index {
	my $cgi  = shift;
	return if !ref $cgi;
	
	my $dbh = DBI->connect( "DBI:mysql:natas30","root", "toor", {'RaiseError' => 1});
	my $username = $cgi->param('username');
	my $quoted_username =  $dbh->quote($username);
	
	my $password = $cgi->param('password');
	my $quoted_password =  $dbh->quote($password);	
	
	my $query="Select * FROM users where username =" . $quoted_username . " and password =" . $quoted_password; 
	
	################################################################################
	# print 'Parameters: ' . $username . '\m' . $password . '\n';                  #
	# print 'Quoted params: ' . $quoted_username . '\m' . $quoted_password . '\n'; #
	# print 'Query string:' . $query . '\n';                                       #
	################################################################################
	
	my $sth = $dbh->prepare($query);
	$sth->execute();
	my $ver = $sth->fetch();
	if ($ver){
	    print $cgi->header,
		  $cgi->start_html("WIN!"),
		  $cgi->h1("$ver"),
		  $cgi->h2("You succeeded with query " . $query),
		  $cgi->h2("Suplied parameters U:" . $username . " P:" . $password),
		  $cgi->h2("Quoted parameters U:" . $quoted_username . " P:" . $quoted_password),
		  $cgi->end_html;
	} else{
	    print $cgi->header,
		  $cgi->start_html("FAIL!"),
		  $cgi->h2("You failed with query " . $query),
		  $cgi->h2("Suplied parameters U:" . $username . " P:" . $password),
		  $cgi->h2("Quoted parameters U:" . $quoted_username . " P:" . $quoted_password),
		  $cgi->end_html;
	}
	
	$sth->finish();
	$dbh->disconnect();
    }
}

my $pid = MyWebServer->new(8080)->background();
print "Use 'kill $pid' to stop server.\n";
