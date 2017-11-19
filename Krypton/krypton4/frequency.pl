#!/usr/bin/perl

use strict;
use warnings;

use Path::Tiny 'path';


my @FILENAMES = ("found1", "found2", "found3");
my @LETTERS = ("A" .. "Z");
my @ENGLISH_FREQ = ("E", "T", "A", "O", "I", "N", "S", 
                    "H", "R", "D", "L", "C", "U", "M", 
                    "W", "F", "G", "Y", "P", "B", "V", 
                    "K", "J", "X", "Q", "Z");

sub count_occurence {
    my ($string) = @_;
    my %frequency = map { $_ => 0 } @LETTERS;

    foreach my $letter (split //, $string) {
        $frequency{$letter}++;
    }

    return %frequency;
}

sub get_key_hash {
    my (%frequency) = @_;
    my @letters = sort { $frequency{$b} <=> $frequency{$a} } keys %frequency;

    return map { $letters[$_] => $ENGLISH_FREQ[$_] } 0 .. $#letters;
}

sub count_frequency_files {
    my %total_frequency = map { $_ => 0 } @LETTERS;

    foreach my $filename (@FILENAMES) {
        my $text = path($filename)->slurp =~ s/\s+//gr;
        my %frequency = count_occurence($text);

        $total_frequency{$_} += $frequency{$_} for keys %frequency; 
    }

    return %total_frequency;
}

my %cypher_key = get_key_hash(count_frequency_files());
print $cypher_key{$_} for split //, path("krypton4")->slurp =~ s/\s+//gr;
print "\n";

