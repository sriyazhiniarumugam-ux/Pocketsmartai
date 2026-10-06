function showMessage(
    text,
    success = false
) {

    const element =
        document.getElementById(
            "formMessage"
        );

    element.textContent = text;

    element.style.color =
        success
            ? "green"
            : "crimson";
}


async function submitAuth(
    form,
    endpoint
) {

    try {

        const body =
            Object.fromEntries(
                new FormData(form).entries()
            );


        const data =
            await api(
                endpoint,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(body)
                }
            );


        localStorage.setItem(
            "pocketsmart_token",
            data.access_token
        );


        location.href =
            "/dashboard";

    }

    catch (error) {

        showMessage(
            error.message
        );

    }

}


document.addEventListener(
    "DOMContentLoaded",
    () => {

        const loginForm =
            document.getElementById(
                "loginForm"
            );


        if (loginForm) {

            loginForm.onsubmit =
                event => {

                    event.preventDefault();

                    submitAuth(
                        loginForm,
                        "/api/login"
                    );

                };

        }


        const registerForm =
            document.getElementById(
                "registerForm"
            );


        if (registerForm) {

            registerForm.onsubmit =
                event => {

                    event.preventDefault();

                    submitAuth(
                        registerForm,
                        "/api/register"
                    );

                };

        }

    }
);