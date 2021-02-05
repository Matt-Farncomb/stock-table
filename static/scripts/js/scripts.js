window.onload = function () {
    // will stop the refresh initiated by the HTML when js not disabled
    window.stop();
    var p = document.querySelector("#refresh-notification p");
    startCountdown(p);
    initiatePageRefresh(p);
    fadeElementOnScroll("footer");
};
// When the DB is due to start updating,
// poll the server every 10 seconds to see
// if update is complete then refresh
// when update is complete.
function initiatePageRefresh(p) {
    // refresh_interval comes from the server (is in table.html)
    var previouslyUpdated = Date.parse(refreshInterval.previouslyUpdated);
    var interval = 10000; // 10 seconds
    setTimeout(function () {
        return setInterval(function () {
            return fetch("/api")
                .then(function (response) { return response.json(); })
                .then(function (datetimeFromDB) {
                p.innerText = "Page data now out of date. Standby for refresh";
                var mostRecentUpdate = Date.parse(datetimeFromDB);
                if (mostRecentUpdate > previouslyUpdated) {
                    console.log("reloading");
                    location.reload();
                }
            });
        }, interval);
    }, refreshInterval.seconds * 1000);
}
// Update counter at top of page to inform
// user when update is complete and
// the page will refresh.
function startCountdown(p) {
    // const p: HTMLParagraphElement = document.querySelector("#refresh-notification p");
    var refreshCountdown = p.querySelector("span");
    // refresh_interval comes from the server (is in table.html)
    var displayedMinutes = refreshInterval.minutes;
    var interval = 60000; // 60 seconds
    p.classList.remove("hidden");
    setInterval(function () {
        if (displayedMinutes == 1) {
            p.innerText = "Page will soon refresh with new inventory";
        }
        else {
            displayedMinutes -= 1;
            refreshCountdown.innerHTML = String(displayedMinutes);
        }
    }, interval);
}
function millisecondsToSeconds(mil) {
    return Math.floor(mil / 1000);
}
// When user has scrolled past approxPageHeight, reveal/hide element.
// NOTE: Use on elements with 'transparent' class
function fadeElementOnScroll(elementName) {
    var elementClasses = document.querySelector(elementName).classList;
    var approxPageHeight = 700;
    window.onscroll = function () {
        if (window.scrollY >= approxPageHeight) {
            if (!elementClasses.contains("show"))
                elementClasses.add("show");
        }
        else {
            if (elementClasses.contains("show"))
                elementClasses.remove("show");
        }
    };
}
