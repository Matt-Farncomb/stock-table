
interface serverRefreshObj {
    minutes: number;
    seconds: number;
    previouslyUpdated: string; //datetime string
  }

// refreshInterval comes from the server  and is in table.html)
declare var refreshInterval: serverRefreshObj;

window.onload = () => {
    // will stop the refresh initiated by the HTML when js not disabled
    window.stop();
    
    const p: HTMLParagraphElement = document.querySelector("#refresh-notification p");

    startCountdown(p); 
    initiatePageRefresh(p);
    fadeElementOnScroll("footer");               
}

// When the DB is due to start updating,
// poll the server every 10 seconds to see
// if update is complete then refresh
// when update is complete.
function initiatePageRefresh(p): void {
    // refresh_interval comes from the server (is in table.html)
    const previouslyUpdated: number = Date.parse(refreshInterval.previouslyUpdated);
    const interval = 10000 // 10 seconds

    setTimeout(() => 
        setInterval(() => 
                fetch("/api")
                .then(response => response.json())
                .then(datetimeFromDB => {
                    p.innerText = "Page data now out of date. Standby for refresh";
                    const mostRecentUpdate: number = Date.parse(datetimeFromDB);
                    if (mostRecentUpdate > previouslyUpdated) { 
                        console.log("reloading");
                        location.reload();
                    }
                }), 
            interval ), 
    refreshInterval.seconds * 1000)
}

// Update counter at top of page to inform
// user when update is complete and
// the page will refresh.
function startCountdown(p): void {

    // const p: HTMLParagraphElement = document.querySelector("#refresh-notification p");
    const refreshCountdown = p.querySelector("span");
    // refresh_interval comes from the server (is in table.html)
    let displayedMinutes = refreshInterval.minutes;
    const interval = 60000 // 60 seconds
    p.classList.remove("hidden");

    setInterval(() => {      
        if (displayedMinutes == 1) {
            p.innerText = "Page will soon refresh with new inventory";
        } else {
            displayedMinutes -= 1;
            refreshCountdown.innerHTML = String(displayedMinutes);
            }
        }, interval    
    )
}

function millisecondsToSeconds(mil: number): number {
    return Math.floor(mil / 1000);
}

// When user has scrolled past approxPageHeight, reveal/hide element.
// NOTE: Use on elements with 'transparent' class
function fadeElementOnScroll(elementName: string): void {
    const elementClasses = document.querySelector(elementName).classList;
    const approxPageHeight = 700;
    window.onscroll = () => {  
        if (window.scrollY >= approxPageHeight) {
            if (!elementClasses.contains("show")) elementClasses.add("show");       
        } else {
            if (elementClasses.contains("show")) elementClasses.remove("show");
        }
    }
}



