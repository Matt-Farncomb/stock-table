window.onload = () => {
    // will stop the refresh initiated by the HTML
    window.stop();

    // Update counter at top of page to inform
    // user when update is complete and
    // the page will refresh.
    startCountdown();

    // When the DB is due to start updating,
    // poll the server every 10 seconds to see
    // if update is complete then refresh
    // when update is complete.
    initiatePageRefresh();
                    
}

function initiatePageRefresh() {

    const last_updated = Date.parse(refresh_interval.last_updated);
    const interval = 10000 // 10 seconds

    setTimeout(() => 
        setInterval(() => 
                fetch("http://127.0.0.1:8000/api")
                .then(response => response.json())
                .then(dbdatus => {
                    console.log(dbdatus)
                    const db_update = Date.parse(dbdatus[0]);
                    if (db_update > last_updated) { 
                        location.reload();
                    }
                }), 
            interval ), 
    refresh_interval.seconds * 1000)
}

function startCountdown() {

    const refreshNotification = document.querySelector("#refresh-notification");
    const p = refreshNotification.querySelector("p");
    const refreshCountdown = p.querySelector("span");
    // refresh_interval comes from the server (is in base.html)
    let displayedMinutes = refresh_interval.minutes;
    const interval = 60000 // 60 seconds
    p.classList.remove("hidden");

    setInterval(() => {      
        if (displayedMinutes == 1) {
            p.innerText = "Page will soon refresh with new inventory";
        } else {
            displayedMinutes -= 1;
            refreshCountdown.innerHTML = displayedMinutes;
            }
        }, interval    
    )
}

function millisecondsToSeconds(mil) {
    return Math.floor(mil / 1000);
}



