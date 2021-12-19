function resizeIframe(obj) {
    obj.style.height = obj.contentWindow.document.documentElement.scrollHeight + 'px';
}

var data = {"direction": 0, "speed": 0, "AI": 0}  // This dictionary will be sent to the Raspberry Pi

autoDrive = false;  

// Get elements
up_button = document.getElementById("up");
down_button = document.getElementById("down");
left_button = document.getElementById("left");
right_button = document.getElementById("right");
autoDrive_switch = document.getElementById("autodrive");

// Events for up button
up_button.addEventListener("mousedown", upPress, false);  // If button is pressed
up_button.addEventListener("mouseup", resetPress, false);  // If button is released
up_button.addEventListener("mouseleave", resetPress, false);  // If mouse leaves button boundaries (for example while still pressing it)

// Events for down button
down_button.addEventListener("mousedown", downPress, false);
down_button.addEventListener("mouseup", resetPress, false);
down_button.addEventListener("mouseleave", resetPress, false);

// Events for left button
left_button.addEventListener("mousedown", leftPress, false);
left_button.addEventListener("mouseup", resetPress, false);
left_button.addEventListener("mouseleave", resetPress, false);

// Events for right button
right_button.addEventListener("mousedown", rightPress, false);
right_button.addEventListener("mouseup", resetPress, false);
right_button.addEventListener("mouseleave", resetPress, false);

// Events for autoDrive switch
autoDrive_switch.addEventListener("click", switchAutoDrive, false);


// This function is executed when the auto-drive switch is pressed.
function switchAutoDrive() {
    autoDrive = autoDrive_switch.checked;
    console.log("Switched auto drive to", autoDrive);
    resetPress();
}

// Up (forwards) is pressed
function upPress(e) {
    e.preventDefault();
    data["direction"] = 0
    if (!autoDrive) data["speed"] = 1;
    sendDirection()
}
// Down (backwards) is pressed
function downPress(e) {
    e.preventDefault();
    data["direction"] = 2
    if (!autoDrive) data["speed"] = 1;
    sendDirection()
}
// Left is pressed
function leftPress(e) {
    e.preventDefault();
    data["direction"] = 1
    if (!autoDrive) data["speed"] = 1;
    sendDirection()
}
// Right is pressed
function rightPress(e) {
    e.preventDefault();
    data["direction"] = 3
    if (!autoDrive) data["speed"] = 1;
    sendDirection()
}
// Reset direction
function resetPress(e) {
    if (e) e.preventDefault();
    data["direction"] = 0
    data["speed"] = autoDrive ? 1 : 0  // If auto-drive is on, keep speed at 1, else, speed = 0
    sendDirection()
}

// Post new data to RPi
function sendDirection() {
    $.ajax({
        type: "POST",
        url: "/receiver",
        contentType: "application/json",
        data: JSON.stringify(data),
        dataType: "json",
        success: function(response) {},
        error: function(err) {}
    });
}
