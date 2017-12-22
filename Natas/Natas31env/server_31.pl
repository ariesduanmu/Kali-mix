use strict;
use warnings;

use feature 'say';

{
    package MyWebServer;

    use DBI;
    use HTTP::Server::Simple::CGI;
    our @ISA = qw(HTTP::Server::Simple::CGI);

    $ENV{'TMPDIR'}="WWWDIR/tmp/";

    my %dispatch = (
        '/index.pl' => \&resp_index,
    );

    sub handle_request {
        my $self = shift;
        my $cgi = shift;

        my $path = $cgi->path_info();
        my $handler = $dispatch{$path};

        if (ref($handler) eq "CODE") {
            print "HTTP/1.0 200 OK\r\n";
            $handler->($cgi);
        } else {
            print "HTTP/1.0 404 Not found\r\n";
            print $cgi->header,
                  $cgi->start_html('Natas31'),
                  $cgi->h1('natas31'),
                  $cgi->start_multipart_form(
                    -action=>'index.pl',
                    -method=>'POST',
                    ),
                  $cgi->h2('CSV2HTML'),
                  $cgi->p('We all like .csv files.'),
                  $cgi->p("But isn't a nicely rendered and sortable table much cooler?"),
                  $cgi->p('Select file to upload:'),
                  $cgi->filefield(
                    -name=>'upload_file',
                    -size=>50,
                    -maxlength=>80,
                    ),
                  $cgi->submit(
                    -name=>'submit',
                    ),
                  $cgi->end_form,
                  $cgi->end_html;
        }

    }

    sub resp_index {
        my $cgi = shift;
        return if !ref $cgi;

        print $cgi->header,
              $cgi->start_html('Natas31'),
              $cgi->h2('Received:');

        my $file = $cgi->param('upload_file');
        say '<table class="sortable table table-hover table-striped">';
        my $i=0;

        open my $fh, "<", $file or die "could not open $file: $!";
        while (<$fh>) {
            my @elements=split /,/, $_;

            if($i==0){ # header
                say "<tr>";
                foreach(@elements){
                    say "<th>".$_."</th>";   
                }
                say "</tr>";
            }
            else{ # table content
                say "<tr>";
                foreach(@elements){
                    say "<td>".$_."</td>";   
                }
                say "</tr>";
            }
            $i+=1;
        }
        say '</table>';
        

    }
}

my $pid = MyWebServer->new(8080)->background();
print "Use 'kill $pid' to stop server.\n";

