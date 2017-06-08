// TOOLS
import cookie from './tools/cookie.es6';
// FUNCTIONALITY
import ui from './ui.es6';

$(document).ready(function(){
    /**
     * Ajax setup
     */
    let csrf = cookie.getCookie('crsftoken');
    $.ajaxSetup({ headers : {'X-CSRFToken': csrf }});

    /**
     * UI utils
     * class to put JS front-end code
     */
    ui.init();
});