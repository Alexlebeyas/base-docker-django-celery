/**
 * Class to handle ajax form
 * # todo remove jQuery usage
 */
export class FormAjax {
    /**
     * Class to create ajax call with a django form - Handle only post method for now
     * @param {jquery Object} form - requirements: data-action (url to send ajax call)
     * @param {function} onSuccess - function params: {Anything} response, {Object} instance - current instance
     * @param {function} onError - default = null - function params: {jqXHR} response, {Object} instance - current instance
     * @param {function} beforeSend - default = null - function params: {jqXHR} jqXHR, {Object} settings, {Object} instance - current instance
    */
    constructor(form, onSuccess, onError=null, beforeSend=null) {
        if (this._validForm(form, onSuccess)) {
            this._form = form;
            this._onSuccess = onSuccess;
            this._onError = onError;
            this._beforeSend = beforeSend;
            this._appendErrors(FormAjax.getErrorSpan);
            this._addSubmitCall();
        }
        return this;
    }

    /**
     * Validate the FormAjax creation -- display errors in console.log
     * @param {jquery Object} form
     * @param {function} onSuccess
     * @returns {boolean}
     * @private
     */
    _validForm(form, onSuccess) {
        if (!form.attr('action')) {
            console.error('FormAjax constructor error', '=> You must add this action attribute');
            return false;
        } else if (!form.attr('method') || form.attr('method').toLowerCase() != "post") {
            console.error('FormAjax constructor error', '=> You must set the method attribute to "POST"');
            return false;
        } else if (!onSuccess || typeof onSuccess != 'function') {
            console.error('FormAjax constructor error', '=> You must implement an onSuccess callback');
            return false;
        }
        return true;
    }

    /**
     * Append html element to display errors in the form
     * @param {function} getErrorFormat - Function that return html element to display input errors
     * @private
     */
    _appendErrors(getErrorFormat) {
        this._form.find('.form-group').each(function () {
            let $formGroup = $(this);
            let $formGroupInput = $formGroup.find('input');
            if ($formGroupInput.attr('type') != "hidden") {
                let errorElement = getErrorFormat($formGroupInput.attr('name'));
                $formGroup.append(errorElement);
            }
        });

        // For general messages
        if (!this._form.find('#error___all__').attr('class')) {
            this._form.prepend(getErrorFormat('__all__'));
        }
    }

    /**
     * Add call on submit to the form
     * @private
     */
    _addSubmitCall() {
        let class_ = this;
        this._form.submit( function (e) {
            e.preventDefault();
            class_._hideErrors();
            $.ajax({
                method: class_._form.attr('method'),
                url: class_._form.attr('action'),
                data: class_._form.serialize(),
                beforeSend: function (jqXHR, settings) {
                    if (class_._beforeSend) {
                        class_._beforeSend(jqXHR, settings, class_);
                    }
                },
                success: function(response) {
                    class_._onSuccess(response, class_)
                },
                error: function(response) {
                    // handle errors
                    let errors = JSON.parse(response.responseJSON);
                    class_._displayErrors(errors);
                    if (class_._onError) {
                        class_._onError(response, class_)
                    }
                }
            })
        });
    }

    /**
     * Display errors from Django error response in the html element
     * @param {Object} errors - This object is from django forms: you must return form.errors.as_json()
     * @private
     */
    _displayErrors(errors) {
        for (let [key, value] of Object.entries(errors)) {
            for (let i = 0; i < value.length; i++) {
                let errorObj = value[i];
                $('#error_' + key).html(errorObj.message);
            }
        }
    }

    /**
     * Before the ajax call - hide form errors
     * @private
     */
    _hideErrors() {
        this._form.find('.ajax_error').each(function (k, v) {
            $(this).html('');
        });
        this._form.find('.has_error').each(function (k, v) {
            $(this).removeClass('has_error');
        });
    }

    /**
     * To clear field values
     */
    clearFields() {
        this._form.find('.form-group input').each(function () {
            let $input = $(this);
            if ($input.attr('type') != "hidden") {
                $input.val('');
            }
        });
    }

    /**
     * Return a html element to display inputs errors
     * @param fieldName
     * @returns {string}
     */
    static getErrorSpan(fieldName) {
         return `<span class="ajax_error" id="error_${fieldName}"></span>`;
    }
}