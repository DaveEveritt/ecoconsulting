#!/usr/bin/perl -w

use strict;
use CGI;
use Mail::Send;

#########################################
# User Params / Templates
#########################################
# name
# email
# message

my $to = "deveritt\@innotts.co.uk";
my $subject = "From Eco Consulting";
my $mailtext = << "ENDMAIL";
Reply to: <var name>, <var email>\n
<var message>\n\n
Sum = <var sum>
ENDMAIL

#########################################
# End of user params
#########################################

my @spamwords = (qw(spybot megagames webcam webcams cheapticket vogue.com valium cigarettes airlines viagra porn httpgoogle httpmsn adultgroups gaymovies googlesearchworld googleus yahoous onlinegambling nakedwoman yahooadult atacand ashwagandha arimidex aricept antabuse amaryl allaceon cheapticketscom),'nice site look this','first page of Google','GOOGLE RANKING','increase traffic to your website');

my $q = new CGI;

if ($q->param('email') && $q->param('message')) {
	foreach($q->param) {$q->param_fetch($_)->[0] =~ s/[^A-Za-z0-9\@\'\n\.\,\-\!~ ]//g;}
	$q->param("name","") unless $q->param("name");
	my $isspam = 0;
	my $msgcheck = lc($q->param("message"));
	foreach (@spamwords) {
		if (index($msgcheck,$_) > -1) {
			$isspam = 1;
			last;
		}
	}
	my @nofill = qw(about comment);
	foreach (@nofill) {
    	if ($q->param($_) != "") {
        	$isspam = 1;
    	}
	}	
	if ($isspam || $q->param("sum") != "5" || $q->param("link") != "http://") {
		print $q->redirect("/contact/index.shtml");
# 		print $q->redirect("/contact/contact-spam.shtml");
	}
	else {
		my $msg = new Mail::Send(Subject=>$subject, To=>$to);
		$mailtext =~ s/<var (.*?)>/$q->param($1)/ge;
		my $fh = $msg->open; print $fh $mailtext; $fh->close;
		print $q->redirect("/contact/contact-thanks.shtml");
	}
}
else {
	print $q->redirect("/contact/contact-blank.shtml");
}

exit;
