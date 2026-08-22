/* =========================================================
   GREEN SOLUTIONS
   Enterprise AI Sustainability Intelligence
   Quick Rollout Demo
========================================================= */


/* =========================================================
   DEMO DATA
========================================================= */

const assets = [

    {
        id: "INV-01",
        status: "Critical",
        fault: "String Underperformance",
        priority: "High",
        confidence: 83,
        capacity: "250 kW",
        output: "161 kW",
        health: 64,
        impact: "Estimated generation loss",
        impactValue: "18%",
        evidence:
            "Average output is significantly below the healthy baseline for this asset.",
        action:
            "Dispatch technician to inspect string connections and combiner box.",
        category: "Electrical",
        lastReading: "10:42 AM",
        recommendation:
            "Inspect string connections, combiner box and DC-side continuity."
    },

    {
        id: "INV-02",
        status: "Attention",
        fault: "Inverter Clipping",
        priority: "Medium",
        confidence: 71,
        capacity: "300 kW",
        output: "247 kW",
        health: 78,
        impact: "Potential production loss",
        impactValue: "9%",
        evidence:
            "Output plateaus below expected peak during otherwise favorable solar conditions.",
        action:
            "Verify inverter sizing and DC input ceiling.",
        category: "Inverter",
        lastReading: "10:39 AM",
        recommendation:
            "Review inverter configuration and DC input limits."
    },

    {
        id: "INV-03",
        status: "Monitor",
        fault: "Soiling",
        priority: "Low",
        confidence: 78,
        capacity: "275 kW",
        output: "232 kW",
        health: 86,
        impact: "Estimated production loss",
        impactValue: "5%",
        evidence:
            "Output shows a gradual decline consistent with increasing soiling losses.",
        action:
            "Inspect module cleanliness and review the soiling-loss trend.",
        category: "Modules",
        lastReading: "10:41 AM",
        recommendation:
            "Schedule module cleaning and compare post-cleaning performance."
    },

    {
        id: "INV-04",
        status: "Critical",
        fault: "Communication Dropout",
        priority: "High",
        confidence: 91,
        capacity: "225 kW",
        output: "—",
        health: 58,
        impact: "Data availability",
        impactValue: "31%",
        evidence:
            "Repeated missing readings were detected during midday production hours.",
        action:
            "Check monitoring gateway connectivity and network communication.",
        category: "Monitoring",
        lastReading: "9:17 AM",
        recommendation:
            "Validate gateway connectivity, network path and monitoring vendor service."
    },

    {
        id: "INV-05",
        status: "Healthy",
        fault: "No Issue Detected",
        priority: "Low",
        confidence: 97,
        capacity: "320 kW",
        output: "305 kW",
        health: 96,
        impact: "Performance",
        impactValue: "Nominal",
        evidence:
            "Output tracks expected capacity with no abnormal intervals detected.",
        action:
            "No action required.",
        category: "Healthy",
        lastReading: "10:43 AM",
        recommendation:
            "Continue normal monitoring."
    }

];


/* =========================================================
   APPLICATION STATE
========================================================= */

const state = {

    currentPage: "overview",

    selectedAsset: "INV-01",

    workOrders: [],

    notifications: 3,

    copilotResponse: null

};


/* =========================================================
   DOM HELPERS
========================================================= */

const appContent =
    document.getElementById("app-content");

const breadcrumb =
    document.getElementById("breadcrumb-page");

const toast =
    document.getElementById("toast");


/* =========================================================
   UTILITY FUNCTIONS
========================================================= */

function getAsset(id) {

    return assets.find(
        asset => asset.id === id
    );

}


function priorityClass(priority) {

    if (priority === "High") {
        return "high";
    }

    if (priority === "Medium") {
        return "medium";
    }

    return "low";

}


function showToast(message) {

    toast.textContent = message;

    toast.classList.add("show");

    setTimeout(() => {

        toast.classList.remove("show");

    }, 2800);

}


