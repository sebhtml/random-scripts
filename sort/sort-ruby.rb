#!/usr/bin/env ruby

size = 10000
strings = []

size.times do
    length = rand(1000)
    my_string = "!" * length

    strings.push my_string
end

sorted_strings = strings.sort do |a, b| a.length <=> b.length end
