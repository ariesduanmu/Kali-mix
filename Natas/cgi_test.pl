use strict;
use warnings;

use CGI 'param';
use feature 'say';

# A stripped down version to test what the csv will be able to read
# However to make test better we can make this WebServer again (and call another file)
# Usage -->
# ---
# perl cgi_test.pl file="filename"
# ---


my $file = param('file');
say '<table class="sortable table table-hover table-striped">';
my $i = 0;

open my $fh, "<", $file or die "could not open $file: $!";
while (<$fh>) {
    my @elements=split /,/, $_;
    if($i==0) {
        say "<tr>";
        foreach(@elements){
	    say "<th>".$_."</th>";   
        }
        say "</tr>";
    } else {
        say "<tr>";
        foreach(@elements){
	    say "<td>".$_."</td>";   
        }
        say "</tr>";
    }
    $i+=1;
}
say '</table>';