function animateNumber(element, target) {

    if (!element) return;

    const duration = 650;

    const start = 0;

    const startTime = performance.now();

    function update(currentTime) {

        const progress =
            Math.min(
                (currentTime - startTime) / duration,
                1
            );

        const value =
            Math.round(
                start +
                (target - start) *
                progress
            );

        element.textContent = value;

        if (progress < 1) {

            requestAnimationFrame(update);

        }

    }

    requestAnimationFrame(update);

}


/* =========================================================
   NAVIGATION
========================================================= */

function setupNavigation() {

    const navItems =
        document.querySelectorAll(".nav-item");

    navItems.forEach(item => {

        item.addEventListener("click", () => {

            const page =
                item.dataset.page;

            navigate(page);

        });

    });

}


function navigate(page) {

    state.currentPage = page;

    document
        .querySelectorAll(".nav-item")
        .forEach(item => {

            item.classList.toggle(
                "active",
                item.dataset.page === page
            );

        });


    const pageNames = {

        overview: "Overview",

        intelligence: "AI Intelligence",

        assets: "Asset 360",

        operations: "Operations",

        reports: "Reports"

    };


    breadcrumb.textContent =
        pageNames[page] || "Overview";


    renderPage(page);

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });

}


/* =========================================================
   OVERVIEW
========================================================= */

function renderOverview() {

    appContent.innerHTML = `

        <div class="page-kicker">
            ENTERPRISE SUSTAINABILITY INTELLIGENCE
        </div>

        <h1>
            Turn asset data into
            <span style="color:#15935d">
                intelligent action.
            </span>
        </h1>

        <p class="subtitle">
            AI-powered operational intelligence for solar
            asset owners, operators and sustainability teams.
        </p>


        <div class="hero">

            <div class="page-kicker">
                AI PORTFOLIO INTELLIGENCE
            </div>

            <h1>
                Your portfolio is
                <span>80% healthy.</span>
            </h1>

            <p>
                Green Solutions continuously analyzes asset
                performance, identifies anomalies and converts
                findings into prioritized operational actions.
            </p>

            <div class="hero-actions">

                <button
                    class="btn primary"
                    onclick="navigate('intelligence')"
                >
                    ✦ View AI Findings
                </button>

                <button
                    class="btn dark"
                    onclick="navigate('operations')"
                >
                    View Operations Queue →
                </button>

            </div>

        </div>


        <div class="grid-5">

            <div class="kpi">

                <div class="kpi-label">
                    PORTFOLIO HEALTH
                </div>

                <div class="kpi-value">
                    80%
                </div>

                <div class="kpi-detail">
                    +4.2% vs previous period
                </div>

            </div>


            <div class="kpi">

                <div class="kpi-label">
                    ASSETS MONITORED
                </div>

                <div class="kpi-value">
                    5
                </div>

                <div class="kpi-detail">
                    Continuous AI monitoring
                </div>

            </div>


            <div class="kpi">

                <div class="kpi-label">
                    AI FINDINGS
                </div>

                <div class="kpi-value">
                    4
                </div>

                <div class="kpi-detail">
                    3 require action
                </div>

            </div>


            <div class="kpi">

                <div class="kpi-label">
                    HIGH PRIORITY
                </div>

                <div class="kpi-value">
                    2
                </div>

                <div class="kpi-detail">
                    Require attention
                </div>

            </div>


            <div class="kpi">

                <div class="kpi-label">
                    AI CONFIDENCE
                </div>

                <div class="kpi-value">
                    84%
                </div>

                <div class="kpi-detail">
                    Portfolio average
                </div>

            </div>

        </div>


        <div class="section-head">

            <h2>
                Portfolio intelligence
            </h2>

            <p>
                AI-generated insights across your monitored assets.
            </p>

        </div>


        <div class="two-col">

            <div class="card">

                <div class="card-title">
                    Portfolio Health
                </div>

                <div class="score">
                    80
                </div>

                <div class="card-caption">
                    Overall asset health score
                </div>

                <div class="progress">
                    <i style="width:80%"></i>
                </div>

                <div class="card-caption">
                    4 of 5 assets analyzed successfully
                </div>

            </div>


            <div class="card">

                <div class="card-title">
                    Priority Findings
                </div>

                <div class="card-caption">
                    AI-detected conditions requiring attention
                </div>

                ${renderFinding(
                    assets[0]
                )}

                ${renderFinding(
                    assets[3]
                )}

                ${renderFinding(
                    assets[1]
                )}

            </div>

        </div>


        ${renderCopilot()}

    `;


    setupCopilot();

}


