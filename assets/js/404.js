let seconds = 5;

const countdownEl =
    document.getElementById(
        "countdown"
    );


const timer =
    setInterval(
        () => {

            seconds -= 1;


            if (countdownEl) {

                countdownEl.textContent =
                    seconds;

            }


            if (seconds <= 0) {

                clearInterval(timer);

                window.location.href =
                    "index.html";

            }

        },
        1000
    );
