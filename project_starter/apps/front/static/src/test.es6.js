import {FormAjax} from "./tools/form.ajax.es6"

class Test {
    init() {
        new FormAjax($('#post-test'), this.postSuccess, this.postError);
    }

    postSuccess(response, formAjax) {
        formAjax.clearFields();
        alert(response.message);
    }
    postError(response, formAjax) {
        let message = "CSRF-TOKEN error";
        if (response.responseJSON && response.responseJSON.message) {
            message = response.responseJSON.message;
        }
        console.error(`${response.statusText} : ${message}`);
    }
}

export default new Test();