function renderFinding(asset) {

    return `

        <div class="finding">

            <div class="finding-top">

                <div class="finding-name">

                    ${asset.id}
                    —
                    ${asset.fault}

                </div>

                <span class="badge ${priorityClass(asset.priority)}">
                    ${asset.priority}
                </span>

            </div>

            <div class="finding-body">

                ${asset.evidence}

            </div>

        </div>

    `;

}


/* =========================================================
   AI INTELLIGENCE
========================================================= */

function renderIntelligence() {

    appContent.innerHTML = `

        <div class="page-kicker">
            AI INTELLIGENCE
        </div>

        <h1>
            AI-generated asset intelligence
        </h1>

        <p class="subtitle">
            Explainable AI findings grounded in portfolio
            performance data.
        </p>


        <div class="hero">

            <div class="page-kicker">
                DIAGNOSTIC REASONING ENGINE
            </div>

            <h1>
                Detect.
                <span>Explain.</span>
                Recommend.
            </h1>

            <p>
                The AI diagnostic engine evaluates asset behavior,
                identifies abnormal patterns and recommends the
                next operational action.
            </p>

            <div class="hero-actions">

                <button
                    class="btn primary"
                    onclick="runPortfolioAnalysis()"
                >
                    ✦ Run AI Analysis
                </button>

            </div>

        </div>


        <div class="section-head">

            <h2>
                Current AI findings
            </h2>

            <p>
                Each finding includes evidence, confidence and
                a recommended action.
            </p>

        </div>


        <div class="intel-grid">

            ${assets.map(
                asset => renderIntelCard(asset)
            ).join("")}

        </div>

    `;

}


function renderIntelCard(asset) {

    return `

        <div class="intel-card">

            <div class="intel-head">

                <div>

                    <div class="asset-name">
                        ${asset.id}
                    </div>

                    <div class="fault">
                        ${asset.fault}
                    </div>

                </div>

                <span class="badge ${priorityClass(asset.priority)}">
                    ${asset.priority}
                </span>

            </div>


            <div style="
                display:flex;
                justify-content:space-between;
                margin-top:16px;
                font-size:8px;
                color:#87958e;
            ">

                <span>
                    AI CONFIDENCE
                </span>

                <strong style="color:#175c40">
                    ${asset.confidence}%
                </strong>

            </div>


            <div class="progress">

                <i
                    style="width:${asset.confidence}%"
                ></i>

            </div>


            <div class="evidence">

                <strong>
                    Evidence
                </strong>

                <br>

                ${asset.evidence}

            </div>


            <div class="action">

                <strong>
                    Recommended action:
                </strong>

                ${asset.action}

            </div>


            <div style="
                display:flex;
                justify-content:space-between;
                align-items:center;
                margin-top:18px;
            ">

                <span style="
                    font-size:8px;
                    color:#9aa69f;
                ">
                    ${asset.category}
                </span>

                <button
                    class="btn"
                    onclick="openAsset('${asset.id}')"
                >
                    View Asset 360 →
                </button>

            </div>

        </div>

    `;

}


/* =========================================================
   ASSET 360
========================================================= */

