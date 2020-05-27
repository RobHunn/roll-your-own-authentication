document.getElementById('reg_form').addEventListener('submit', onClick)
function onClick(e) {
    e.preventDefault();
    fetch('/api/reg_user', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            first_name: document.querySelector('#first_name').value,
            last_name: document.querySelector('#last_name').value,
            email: document.querySelector('#email').value,
            password: document.querySelector('#password').value
        })
    })
}