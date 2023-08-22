function do_basket_search() {
    var key = document.getElementById("search-field-typebox").value;

    var loaderUI = document.getElementById("loader-wheel");
    var searchButton = document.getElementById("search-button-clicker");
    var noneFound = document.getElementById("noneFoundContainer");

    loaderUI.style.display = "block";
    searchButton.style.display = "none";
    noneFound.style.display = "none";

    var url = `/operate_basket?id=iahfiasfdosai2313212**7613&key=${encodeURIComponent(key)}`;

    fetch(url, {
        method: "GET"
      })
      .then((response) => response.json())
      .then((json) => {
        loaderUI.style.display = "none";
        searchButton.style.display = "block";

        if (json == false) {
            noneFound.style.display = "flex";
            return;
        };

        console.log(json);
      });

    
};