function renderAssets() {

    const asset =
        getAsset(state.selectedAsset);


    appContent.innerHTML = `

        <div class="page-kicker">
            ASSET 360
        </div>

        <h1>
            Asset-level intelligence
        </h1>

        <p class="subtitle">
            Explore AI diagnostics, operational condition and
            recommended actions for every monitored asset.
        </p>


        <div class="asset-select">

            ${assets.map(
                item => `

                    <button
                        class="asset-pill ${
                            item.id === asset.id
                                ? "active"
                                : ""
                        }"
                        onclick="selectAsset('${item.id}')"
                    >
                        ${item.id}
                    </button>

                `
            ).join("")}

        </div>


        <div class="asset-hero">

            <div>

                <div class="page-kicker">
                    ${asset.category}
                </div>

                <h2>
                    ${asset.id}
                </h2>

                <p>
                    ${asset.fault}
                    · Last reading ${asset.lastReading}
                </p>

            </div>


            <span class="badge ${priorityClass(asset.priority)}">

                ${asset.status}

            </span>

        </div>


        <div class="asset-metrics">

            <div class="metric">

                <strong>
                    ${asset.health}%
                </strong>

                <span>
                    Asset Health
                </span>

            </div>


            <div class="metric">

                <strong>
                    ${asset.confidence}%
                </strong>

                <span>
                    AI Confidence
                </span>

            </div>


            <div class="metric">

                <strong>
                    ${asset.output}
                </strong>

                <span>
                    Current Output
                </span>

            </div>

        </div>


        <div class="two-col">

            <div class="card">

                <div class="card-title">
                    AI Diagnosis
                </div>

                <div class="card-caption">
                    Explainable reasoning
                </div>

                <div class="evidence">

                    ${asset.evidence}

                </div>

                <div class="card-title">
                    Recommended Action
                </div>

                <div class="finding-body">

                    ${asset.recommendation}

                </div>

                <button
                    class="btn primary"
                    style="margin-top:18px"
                    onclick="createWorkOrder('${asset.id}')"
                >
                    Create Work Order
                </button>

            </div>


            <div class="card">

                <div class="card-title">
                    Asset Performance
                </div>

                <div class="card-caption">
                    Current operational snapshot
                </div>


                <div style="
                    margin-top:20px;
                ">

                    <div style="
                        display:flex;
                        justify-content:space-between;
                        font-size:9px;
                    ">

                        <span>
                            Health
                        </span>

                        <strong>
                            ${asset.health}%
                        </strong>

                    </div>

                    <div class="progress">
                        <i style="
                            width:${asset.health}%
                        "></i>
                    </div>


                    <div style="
                        display:flex;
                        justify-content:space-between;
                        font-size:9px;
                        margin-top:18px;
                    ">

                        <span>
                            Capacity
                        </span>

                        <strong>
                            ${asset.capacity}
                        </strong>

                    </div>


                    <div style="
                        display:flex;
                        justify-content:space-between;
                        font-size:9px;
                        margin-top:18px;
                    ">

                        <span>
                            Expected Impact
                        </span>

                        <strong>
                            ${asset.impactValue}
                        </strong>

                    </div>


                    <div style="
                        display:flex;
                        justify-content:space-between;
                        font-size:9px;
                        margin-top:18px;
                    ">

                        <span>
                            AI Category
                        </span>

                        <strong>
                            ${asset.category}
                        </strong>

                    </div>

                </div>

            </div>

        </div>

    `;

}


function selectAsset(id) {

    state.selectedAsset = id;

    renderAssets();

}


function openAsset(id) {

    state.selectedAsset = id;

    navigate("assets");

}


/* =========================================================
   OPERATIONS
========================================================= */

