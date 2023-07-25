function do_search() {
    var searchEAN = document.getElementById("search-field-typebox").value;
    console.log(searchEAN);

    var returnDumper = document.getElementById("return-dump");
    returnDumper.textContent = "-----LOADING-----";

    var loaderUI = document.getElementById("loader-wheel")
    var searchButton = document.getElementById("search-button-clicker")

    loaderUI.style.display = "block";
    searchButton.style.display = "none";

    var url = `/search_all?id=iahfiasfdosai2313212**7613&ean=${encodeURIComponent(searchEAN)}&product_name=?`

    fetch(url, {
        method: "GET"
    })
    .then((response) => response.json())
    .then((json) => {
        console.log(json);
        returnDumper.textContent = JSON.stringify(json);

        loaderUI.style.display = "none";
        searchButton.style.display = "block";
    });
}