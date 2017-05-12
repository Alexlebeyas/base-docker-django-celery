// TOOLS
import cookie from './tools/cookie.es6';
// FUNCTIONALITY
import ui from './ui.es6';
import test from './test.es6';
import {map} from 'map.es6';

$(document).ready(function(){
    /**
     * Ajax setup
     */
    let csrf = cookie.getCookie('crsftoken');
    $.ajaxSetup({ headers : {'X-CSRFToken': csrf }});

    /**
     * UI utils
     */
    ui.init();
    test.init();
    map.init();
});