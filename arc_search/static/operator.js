function do_search() {
    var searchEAN = document.getElementById("search-field-typebox").value;
    console.log(searchEAN);

    var returnDumper = document.getElementById("return-dump");
    returnDumper.textContent = "-----LOADING-----";

    var url = `/search_all?id=iahfiasfdosai2313212**7613&ean=${encodeURIComponent(searchEAN)}&product_name=?`

    fetch(url, {
        method: "GET"
    })
    .then((response) => response.json())
    .then((json) => {
        console.log(json);
        returnDumper.textContent = JSON.stringify(json);
    });
}