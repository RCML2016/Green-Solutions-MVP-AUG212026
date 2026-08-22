/* =========================================================
   GREEN SOLUTIONS
   Production Landing Page JavaScript
========================================================= */


document.addEventListener(
    "DOMContentLoaded",
    () => {

        initializeNavigation();

        initializeMobileMenu();

        initializeScrollEffects();

        initializeRevealAnimations();

        initializeCurrentYear();

        initializeProductInteractions();

    }
);


/* =========================================================
   CONFIGURATION
========================================================= */

const CONFIG = {

    platformUrl:
        "https://green-solutions-ai.streamlit.app/",

    animationDuration:
        650

};


/* =========================================================
   NAVIGATION
========================================================= */

function initializeNavigation() {

    const links =
        document.querySelectorAll(
            'a[href^="#"]'
        );


    links.forEach(
        link => {

            link.addEventListener(
                "click",
                event => {

                    const targetId =
                        link.getAttribute(
                            "href"
                        );


                    if (
                        !targetId ||
                        targetId === "#"
                    ) {

                        return;

                    }


                    const target =
                        document.querySelector(
                            targetId
                        );


                    if (!target) {

                        return;

                    }


                    event.preventDefault();


                    const header =
                        document.querySelector(
                            ".site-header"
                        );


                    const offset =
                        header
                            ? header.offsetHeight
                            : 0;


                    const targetPosition =
                        target.getBoundingClientRect()
                            .top +
                        window.scrollY -
                        offset;


                    window.scrollTo(
                        {
                            top:
                                targetPosition,

                            behavior:
                                "smooth"
                        }
                    );


                    closeMobileMenu();

                }

            );

        }
    );

}


/* =========================================================
   MOBILE MENU
========================================================= */

function initializeMobileMenu() {

    const button =
        document.getElementById(
            "mobileMenuButton"
        );


    const menu =
        document.getElementById(
            "mobileMenu"
        );


    if (!button || !menu) {

        return;

    }


    button.addEventListener(
        "click",
        () => {

            menu.classList.toggle(
                "open"
            );

        }
    );

}


function closeMobileMenu() {

    const menu =
        document.getElementById(
            "mobileMenu"
        );


    if (menu) {

        menu.classList.remove(
            "open"
        );

    }

}


/* =========================================================
   HEADER SCROLL EFFECT
========================================================= */

function initializeScrollEffects() {

    const header =
        document.querySelector(
            ".site-header"
        );


    if (!header) {

        return;

    }


    function updateHeader() {

        if (
            window.scrollY > 30
        ) {

            header.style.boxShadow =
                "0 8px 30px rgba(7,28,20,.07)";

        } else {

            header.style.boxShadow =
                "none";

        }

    }


    window.addEventListener(
        "scroll",
        updateHeader,
        {
            passive: true
        }
    );


    updateHeader();

}


/* =========================================================
   REVEAL ANIMATIONS
========================================================= */

function initializeRevealAnimations() {

    const elements =
        document.querySelectorAll(
            ".pillar, .solution-card, .trust-item, .architecture-card, .vision-stat-row div"
        );


    if (
        !("IntersectionObserver" in window)
    ) {

        return;

    }


    elements.forEach(
        element => {

            element.style.opacity =
                "0";

            element.style.transform =
                "translateY(20px)";

            element.style.transition =
                "opacity .65s ease, transform .65s ease";

        }
    );


    const observer =
        new IntersectionObserver(
            entries => {

                entries.forEach(
                    entry => {

                        if (
                            !entry.isIntersecting
                        ) {

                            return;

                        }


                        entry.target.style.opacity =
                            "1";


                        entry.target.style.transform =
                            "translateY(0)";


                        observer.unobserve(
                            entry.target
                        );

                    }
                );

            },
            {
                threshold:
                    .12
            }
        );


    elements.forEach(
        element => {

            observer.observe(
                element
            );

        }
    );

}


/* =========================================================
   CURRENT YEAR
========================================================= */

function initializeCurrentYear() {

    const element =
        document.getElementById(
            "currentYear"
        );


    if (element) {

        element.textContent =
            new Date()
                .getFullYear();

    }

}


/* =========================================================
   PRODUCT INTERACTIONS
========================================================= */

function initializeProductInteractions() {

    const product =
        document.querySelector(
            ".product-window"
        );


    if (!product) {

        return;

    }


    /*
        Desktop-only subtle mouse interaction.
        Makes the product preview feel alive without
        becoming distracting.
    */

    if (
        window.matchMedia(
            "(pointer:fine)"
        ).matches
    ) {

        product.addEventListener(
            "mousemove",
            event => {

                const rect =
                    product.getBoundingClientRect();


                const x =
                    (
                        event.clientX -
                        rect.left
                    ) /
                    rect.width;


                const y =
                    (
                        event.clientY -
                        rect.top
                    ) /
                    rect.height;


                const rotateY =
                    -4 +
                    (
                        x - .5
                    ) * 5;


                const rotateX =
                    2 -
                    (
                        y - .5
                    ) * 4;


                product.style.transform =
                    `
                    perspective(1300px)
                    rotateY(${rotateY}deg)
                    rotateX(${rotateX}deg)
                    translateY(-2px)
                    `;

            }
        );


        product.addEventListener(
            "mouseleave",
            () => {

                product.style.transform =
                    `
                    perspective(1300px)
                    rotateY(-4deg)
                    rotateX(2deg)
                    `;

            }
        );

    }

}


/* =========================================================
   PLATFORM CTA TRACKING
========================================================= */

document.addEventListener(
    "click",
    event => {

        const target =
            event.target.closest(
                'a[href*="streamlit.app"]'
            );


        if (!target) {

            return;

        }


        /*
            Lightweight demo analytics hook.

            Replace this later with:
            - Google Analytics
            - Microsoft Clarity
            - PostHog
            - your own analytics endpoint

        */

        console.log(
            "[Green Solutions] Platform launch:",
            CONFIG.platformUrl
        );

    }
);


/* =========================================================
   BUTTON MICRO-INTERACTION
========================================================= */

document.addEventListener(
    "click",
    event => {

        const button =
            event.target.closest(
                ".button"
            );


        if (!button) {

            return;

        }


        button.animate(
            [
                {
                    transform:
                        "translateY(-2px) scale(1)"
                },

                {
                    transform:
                        "translateY(-2px) scale(.97)"
                },

                {
                    transform:
                        "translateY(-2px) scale(1)"
                }
            ],
            {
                duration:
                    180,

                easing:
                    "ease-out"
            }
        );

    }
);


/* =========================================================
   ACCESSIBILITY
========================================================= */

document.addEventListener(
    "keydown",
    event => {

        if (
            event.key === "Escape"
        ) {

            closeMobileMenu();

        }

    }
);


/* =========================================================
   PERFORMANCE
========================================================= */

window.addEventListener(
    "load",
    () => {

        document.body.classList.add(
            "page-loaded"
        );

    }
);
