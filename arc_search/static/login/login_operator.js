function verify_otp() {
  const code = document.getElementById("search-field-typebox").value;

  if (code != '' && selectedUser != '') {
    const userID = userIconMap[selectedUser];
    console.log("LOGGING IN");

    var url = `/login/verify_otp?user_id=${encodeURIComponent(userID)}&otp=${encodeURIComponent(code)}`;

    fetch(url, {
        method: "GET"
      })
      .then((response) => response.json())
      .then((json) => {
        console.log(json);

        if (json == false) {
            console.log("Login Failed 22!");
            var message = document.getElementById("auth_fail_message");
            message.style.visibility = "visible";
        } else {
            const new_inner = '<iframe src="/static/mainpage.html" frameborder="0" width="100%" height="100%"></iframe>';
            document.body.innerHTML = new_inner;
        };

      });
  } else {
    console.log("EMPTY FIELDS");
  };
};

var userIconMap = {};
var selectedUser = '';

function CreateUserIcons() {
  var url = '/login/get_users';
  fetch(url).then(res=> res.json()).then(data => {

    var holder = document.getElementById("user-icon-holder");

    for (const obj of data) {
      userIconMap[obj[1]] = obj[0];

      var img = document.createElement("img");
      img.src = `/static/login/user_icons/${obj[1]}_off.png`;
      img.setAttribute('data-name', obj[1])
      img.style.cssText = 'width: 60px;  height: 60px; margin: 40px;';

      img.onclick = function() {
        ClickUserIcon(this);
      };

      holder.appendChild(img);
    };

  });
};

function ClickUserIcon(img) {
  var imageContainer = document.getElementById("user-icon-holder");
  var images = imageContainer.querySelectorAll("img");
  images.forEach(function(target) {
    const target_name = target.getAttribute("data-name");
      target.src = `/static/login/user_icons/${target_name}_off.png`;
  });

  const name = img.getAttribute("data-name");
  img.src = `/static/login/user_icons/${name}_on.png`;
  selectedUser = name;
}