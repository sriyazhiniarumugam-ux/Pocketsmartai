document.addEventListener(
    "DOMContentLoaded",
    async () => {

        try {

            const rows =
                await api(
                    "/api/history"
                );


            const element =
                document.getElementById(
                    "historyList"
                );


            element.innerHTML =
                rows
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

                                        PLAN

                                    </strong>


                                    <div>

                                        Budget:

                                        ${money(
                                            item.budget
                                        )}

                                    </div>


                                    <small>

                                        ${new Date(
                                            item.created_at
                                        ).toLocaleString()}

                                    </small>

                                </div>


                                <a
                                    class="btn ghost"
                                    href="/planner/${item.planner}"
                                >

                                    Create again

                                </a>

                            </div>

                        `
                    )
                    .join("")
                    ||
                    "<p>No saved recommendations yet.</p>";

        }

        catch (error) {

            document.getElementById(
                "historyList"
            ).innerHTML = `

                <p>

                    ${escapeHtml(
                        error.message
                    )}

                </p>

            `;

        }

    }
);