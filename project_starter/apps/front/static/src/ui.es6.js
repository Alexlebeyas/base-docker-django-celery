class UI {
    /**
     * Put your code for jquery $(document).ready() function
     */
    ready() {
        console.log('page', 'ready');
        let $body = $("body");
        let $page404 = $('#page-404');
        let $navBarToggle = $(".navbar-toggle" );

        //hide footer on 404
        if ($page404.length) {
            //make the 404 page take 100% of the page height in each devices*
            $page404.css('height', window.innerHeight);
            $( "footer" ).hide();
        }

        //Disable scroll when navbar-toggle is open
        //to do: change the object for the good ones! navbar-toggle is the btn to open the menu - nav-primary-group is the menu. body stays the same
         $navBarToggle.click(function () {
             let $navPrimaryGroup = $(".nav-primary-group");
             if($navBarToggle.hasClass( "collapsed" )) {
                $body.css("overflow-y", "hidden");
                $body.css("height", $( window ).height());
                $navPrimaryGroup.css("height", $( window ).height());
             }
             else {
                $body.css("overflow-y", "auto");
                $body.css("height", "auto");
                $navPrimaryGroup.css("height", "auto");
             }
         });

        //modal open fix - add class modal open to make sure that the ipad don't lose focus
        $(document).on('hidden.bs.modal', function (event) {
          if ($('.modal:visible').length) {
            $body.addClass('modal-open');
          }
        });
    }

    /**
     * Put your code for jquery $(window).load() function
     */
    loaded() {
        console.log('page', 'loaded');

    }
}

export default new UI();