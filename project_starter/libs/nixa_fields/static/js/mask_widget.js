/**
 * Created by philippe on 12/9/16.
 */
"use strict";

$(function () {
    var $nixaFieldPhone = $('.nixa-fields-mask');
    var vendor_url = $nixaFieldPhone.first().data('vendor-url');

    if ($.mask !== "function") {
        // When the script is loaded,
        //  We add the mask and listener
        $.getScript(vendor_url, function () {
            $nixaFieldPhone.each(function (key, value) {
                var $input = $(value);
                // Apply the mask if exist
                var mask = $input.data('mask-value');
                if (mask) {
                    $input.mask(mask, mask_options);
                }
                // Precaution
                $input.unbind('change');
                // Send the value to the hidden field
                $input.change(function () {
                    var $related = $("#" + $input.data('related-input'));

                    var phone_value = $input.val();
                    if (mask) {
                        phone_value = $input.unmask().val();
                        $input.mask(mask, mask_options);
                    }

                    $related.val(phone_value);
                })
            });
        });
    }
});

var mask_options = {
    'translation': {
        'Z': {
            pattern: /[A-Za-z]/,
            optional: false
        }
    }
};