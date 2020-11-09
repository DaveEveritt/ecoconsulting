$(document).ready(function() {

    //Default action on load
    $(".tab_container > div").hide(); //Hide all content
    $("ul.tabs li:first").addClass("active").show(); //Highlight first tab
    $(".tab_container > div:first").show(); //Show first tab content

    //On click tab
    $("ul.tabs li a").click(function() {
        $("ul.tabs li a").removeClass("active"); //Remove any "active" class
        $(this).addClass("active"); //Add "active" class to selected tab
        $(".tab_container > div").hide(); //Hide all tab content
        var activeTab = $(this).attr("href"); //Find the active tab href
        $(activeTab).fadeIn(400); //Fade in the active content
       return false;
    });

});
