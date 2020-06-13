#!/usr/bin/perl -w

use strict;
# use CGI::Carp qw(fatalsToBrowser);
# use CGI qw(:standard);

my $xml = `wget -O - duall.iesd.dmu.ac.uk/1010buildings/DuallWebService.asmx/gGetBuildingMeters`;
print $xml;
# print "hello";

# while($xml =~/<Meter_ID>(\d+)/g) {print "$1\n"}
# while($xml =~/<Meter_Name>([ \w]+)/g) {print "$1\n"}
# [.]*[\s]+

# while($xml =~/<Meter_Name>([ \w]+)[\s\S]+<Lat>([\.\d]+)/g) {print "$1 $2\n"}

# while($xml) {push @results $_ ``}