function renderOperations() {

    const operationalAssets =
        assets
            .filter(
                asset =>
                    asset.fault !==
                    "No Issue Detected"
            )
            .sort(
                (a, b) =>
                    b.confidence -
                    a.confidence
            );


    appContent.innerHTML = `

        <div class="page-kicker">
            OPERATIONS
        </div>

        <h1>
            AI-prioritized work queue
        </h1>

        <p class="subtitle">
            Convert AI findings into concrete operational
            actions for field teams.
        </p>


        <div class="grid-5">

            <div class="kpi">

                <div class="kpi-label">
                    OPEN ACTIONS
                </div>

                <div class="kpi-value">
                    ${operationalAssets.length}
                </div>

                <div class="kpi-detail">
                    AI-generated
                </div>

            </div>


            <div class="kpi">

                <div class="kpi-label">
                    HIGH PRIORITY
                </div>

                <div class="kpi-value">
                    ${
                        operationalAssets.filter(
                            x => x.priority === "High"
                        ).length
                    }
                </div>

                <div class="kpi-detail">
                    Immediate attention
                </div>

            </div>


            <div class="kpi">

                <div class="kpi-label">
                    AI CONFIDENCE
                </div>

                <div class="kpi-value">
                    84%
                </div>

                <div class="kpi-detail">
                    Average
                </div>

            </div>


            <div class="kpi">

                <div class="kpi-label">
                    WORK ORDERS
                </div>

                <div class="kpi-value">
                    ${state.workOrders.length}
                </div>

                <div class="kpi-detail">
                    Created in demo
                </div>

            </div>


            <div class="kpi">

                <div class="kpi-label">
                    RESPONSE
                </div>

                <div class="kpi-value">
                    AI
                </div>

                <div class="kpi-detail">
                    Automated triage
                </div>

            </div>

        </div>


        <div class="section-head">

            <h2>
                Priority work queue
            </h2>

            <p>
                AI-ranked based on condition, confidence and
                operational impact.
            </p>

        </div>


        ${operationalAssets.map(
            (asset, index) => `

                <div class="ops-row">

                    <div class="num">
                        ${String(index + 1).padStart(2, "0")}
                    </div>


                    <div>

                        <strong>
                            ${asset.id}
                        </strong>

                        <small>
                            ${asset.category}
                        </small>

                    </div>


                    <div>

                        <strong>
                            ${asset.fault}
                        </strong>

                        <small>
                            ${asset.action}
                        </small>

                    </div>


                    <div>

                        <span class="badge ${priorityClass(asset.priority)}">
                            ${asset.priority}
                        </span>

                    </div>


                    <div>

                        <button
                            class="btn"
                            onclick="createWorkOrder('${asset.id}')"
                        >
                            Create Work Order
                        </button>

                    </div>

                </div>

            `
        ).join("")}

    `;

}


/* =========================================================
   REPORTS
========================================================= */

function renderReports() {

    appContent.innerHTML = `

        <div class="page-kicker">
            REPORTING CENTER
        </div>

        <h1>
            AI-generated reports
        </h1>

        <p class="subtitle">
            Generate audience-specific reporting from the same
            underlying AI diagnostic findings.
        </p>


        <div class="reports">

            <div class="report">

                <div class="report-icon">
                    🔧
                </div>

                <h3>
                    Field Work Order
                </h3>

                <p>
                    Technician-ready work instructions containing
                    asset IDs, fault conditions and recommended
                    checks.
                </p>

                <button
                    class="btn primary"
                    onclick="openReport('work-order')"
                >
                    View Report
                </button>

            </div>


            <div class="report">

                <div class="report-icon">
                    ◈
                </div>

                <h3>
                    Owner Report
                </h3>

                <p>
                    Executive-friendly summary explaining what
                    happened, expected impact and actions underway.
                </p>

                <button
                    class="btn primary"
                    onclick="openReport('owner')"
                >
                    View Report
                </button>

            </div>


            <div class="report">

                <div class="report-icon">
                    ▣
                </div>

                <h3>
                    Compliance Summary
                </h3>

                <p>
                    Formal record of findings, actions taken and
                    current status for regulatory and investor use.
                </p>

                <button
                    class="btn primary"
                    onclick="openReport('compliance')"
                >
                    View Report
                </button>

            </div>

        </div>


        <div class="section-head">

            <h2>
                Reporting intelligence
            </h2>

            <p>
                One AI analysis can serve multiple business audiences.
            </p>

        </div>


        <div class="card" style="padding:24px">

            <div class="card-title">
                Unified AI reporting pipeline
            </div>

            <div style="
                display:grid;
                grid-template-columns:
                    repeat(4,1fr);
                gap:10px;
                margin-top:20px;
            ">

                <div class="metric">
                    <strong>01</strong>
                    <span>Asset Data</span>
                </div>

                <div class="metric">
                    <strong>02</strong>
                    <span>AI Diagnosis</span>
                </div>

                <div class="metric">
                    <strong>03</strong>
                    <span>Human Review</span>
                </div>

                <div class="metric">
                    <strong>04</strong>
                    <span>Reports</span>
                </div>

            </div>

        </div>

    `;

}


