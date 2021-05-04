// TOOLS
import cookie from './tools/cookie.es6';
// FUNCTIONALITY
import ui from './ui.es6';

$(document).ready(function(){
    /**
     * Ajax setup
     */
    let csrf = cookie.getCookie('csrftoken');
    $.ajaxSetup({ headers : {'X-CSRFToken': csrf }});

    /**
     * UI utils
     * class to put JS front-end code
     */
    ui.ready();
});

$(window).on('load', () => {
    ui.loaded();
});