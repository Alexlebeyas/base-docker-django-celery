class Cookie {
    constructor() {
        this._cookies = {};
        for (let cookie of document.cookie.split(';')) {
            let [name, value] = cookie.split('=');
            this._cookies[name] = decodeURIComponent(value);
        }
    }

    getCookie (name) { return this._cookies[name] }
}

export default new Cookie()

function setContactFormListener() {
   $('section#contact form:first').submit(function(e){
       e.preventDefault();
       var _self = $(this);
       $.ajax({
           method: "POST",
           url: _self.attr('action'),
           data: _self.serialize(),
           success: function() {
               // handle success
               _self.hide();
               $('section#contact div.success-message:first').show();
           },
           error: function(data) {
               // handle errors
               var errors = JSON.parse(data.responseJSON);
               for (var key in errors) {
                   for (var i = 0; i < errors[key].length; i++) {
                       $('#error_' + key).html(errors[key][i]["message"]);
                   }
               }
           }
       })
   })
}