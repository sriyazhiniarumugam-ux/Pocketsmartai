function token() {
    return localStorage.getItem(
        "pocketsmart_token"
    );
}


function authHeaders(extra = {}) {

    const headers = {
        ...extra
    };

    if (token()) {

        headers["Authorization"] =
            "Bearer " + token();

    }

    return headers;
}


async function api(
    url,
    options = {}
) {

    options.headers = authHeaders(
        options.headers || {}
    );

    const response =
        await fetch(
            url,
            options
        );


    if (
        response.status === 401
    ) {

        localStorage.removeItem(
            "pocketsmart_token"
        );

        if (
            !location.pathname.includes(
                "login"
            )
            &&
            !location.pathname.includes(
                "register"
            )
        ) {

            location.href = "/login";

        }
    }


    const data =
        await response
            .json()
            .catch(
                () => ({
                    detail:
                        "Unexpected server response"
                })
            );


    if (!response.ok) {

        throw new Error(
            data.detail ||
            "Request failed"
        );

    }


    return data;
}


document.addEventListener(
    "DOMContentLoaded",
    async () => {

        const link =
            document.getElementById(
                "authLink"
            );

        if (!link) {
            return;
        }


        if (token()) {

            link.textContent =
                "Logout";

            link.href = "#";


            link.onclick = async () => {

                localStorage.removeItem(
                    "pocketsmart_token"
                );

                location.href = "/";

            };

        }

    }
);


function money(value) {

    return new Intl.NumberFormat(
        "en-IN",
        {
            style: "currency",
            currency: "INR",
            maximumFractionDigits: 0
        }
    ).format(value);

}


function escapeHtml(value) {

    return String(
        value ?? ""
    ).replace(
        /[&<>"']/g,
        character => ({

            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            '"': "&quot;",
            "'": "&#039;"

        })[character]
    );

}


function safeUrl(value) {

    try {

        const url =
            new URL(value);

        if (
            ["http:", "https:"]
            .includes(
                url.protocol
            )
        ) {

            return url.href;

        }

    } catch (error) {

        return "#";

    }

    return "#";
}


function renderResults(data) {

    const element =
        document.getElementById(
            "results"
        );

    if (!element) {
        return;
    }


    const plan =
        (data.budget_plan || [])
        .map(
            item => `

                <div class="budget-box">

                    <strong>
                        ${escapeHtml(
                            item.category
                        )}
                    </strong>

                    <span>
                        ${item.percentage}%
                        ·
                        ${money(item.amount)}
                    </span>

                </div>

            `
        )
        .join("");


    const recommendations =
        (data.recommendations || [])
        .map(
            item => `

                <article
                    class="recommendation"
                >

                    <span class="tag">

                        ${escapeHtml(
                            item.platform
                        )}

                    </span>


                    <h3>

                        ${escapeHtml(
                            item.name
                        )}

                    </h3>


                    <div class="price">

                        ${money(
                            item.estimated_price
                        )}

                    </div>


                    <p>

                        ${escapeHtml(
                            item.reason
                        )}

                    </p>


                    <a
                        href="${safeUrl(
                            item.search_url
                        )}"
                        target="_blank"
                        rel="noopener"
                    >

                        Search platform →

                    </a>

                </article>

            `
        )
        .join("");


    const tips =
        (data.tips || [])
        .map(
            item => `

                <li>
                    ${escapeHtml(item)}
                </li>

            `
        )
        .join("");


    const imageInsight =
        data.image_insight
            ? `

                <h3>
                    Image insight
                </h3>

                <p>
                    ${escapeHtml(
                        data.image_insight
                    )}
                </p>

              `
            : "";


    element.innerHTML = `

        <section class="result-card">

            <h2>

                Your
                ${escapeHtml(
                    data.planner
                )}
                plan

            </h2>


            <p>

                ${escapeHtml(
                    data.summary
                )}

            </p>


            <h3>
                Budget allocation
            </h3>


            <div class="budget-grid">

                ${plan}

            </div>


            <h3>

                Recommendations

                <span class="tag">

                    ${escapeHtml(
                        data.source
                    )}

                </span>

            </h3>


            <div class="recommendations">

                ${recommendations}

            </div>


            ${imageInsight}


            <h3>
                Tips
            </h3>


            <ul>
                ${tips}
            </ul>

        </section>

    `;
}