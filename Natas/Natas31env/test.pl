use strict;
use warnings;

@ARGV=( 'echo exploited|' );



my $filehandle = "ARGV";

while (<$filehandle>) {
  print $_;
}
