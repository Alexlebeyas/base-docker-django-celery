class UI {
    /**
     * Put your code for jquery $(document).ready() function
     */
    ready() {
        let $body = $("body");

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

    }
}

export default new UI();