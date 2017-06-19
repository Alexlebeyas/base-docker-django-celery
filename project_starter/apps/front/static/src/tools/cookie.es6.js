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
