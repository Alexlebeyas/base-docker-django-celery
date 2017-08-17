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
        } else if (!form.attr('method') || form.attr('method').toLowerCase() !== "post") {
            console.error('FormAjax constructor error', '=> You must set the method attribute to "POST"');
            return false;
        } else if (!onSuccess || typeof onSuccess !== 'function') {
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

        this._form.find('.form-group').each((k, v) => {
            let $formGroup = $(v);
            let $formGroupInput = $formGroup.find('input');
            if ($formGroupInput.attr('type') !== "hidden") {
                let name = $formGroupInput.attr('name');
                let errorElement = getErrorFormat(`${name}`);
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
        this._form.submit((e) => {
            e.preventDefault();
            this._hideErrors();
            $.ajax({
                method: this._form.attr('method'),
                url: this._form.attr('action'),
                data: this._form.serialize(),
                beforeSend: (jqXHR, settings) => {
                    if (this._beforeSend) {
                        this._beforeSend(jqXHR, settings, this);
                    }
                },
                success: (response) => {
                    this._onSuccess(response, this)
                },
                error: (response) => {
                    // handle errors
                    let errors = JSON.parse(response.responseJSON);
                    this._displayErrors(errors);
                    if (this._onError) {
                        this._onError(response, this)
                    }
                }
            })
        });
    }

    /**
     * Display errors from Django error response in the html element
     *  Note: usage when Django form prefix is used -- add data-prefix to the form with form.prefix value
     * @param {Object} errors - This object is from django forms: you must return form.errors.as_json()
     * @private
     */
    _displayErrors(errors) {
        let prefix = this._form.data('prefix');

        for (let [key, value] of Object.entries(errors)) {
            for (let i = 0; i < value.length; i++) {
                let errorObj = value[i];
                let errorId = (prefix) ? `#error_${prefix}-${key}` : `#error_${key}`;
                $(errorId).html(errorObj.message);
            }
        }
    }

    /**
     * Before the ajax call - hide form errors
     * @private
     */
    _hideErrors() {
        this._form.find('.ajax_error').each((k, v) => {
            $(v).html('');
        });
        this._form.find('.has_error').each((k, v) => {
            $(v).removeClass('has_error');
        });
    }

    /**
     * To clear field values
     */
    clearFields() {
        this._form.find('.form-group input').each((k, v) => {
            let $input = $(v);
            if ($input.attr('type') !== "hidden") {
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