/* =========================================================
   REPORT MODAL
========================================================= */

function openReport(type) {

    const reportData = {

        "work-order": {

            title: "Field Work Order",

            content: `
                1. INV-01 — Inspect string connections
                and combiner box.

                2. INV-02 — Verify inverter DC input
                ceiling and sizing.

                3. INV-04 — Check monitoring gateway
                and network connectivity.
            `

        },

        owner: {

            title: "Owner Report",

            content: `
                Four assets were analyzed during the current
                review period. INV-01 is underperforming and
                requires electrical inspection. INV-02 shows
                signs of inverter clipping. INV-04 has a
                communication issue affecting data availability.

                The remaining portfolio is performing within
                expected operating conditions.
            `

        },

        compliance: {

            title: "Compliance Summary",

            content: `
                Current review period findings:

                INV-01 — String underperformance identified.
                Corrective inspection recommended.

                INV-02 — Inverter clipping identified.
                Engineering review recommended.

                INV-04 — Communication fault identified.
                Monitoring connectivity review required.

                INV-05 — No abnormal condition detected.
            `

        }

    };


    const report =
        reportData[type];


    const modal =
        document.createElement("div");

    modal.style.cssText = `

        position:fixed;
        inset:0;
        background:rgba(3,25,17,.62);
        display:grid;
        place-items:center;
        z-index:500;
        padding:20px;

    `;


    modal.innerHTML = `

        <div style="
            background:#fff;
            max-width:650px;
            width:100%;
            border-radius:18px;
            padding:25px;
            box-shadow:0 25px 80px rgba(0,0,0,.25);
        ">

            <div style="
                display:flex;
                justify-content:space-between;
                align-items:center;
            ">

                <h2 style="
                    margin:0;
                    font-size:18px;
                ">
                    ${report.title}
                </h2>

                <button
                    class="btn"
                    id="close-report"
                >
                    Close
                </button>

            </div>


            <div style="
                margin-top:20px;
                padding:18px;
                background:#f7faf8;
                border:1px solid #e3ebe6;
                border-radius:12px;
                font-size:10px;
                line-height:1.8;
                white-space:pre-line;
                color:#51655b;
            ">
                ${report.content}
            </div>


            <button
                class="btn primary"
                style="margin-top:15px"
                id="download-report"
            >
                Download Demo Report
            </button>

        </div>

    `;


    document.body.appendChild(modal);


    document
        .getElementById("close-report")
        .onclick = () => {

            modal.remove();

        };


    document
        .getElementById("download-report")
        .onclick = () => {

            downloadTextFile(
                report.title,
                report.content
            );

        };

}


function downloadTextFile(
    filename,
    content
) {

    const blob =
        new Blob(
            [content],
            {
                type: "text/plain"
            }
        );


    const url =
        URL.createObjectURL(blob);


    const link =
        document.createElement("a");


    link.href = url;

    link.download =
        filename
            .replaceAll(" ", "_")
            .toLowerCase() +
        ".txt";


    link.click();


    URL.revokeObjectURL(url);


    showToast(
        "Report downloaded."
    );

}


/* =========================================================
   WORK ORDERS
========================================================= */

function createWorkOrder(id) {

    const asset =
        getAsset(id);


    if (
        state.workOrders.includes(id)
    ) {

        showToast(
            `${id} already has a work order.`
        );

        return;

    }


    state.workOrders.push(id);


    showToast(
        `Work order created for ${id}.`
    );


    if (
        state.currentPage ===
        "operations"
    ) {

        renderOperations();

    }

}


/* =========================================================
   AI ANALYSIS
========================================================= */

function runPortfolioAnalysis() {

    showToast(
        "AI diagnostic analysis started..."
    );


    setTimeout(() => {

        showToast(
            "Analysis complete — 4 findings identified."
        );

        navigate(
            "intelligence"
        );

    }, 1200);

}


/* =========================================================
   AI COPILOT
========================================================= */

