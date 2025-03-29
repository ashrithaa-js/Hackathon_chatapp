async function register() {
    let response = await fetch('/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            username: document.getElementById('username').value,
            password: document.getElementById('password').value
        })
    });
    alert(await response.text());
}

async function login() {
    let response = await fetch('/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            username: document.getElementById('username').value,
            password: document.getElementById('password').value
        })
    });
    let data = await response.json();
    if (data.token) {
        localStorage.setItem('token', data.token);
        alert('Logged in!');
    } else {
        alert('Invalid credentials');
    }
}

async function sendMessage() {
    let response = await fetch('/chat/send', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('token')
        },
        body: JSON.stringify({
            receiver: document.getElementById('receiver').value,
            message: document.getElementById('message').value
        })
    });
    alert(await response.text());
}

async function getMessages() {
    let response = await fetch('/chat/messages', {
        method: 'GET',
        headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') }
    });
    let messages = await response.json();
    document.getElementById('chat').innerText = JSON.stringify(messages, null, 2);
}
