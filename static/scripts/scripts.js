window.onload = () => {
    // will stop the refresh initiated by the HTML
    window.stop();

    const refreshNotification = document.querySelector("#refresh-notification");
    const p = refreshNotification.querySelector("p");
    const span = p.querySelector("span");

    let displayedMinutes = refresh_interval.minutes;

    p.classList.remove("hidden");
    refreshNotification.classList.remove("noscript");
    refreshNotification.classList.add("refresh-notification")
    
    // span.innerHTML = nearestMinute()

    console.log("fart");
    let dbUpdating = "false";

    console.log(refresh_interval);
    const last_updated = Date.parse(refresh_interval.last_updated);
    console.log(last_updated)
    // check to see if server is updating
    // if server was updating but now isn't, reload page

    // setTimeout(location.reload(), refresh_interval.seconds * 1000);
    // setTimeout(() => location.reload(), refresh_interval.seconds * 1000);
    setInterval(() => {      
        console.log("working");
        if (displayedMinutes == 1) {
            p.innerText = "Page will soon refresh with new inventory";
        } else {
            displayedMinutes -= 1;
            span.innerHTML = displayedMinutes;
            }
        }, 60000    
    )

    setTimeout(() => 
        setInterval(() => 
                fetch("http://127.0.0.1:8000/api")
                .then(response => response.json())
                .then(dbdatus => {
                    console.log(dbdatus)
                    const db_update = Date.parse(dbdatus[0]);
                    if (db_update > last_updated) { 
                        // console.log("reload");
                        location.reload();
                    }
                }), 
        10000 ), 
    refresh_interval.seconds * 1000)
                       




    // setInterval(() => 
    //     fetch("http://127.0.0.1:8000/api")
    //     .then(response => response.json())
    //     .then(dbdatus => {
    //         console.log(dbdatus);
    //         console.log(secondsTillUpdate(dbdatus[1]));
    //         span.innerHTML = nearestMinute(secondsTillUpdate(dbdatus[1]))
    //         if (dbdatus[0] === "true") {
    //             dbUpdating = true;
    //             console.log("db has started updating");
    //         } else if (dbdatus[0] === "false" && dbUpdating === true) {
    //             location.reload();
    //             console.log("db updated");
    //             dbUpdating = false;
    //         } else {
    //             console.log("db is not updating");
    //         }
    //     }), 
    //     10000 
    // );
    console.log("test")
    console.log(refresh_interval)

}

// function updateDue(secondsRemaining) {
//     const timeNow = millisecondsToSeconds(Date.now());
//     const updateDueAt = timeNow + secondsRemaining;
//     return updateDueAt;
// }

// function secondsTillUpdate(date) {
//     const UPDATE_INTERVAL = 300; // seconds
//     const dateInSeconds = millisecondsToSeconds(Date.parse(date));
//     const nextUpdateDue = dateInSeconds + UPDATE_INTERVAL;
//     const timeNow = millisecondsToSeconds(Date.now());

//     return nextUpdateDue - timeNow;
// }

function millisecondsToSeconds(mil) {
    return Math.floor(mil / 1000);
}

// function nearestMinute(seconds) {
//     return Math.ceil(seconds / 60);
// }




// on page open, call to the server once
// server caclulates how long until next update and sends that number to clinet
// client can then count until it reaches that time
// also update html frequesntly as it counts
// refresh wehn counter is zero

// when the page is loaded without html, it will say "refresh every 5 minutes"
// but the logic in the refresh would come from the server calcualtion
// so on page load, it will calculate "how long until i need to refresh" and but theat number in the html template

