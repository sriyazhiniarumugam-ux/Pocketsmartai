document.addEventListener(
    "DOMContentLoaded",
    () => {

        const forms = [

            [
                "homeForm",
                "/api/generate-home",
                "json"
            ],

            [
                "partyForm",
                "/api/generate-party",
                "json"
            ],

            [
                "jewelryForm",
                "/api/generate-jewelry",
                "form"
            ]

        ];


        for (
            const [
                id,
                url,
                mode
            ]
            of forms
        ) {

            const form =
                document.getElementById(id);


            if (!form) {
                continue;
            }


            form.onsubmit =
                async event => {

                    event.preventDefault();


                    const loading =
                        document.getElementById(
                            "loading"
                        );


                    loading.classList.remove(
                        "hidden"
                    );


                    try {

                        const options = {
                            method: "POST"
                        };


                        if (
                            mode === "json"
                        ) {

                            const body =
                                Object.fromEntries(
                                    new FormData(
                                        form
                                    ).entries()
                                );


                            if (
                                id === "homeForm"
                            ) {

                                body.rooms =
                                    body.rooms
                                        .split(",")
                                        .map(
                                            item =>
                                                item.trim()
                                        )
                                        .filter(
                                            Boolean
                                        );

                            }


                            if (
                                id === "partyForm"
                            ) {

                                body.guests =
                                    Number(
                                        body.guests
                                    );

                            }


                            body.budget =
                                Number(
                                    body.budget
                                );


                            options.headers = {

                                "Content-Type":
                                    "application/json"

                            };


                            options.body =
                                JSON.stringify(
                                    body
                                );

                        }

                        else {

                            options.body =
                                new FormData(
                                    form
                                );

                        }


                        const data =
                            await api(
                                url,
                                options
                            );


                        renderResults(
                            data
                        );


                        window.scrollTo({

                            top:
                                document
                                    .getElementById(
                                        "results"
                                    )
                                    .offsetTop
                                - 80,

                            behavior:
                                "smooth"

                        });

                    }

                    catch (error) {

                        document
                            .getElementById(
                                "results"
                            )
                            .innerHTML = `

                                <div
                                    class="result-card"
                                >

                                    <p
                                        class="message"
                                    >

                                        ${escapeHtml(
                                            error.message
                                        )}

                                    </p>

                                </div>

                            `;

                    }

                    finally {

                        loading.classList.add(
                            "hidden"
                        );

                    }

                };

        }

    }
);