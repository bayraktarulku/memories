function login(response) {
    let data = JSON.parse(response);
    if (data.status === 'OK') {
        sessionStorage.setItem('token', data.token);
        window.location = '/memories';
    } else {
        alert('Wrong password or email');
    }
}

app = new Vue({
    'el': '#login-app',
    'data': {
        'email': 'sexyboy_111@email.com',
        'password': 'veryhardpassword123',
    },
    'methods': {
        'login_submit': function () {
            data = JSON.stringify({'email': this.email, 'password': this.password});
            this.email = '';
            this.password = '';
            request('POST', '/api/auth',
                    {'Content-Type': 'application/json'},
                    data,
                    login);
        }
    }
})
