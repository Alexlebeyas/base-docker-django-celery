$(document).ready(function(){
    resizeMain();
    checkError();
});

//make the 404 page take 100% of the page height in each devices*
function resizeMain() {
    $('#page-404').css('height', window.innerHeight);
}

//hide footer on 404
function checkError() {
    if ($("#page-404").length) {
        $( "footer" ).hide();
    }
}