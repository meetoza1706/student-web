document.getElementById('unitTestBtn').style.display = 'none'
function login() {
    var username = $("#username").val();
    var password = $("#password").val();
    
    $.ajax({
        url: '/XOM',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({username: username, password: password}),
        success: function(response) {
            console.log('b')
            document.getElementById('control').style.display = 'none';
            document.getElementById('unitTestBtn').style.display = 'block';
        },
        error: function(error) {
            console.log('a')
        }
    });
}
function toggleUnitTest() {
    fetch('/toggle')  // Sends a request to Flask route '/toggle'
        .then(response => {
            if (response.ok) {
                return response.text();
            }
            throw new Error('Network response was not ok.');
        })
        .then(result => {
            console.log(result);  // Optional: Log success message
            document.getElementById('toggleButton').disabled = true;  // Disable the toggle button after toggling
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function disableToggle() {
    fetch('/disable-toggle')  // Sends a request to Flask route '/disable-toggle'
        .then(response => {
            if (response.ok) {
                return response.text();
            }
            throw new Error('Network response was not ok.');
        })
        .then(result => {
            console.log(result);  // Optional: Log success message
            document.getElementById('toggleButton').disabled = true;  // Disable the toggle button
        })
        .catch(error => {
            console.error('Error:', error);
        });
}
