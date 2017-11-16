use LWP;

my $browser = LWP::UserAgent->new;

my $response =  $browser->post( 'http://natas29:airooCaiseiyee8he8xongien9euhe8b@natas29.natas.labs.overthewire.org/')->as_string;

print $response;