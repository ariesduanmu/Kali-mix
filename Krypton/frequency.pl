#!/usr/bin/perl

use strict;
use warnings;
use feature 'say';


use File::Slurp;


my @filenames = ("found1", "found2", "found3");
my @LETTERS = ("A" .. "Z");
my %ENGLISH_FREQ = (
    "E" => 12.702,
    "T" => 9.056,
    "A" => 8.167,
    "O" => 7.507,
    "I" => 6.966,
    "N" => 6.749,
    "S" => 6.327,
    "H" => 6.094,
    "R" => 5.987,
    "D" => 4.253,
    "L" => 4.025,
    "C" => 2.782,
    "U" => 2.758,
    "M" => 2.406,
    "W" => 2.360,
    "F" => 2.228,
    "G" => 2.015,
    "Y" => 1.974,
    "P" => 1.929,
    "B" => 1.492,
    "V" => 0.978,
    "K" => 0.772,
    "J" => 0.153,
    "X" => 0.150,
    "Q" => 0.095,
    "Z" => 0.074
);


sub count_frequency {
    my ($string) = @_;
    my %occurences = count_occurence($string);
    return map { $_ => $occurences{$_} / length($string) } keys %occurences;
}

sub count_occurence {
    my ($string) = @_;
    my %frequency = map { $_ => 0 } @LETTERS;
    foreach (split //, $string) {
        $frequency{$_}++;
    }
    return %frequency;
}

sub decrypt {
    my (%frequency) = @_;
    foreach my $name ( sort { $frequency{$b} <=> $frequency{$a} } keys %frequency ) {
        say "$name , $frequency{$name}";
    }

    # zip over the hashes?
}

foreach (@filenames) {
    my $text = read_file($_);
    $text =~ s/\s+//g;
    my %file_frequency = count_frequency($text);
    decrypt (%file_frequency);
    say "-" x 20;
}


