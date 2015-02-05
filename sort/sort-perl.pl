#!/usr/bin/env perl

@strings = ();

$size = 10000;

$i = 0;

@array = map { "a" x rand(10000) } 1..1000;

@array = sort { length($a) <=> length($b) } @array;


