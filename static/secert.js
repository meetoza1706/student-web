function login() {
    var username = $("#username").val();
    var password = $("#password").val();
    
    $.ajax({
        url: '/XOM',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({username: username, password: password}),
        success: function(response) {
            // Handle successful response
            alert("Login successful!");
        },
        error: function(error) {
            // Handle error response
            alert("Login failed!");
        }
    });
}