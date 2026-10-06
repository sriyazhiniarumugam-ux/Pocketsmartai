document.addEventListener(
    "DOMContentLoaded",
    async () => {

        try {

            const session =
                await api(
                    "/api/session-info"
                );


            document.getElementById(
                "welcome"
            ).textContent =
                `Welcome, ${session.user.name}.`;


            const history =
                await api(
                    "/api/history"
                );


            const recent =
                document.getElementById(
                    "recentPlans"
                );


            recent.innerHTML =
                history
                    .slice(0, 5)
                    .map(
                        item => `

                            <div
                                class="history-item"
                            >

                                <div>

                                    <strong>

                                        ${escapeHtml(
                                            item.planner
                                                .toUpperCase()
                                        )}

                                    </strong>


                                    <div>

                                        ${money(
                                            item.budget
                                        )}

                                    </div>

                                </div>


                                <small>

                                    ${new Date(
                                        item.created_at
                                    ).toLocaleString()}

                                </small>

                            </div>

                        `
                    )
                    .join("")
                    ||
                    "<p>No plans yet.</p>";

        }

        catch (error) {

            location.href =
                "/login";

        }

    }
);