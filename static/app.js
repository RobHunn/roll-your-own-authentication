// document.getElementById('reg_form').addEventListener('submit', onClick)
// function onClick(e) {
//     e.preventDefault();
//     let csrf_token = document.querySelector('#csrf_token').value
//     fetch('/api/reg_user', {
//         method: 'POST',
//         headers: {
//             'Accept': 'application/json',
//             'Content-Type': 'application/json',
//             "X-CSRFToken": csrf_token
//         },
//         body: JSON.stringify({
//             csrf_token,
//             first_name: document.querySelector('#first_name').value,
//             last_name: document.querySelector('#last_name').value,
//             username: document.querySelector('#username').value,
//             email: document.querySelector('#email').value,
//             password: document.querySelector('#password').value
//         })
//     })
// }