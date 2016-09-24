var arkControl = new Terminal('terminal');

// set styling to nothing because it's
// handled by matrix.css and matrix.js
arkControl.setWidth("");
arkControl.setHeight("");
arkControl.setTextColor("");
arkControl.setBackgroundColor("");

// append it to body
document.body.appendChild(arkControl.html);

// global inputHandler for prompts
var inputHandler = function (ans) {
    console.log(ans);
    switch (ans.toLowerCase()) {
        case 'help':
            arkControl.print("Commands available:\n\t'help'\n\t'ark-info'");
            break;
        case 'ark-info':
            arkControl.print("The ship is currently repairing. Will be ready to sail within a few days.");
            break;
        default:
            arkControl.print("Hey. Quit bugging around.");
    }
    arkControl.input("", inputHandler);
}

// Main logic
arkControl.print("Connecting ...");
arkControl.print("Logged in @ark.");
arkControl.input("Welcome aboard. Type 'help' to recieve help.", inputHandler);

