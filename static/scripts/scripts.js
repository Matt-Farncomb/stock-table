window.onload = () => {
    // will stop the refresh initiated by the HTML
    window.stop();

    console.log("fart");
    let dbUpdating = "false";
    // check to see if server is updating
    // if server was updating but now isn't, reload page
    setInterval(() => 
        fetch("http://127.0.0.1:5000/api")
        .then(response => response.json())
        .then(dbdatus => {
            console.log(dbdatus);
            console.log(dbdatus[0]);
            if (dbdatus[0] === "true") {
                dbUpdating = true;
                console.log("db has started updating");
            } else if (dbdatus[0] === "false" && dbUpdating === true) {
                location.reload();
                console.log("db updated");
                dbUpdating = false;
            } else {
                console.log("db is not updating");
            }
        }), 
        10000 
    );

    
}