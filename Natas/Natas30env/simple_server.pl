{
    package MyWebServer;

    use HTTP::Server::Simple::CGI;
    our @ISA = qw(HTTP::Server::Simple::CGI);

    my %dispatch = (
	'/index.cgi' => \&resp_index,
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
		  $cgi->h2('You can got to localhost:8080/index.cgi?username=user&password=pass'),
		  $cgi->end_html;
	}
    }

    sub resp_index {
	my $cgi  = shift;
	return if !ref $cgi;
	
	my $dbh = DBI->connect( "DBI:mysql:natas30","natas30", "toor", {'RaiseError' => 1});
	my $query="Select * FROM users where username =".$dbh->quote(param('username')) . " and password =".$dbh->quote(param('password')); 
	my $sth = $dbh->prepare($query);
	$sth->execute();
	my $ver = $sth->fetch();
	if ($ver){
	    print $cgi->header,
		  $cgi->start_html("WIN!"),
		  $cgi->h1("$ver"),
		  $cgi->end_html;
	}
	else{
	    print $cgi->header,
		  $cgi->start_html("FAIL"),
		  $cgi->end_html;
	}
	$sth->finish();
	$dbh->disconnect();
	
	my $user = $cgi->param('username');
	my $pass = $cgi->param('password');
	
	print $cgi->header,
	      $cgi->start_html("Hello"),
	      $cgi->h1("Hello $user!"),
	      $cgi->hl("Your supplied Password = $pass"),
	      $cgi->end_html;
    }
}

# start the server on port 8080
my $pid = MyWebServer->new(8080)->background();
print "Use 'kill $pid' to stop server.\n";
