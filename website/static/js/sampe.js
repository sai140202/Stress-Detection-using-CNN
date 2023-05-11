
    //  run button to start ml model
    function toggleButton() {
        var button = document.getElementById("run-button");
        if (button.innerHTML === "Run") {
            button.innerHTML = "Stop";
            $.get("/start_process");
        } else {
            button.innerHTML = "Run";
            $.get("/stop_process");
        }
    }

