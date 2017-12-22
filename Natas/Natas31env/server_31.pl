use strict;
use warnings;

use feature 'say';

{
    package Natas31Clone;

    use DBI;
    use HTTP::Server::Simple::CGI;
    our @ISA = qw(HTTP::Server::Simple::CGI);

    $ENV{'TMPDIR'}="WWWDIR/tmp/";

    my %dispatch = (
        '/upload.pl' => \&resp_upload,
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
                    -action=>'upload.pl',
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

    sub resp_upload {
        my $cgi = shift;
        return if !ref $cgi;

        print $cgi->header;
        print $cgi->start_html('Natas31');

        if ($cgi->upload('upload_file')) {
            my $file = $cgi->param('upload_file');
            print $cgi->h2('Recieved ' . $file);
            
            # Not a nice table as on Natas31 though
            print '<table class="sortable table table-hover table-striped">';
            my $i=0;
            while (<$file>) {
                my @elements=split /,/, $_;

                if($i==0){ # header
                    print "<tr>";
                    foreach(@elements){
                        print "<th>".$cgi->escapeHTML($_)."</th>";   
                    }
                    print "</tr>";
                }
                else{ # table content
                    print "<tr>";
                    foreach(@elements){
                        print "<td>".$cgi->escapeHTML($_)."</td>";   
                    }
                    print "</tr>";
                }
                $i+=1;
            }
            print '</table>';
        }
        print $cgi->end_html;
    }
}

my $pid = Natas31Clone->new(8080)->background();
print "Use 'kill $pid' to stop server.\n";
