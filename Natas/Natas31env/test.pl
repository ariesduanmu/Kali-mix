use strict;
use warnings;

# Pretend this came in through a CGI Request Paramete
@ARGV=( 'echo exploited|' );

# This function should return a filehandle, but the user did something
# to trick magical_function to return the string "ARGV"


my $filehandle = "ARGV";

# TRAP
while (<$filehandle>) {
  print $_;
}