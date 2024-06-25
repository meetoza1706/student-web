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
        },
        error: function(error) {
            console.log('a')
        }
    });
}