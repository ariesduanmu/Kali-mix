

{
    package MyWebServer;

    use DBI;
    use HTTP::Server::Simple::CGI;
    our @ISA = qw(HTTP::Server::Simple::CGI);

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

        $fh = $cgi->upload('upload_file');
        $filename = $cgi->param('upload_file');

        print $cgi->header,
              $cgi->start_html('Natas31'),
              $cgi->h2('Received:'),
              $cgi->h2($filename),
              $cgi->end_html;

        open (FILE1, "$fh"); 
        open (FILE2, ">copy.txt"); 

        while ( read(FILE1,$file_contents,1024) ) { 
          print FILE2 $file_contents; 
        }

        close (FILE1);
        close (FILE2);

        # if (defined $fh) {
        #     my $io_handle = $fh->handle;
        #     open (OUTFILE,'>/Users/liqin/Desktop/abc.txt');
        #     while ($io_handle->read($buffer,1024)){
        #         print OUTFILE $buffer;
        #     }
        # }

    }
}

my $pid = MyWebServer->new(8080)->background();
print "Use 'kill $pid' to stop server.\n";