function renderCopilot() {

    return `

        <div class="copilot">

            <h3>
                ✦ AI Copilot
            </h3>

            <p>
                Ask questions about your portfolio,
                asset health or recommended actions.
            </p>


            <div class="copilot-form">

                <input
                    id="copilot-input"
                    type="text"
                    placeholder="Ask: Which assets need immediate attention?"
                >

                <button
                    class="btn primary"
                    id="copilot-submit"
                >
                    Ask AI
                </button>

            </div>


            <div
                id="copilot-response"
                class="response"
                style="
                    display:
                        ${
                            state.copilotResponse
                                ? "block"
                                : "none"
                        };
                "
            >

                ${
                    state.copilotResponse ||
                    ""
                }

            </div>

        </div>

    `;

}


function setupCopilot() {

    const input =
        document.getElementById(
            "copilot-input"
        );


    const button =
        document.getElementById(
            "copilot-submit"
        );


    if (!input || !button) {

        return;

    }


    function ask() {

        const question =
            input.value
                .trim();


        if (!question) {

            showToast(
                "Enter a question first."
            );

            return;

        }


        const response =
            generateCopilotResponse(
                question
            );


        state.copilotResponse =
            response;


        const responseBox =
            document.getElementById(
                "copilot-response"
            );


        responseBox.style.display =
            "block";


        responseBox.textContent =
            response;


        input.value = "";

    }


    button.addEventListener(
        "click",
        ask
    );


    input.addEventListener(
        "keydown",
        event => {

            if (
                event.key === "Enter"
            ) {

                ask();

            }

        }
    );

}


function generateCopilotResponse(
    question
) {

    const q =
        question.toLowerCase();


    if (
        q.includes("immediate") ||
        q.includes("urgent") ||
        q.includes("attention")
    ) {

        return `
AI assessment:

INV-04 has the highest diagnostic confidence at 91%
and is classified as High Priority because monitoring
data is repeatedly dropping during production hours.

INV-01 is also High Priority with an 83% AI confidence
score and requires an electrical inspection.

Recommended sequence:
1. Investigate INV-04 communication.
2. Inspect INV-01 string connections.
3. Review INV-02 inverter configuration.
        `.trim();

    }


    if (
        q.includes("healthy") ||
        q.includes("health")
    ) {

        return `
Portfolio health is currently estimated at 80%.

INV-05 is the healthiest monitored asset with a 96%
health score and 97% AI confidence.

INV-03 remains operational but should be monitored
for increasing soiling losses.
        `.trim();

    }


    if (
        q.includes("action") ||
        q.includes("recommend")
    ) {

        return `
AI recommended actions:

• INV-01 — Inspect string connections.
• INV-02 — Verify inverter DC input ceiling.
• INV-03 — Schedule module cleaning.
• INV-04 — Validate monitoring gateway connectivity.
• INV-05 — Continue normal monitoring.
        `.trim();

    }


    if (
        q.includes("confidence") ||
        q.includes("accurate")
    ) {

        return `
The current portfolio-average AI confidence is
approximately 84%.

Highest-confidence finding:
INV-04 — Communication Dropout at 91%.

Lowest-confidence finding:
INV-02 — Inverter Clipping at 71%.

Lower-confidence findings should be reviewed by
an operations expert before automated action.
        `.trim();

    }


    return `
Based on the current portfolio analysis, Green Solutions
identified four findings across five monitored assets.

The highest priorities are INV-04 and INV-01.

I recommend reviewing the AI Intelligence and Operations
sections for the detailed evidence and next actions.
    `.trim();

}


/* =========================================================
   PAGE ROUTER
========================================================= */

function renderPage(page) {

    switch (page) {

        case "overview":

            renderOverview();

            break;


        case "intelligence":

            renderIntelligence();

            break;


        case "assets":

            renderAssets();

            break;


        case "operations":

            renderOperations();

            break;


        case "reports":

            renderReports();

            break;


        default:

            renderOverview();

    }

}


/* =========================================================
   INITIALIZE APPLICATION
========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    () => {

        setupNavigation();

        renderOverview();

    }
);
