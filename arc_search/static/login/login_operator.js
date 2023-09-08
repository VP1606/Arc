function verify_otp() {

    const username = "demo";
    const code = document.getElementById("search-field-typebox").value;

    console.log("LOGGING IN");

    var url = `/login/verify_otp?username=${encodeURIComponent(username)}&otp=${encodeURIComponent(code)}`;

    fetch(url, {
        method: "GET"
      })
      .then((response) => response.json())
      .then((json) => {
        console.log(json);

        if (json == false) {
            console.log("Login Failed!");
        } else {
            const new_inner = '<iframe src="/static/mainpage.html" frameborder="0" width="100%" height="100%"></iframe>';
            document.body.innerHTML = new_inner;
        };

      });
};