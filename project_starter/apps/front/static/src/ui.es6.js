class UI {
    init() {
        //make the 404 page take 100% of the page height in each devices*
        $('#page-404').css('height', window.innerHeight);

        //hide footer on 404
        if ($("#page-404").length) {
            $( "footer" ).hide();
        }

        //Disable scroll when navbar-toggle is open
        //to do: change the object for the good ones! navbar-toggle is the btn to open the menu - nav-primary-group is the menu. body stays the same
         $(".navbar-toggle" ).click(function () {
             if($( ".navbar-toggle").hasClass( "collapsed" )) {
                $("body").css("overflow-y", "hidden");
                $("body").css("height", $( window ).height());
                $(".nav-primary-group").css("height", $( window ).height());
             }
             else {
                $("body").css("overflow-y", "auto");
                $("body").css("height", "auto");
                $(".nav-primary-group").css("height", "auto");
             }
         });

        //modal open fix - add class modal open to make sure that the ipad don't lose focus
        $(document).on('hidden.bs.modal', function (event) {
          if ($('.modal:visible').length) {
            $('body').addClass('modal-open');
          }
        });

        console.log('test', gettext("This is to be translated"));
        console.log('test', gettext("This is to be translated too"));
    }
}

export default new UI();