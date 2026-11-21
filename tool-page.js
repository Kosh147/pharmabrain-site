// Renders a platform system page (qms.html, ectd.html, tasks.html, pv.html).
// The page names its system in <body data-tool="…">; the system's screenshots, agents and counts come from
// window.PLATFORM (i18n.js), its texts from TOOLS_I18N (tools.i18n.js) with the shared site strings (I18N) as fallback.
(function () {
    const LANGS = ["ru", "en", "zh", "ar", "tr", "hi"];
    const RTL_LANGS = ["ar"];
    const TOOL = PLATFORM.find(p => p.id === document.body.dataset.tool);
    const X = TOOL.prefix;
    let lang = "ru";
    let shot = 0;

    // Page strings (TOOLS_I18N) first, then the shared site strings (I18N); English, then Russian, as fallback.
    const t = (key, vars) => {
        let s = null;
        for (const dict of [window.TOOLS_I18N, window.I18N]) {
            s = (dict[lang] && dict[lang][key]) || (lang !== "ru" && dict.en[key]);
            if (s) break;
        }
        s = s || TOOLS_I18N.ru[key] || I18N.ru[key] || key;
        if (vars) Object.entries(vars).forEach(([k, v]) => { s = s.replace("{" + k + "}", v); });
        return s;
    };
    const withLang = (href) => {
        const [path, hash] = href.split("#");
        return path + (lang === "ru" ? "" : "?lang=" + lang) + (hash ? "#" + hash : "");
    };
    const range = (n) => Array.from({ length: n }, (_, i) => i + 1);
    const shotSrc = (id) => "images/platform/" + id + ".jpg";

    const app = document.getElementById("app");
    app.innerHTML = `
    <header class="nav">
        <div class="container nav-inner">
            <a class="logo" href="./" data-home><img src="images/logo.png" data-i18n-alt="brand" alt=""></a>
            <nav class="nav-links" id="navLinks">
                <a href="./" data-home data-i18n="tp_nav_back"></a>
                <a href="#features" data-i18n="tp_nav_features"></a>
                <a href="#agents" data-i18n="tp_nav_agents"></a>
                <a href="#screens" data-i18n="tp_nav_screens"></a>
                <a href="#plans" data-i18n="tp_nav_plans"></a>
                <a class="nav-cta" href="#contact" data-i18n="tp_nav_demo"></a>
            </nav>
            <div class="nav-tools">
                <select class="lang-select" id="langSelect" data-i18n-aria="lang">
                    <option value="ru">RU · Русский</option>
                    <option value="en">EN · English</option>
                    <option value="zh">中文</option>
                    <option value="ar">العربية</option>
                    <option value="tr">TR · Türkçe</option>
                    <option value="hi">हिन्दी</option>
                </select>
                <button class="menu-btn" id="menuBtn" data-i18n-aria="menu">☰</button>
            </div>
        </div>
    </header>

    <section class="hero" id="top">
        <div class="container hero-grid">
            <div>
                <span class="eyebrow" data-i18n="${X}_eyebrow"></span>
                <h1 data-i18n="${X}_h1"></h1>
                <p class="hero-lead" data-i18n="${X}_lead"></p>
                <div class="hero-actions">
                    <a class="btn btn-primary" href="#contact" data-i18n="tp_cta_demo"></a>
                    <a class="btn btn-ghost" href="#agents" data-i18n="tp_cta_agents"></a>
                </div>
                <div class="hero-meta">
                    ${range(3).map(i => `<span data-i18n="${X}_meta${i}"></span>`).join("")}
                </div>
            </div>
            <div class="shot-wrap">
                <img src="${shotSrc(TOOL.img.replace(/\.jpg$/, ""))}" width="1360" height="820" data-i18n-alt="${X}_h1" alt="">
            </div>
        </div>
    </section>

    <section class="white" id="features">
        <div class="container">
            <p class="kicker" data-i18n="tp_feat_kicker"></p>
            <h2 data-i18n="${X}_feat_h2"></h2>
            <p class="sub" data-i18n="${X}_feat_sub"></p>
            <div class="grid-3">
                ${range(6).map(i => `
                <article class="card">
                    <span class="n">0${i}</span>
                    <h3 data-i18n="${X}_f${i}_h"></h3>
                    <p data-i18n="${X}_f${i}_p"></p>
                </article>`).join("")}
            </div>
            ${TOOL.sources ? `
            <div class="sources">
                <h3 data-i18n="${X}_src_h"></h3>
                <div class="chips">${range(TOOL.sources).map(i => `<span data-i18n="${X}_src${i}"></span>`).join("")}</div>
            </div>` : ""}
        </div>
    </section>

    <section id="flow">
        <div class="container">
            <p class="kicker" data-i18n="tp_flow_kicker"></p>
            <h2 data-i18n="${X}_flow_h2"></h2>
            <p class="sub" data-i18n="${X}_flow_sub"></p>
            <ol class="flow">${range(TOOL.steps).map(i => `<li data-i18n="${X}_step${i}"></li>`).join("")}</ol>
        </div>
    </section>

    <section class="white" id="screens">
        <div class="container">
            <p class="kicker" data-i18n="tp_screens_kicker"></p>
            <h2 data-i18n="tp_screens_h2"></h2>
            <div class="tour-tabs" id="tourTabs"></div>
            <div class="tour-stage">
                <a id="tourLink" href="#" target="_blank" rel="noopener">
                    <img id="tourImg" width="1360" height="820" alt="">
                </a>
                <div class="tour-copy">
                    <p class="kicker" id="tourName"></p>
                    <h3 id="tourTitle"></h3>
                    <p id="tourText"></p>
                    <div class="tour-nav">
                        <button type="button" id="tourPrev" data-i18n-aria="tp_prev">←</button>
                        <button type="button" id="tourNext" data-i18n-aria="tp_next">→</button>
                    </div>
                </div>
            </div>
            <p class="tour-note" data-i18n="tp_screens_note"></p>
        </div>
    </section>

    <section id="agents">
        <div class="container">
            <p class="kicker" data-i18n="tp_agents_kicker"></p>
            <h2 data-i18n="${X}_agents_h2"></h2>
            <p class="sub" data-i18n="${X}_agents_sub"></p>
            <div class="agents" id="agentGrid"></div>
            <p class="agents-more"><a href="./#catalog" data-home-hash="catalog" data-i18n="tp_ag_all"></a></p>
        </div>
    </section>

    <section class="white" id="gxp">
        <div class="container">
            <p class="kicker" data-i18n="tp_gxp_kicker"></p>
            <h2 data-i18n="tp_gxp_h2"></h2>
            <p class="sub" data-i18n="tp_gxp_sub"></p>
            <div class="grid-4">
                ${range(4).map(i => `
                <article class="card">
                    <h3 data-i18n="tp_gxp${i}_h"></h3>
                    <p data-i18n="tp_gxp${i}_p"></p>
                </article>`).join("")}
            </div>
            <div class="related">
                <h3 data-i18n="tp_related_h"></h3>
                <div class="related-grid">
                    ${PLATFORM.filter(p => p.id !== TOOL.id).map(p => `
                    <a href="${p.page}" data-page="${p.page}">
                        <strong data-i18n="pf_${p.id}_name"></strong>
                        <span data-i18n="pf_${p.id}_p"></span>
                    </a>`).join("")}
                </div>
            </div>
        </div>
    </section>

    <section id="plans">
        <div class="container">
            <p class="kicker" data-i18n="tp_plans_kicker"></p>
            <h2 data-i18n="plans_h2"></h2>
            <p class="sub" data-i18n="plans_sub"></p>
            <div class="plans">
                ${[1, 2].map(n => `
                <article class="plan${n === 1 ? " main" : ""}">
                    <span class="plan-tag" data-i18n="plan${n}_tag"></span>
                    <h3 data-i18n="plan${n}_name"></h3>
                    <p class="lead" data-i18n="plan${n}_lead"></p>
                    <ul class="check-list">${range(5).map(i => `<li data-i18n="plan${n}_l${i}"></li>`).join("")}</ul>
                    <a class="btn ${n === 1 ? "btn-teal" : "btn-navy"}" href="#contact" data-plan="${n === 1 ? "individual" : "enterprise"}" data-i18n="plan${n}_cta"></a>
                </article>`).join("")}
            </div>
            <p class="plans-note" data-i18n="plans_note"></p>
        </div>
    </section>

    <section id="contact">
        <div class="container">
            <p class="kicker" data-i18n="tp_contact_kicker"></p>
            <h2 data-i18n="tp_contact_h2"></h2>
            <p class="sub" data-i18n="tp_contact_sub"></p>
            <div class="contact-grid">
                <form class="form" id="contactForm">
                    <div class="form-row">
                        <label for="name" data-i18n="form_name"></label>
                        <input id="name" name="name" required>
                    </div>
                    <div class="form-row">
                        <label for="email" data-i18n="form_email"></label>
                        <input id="email" name="email" type="email" required>
                    </div>
                    <div class="form-row">
                        <label for="phone" data-i18n="form_phone"></label>
                        <input id="phone" name="phone" type="tel" placeholder="+7 (XXX) XXX-XX-XX" required>
                    </div>
                    <div class="form-row">
                        <label for="company" data-i18n="form_company"></label>
                        <input id="company" name="company">
                    </div>
                    <div class="form-row">
                        <label for="plan" data-i18n="form_plan"></label>
                        <select id="plan" name="plan">
                            <option value="" data-i18n="form_plan_none"></option>
                            <option value="individual" data-i18n="plan1_name"></option>
                            <option value="enterprise" data-i18n="plan2_name"></option>
                        </select>
                    </div>
                    <div class="form-row">
                        <label for="message" data-i18n="tp_form_message"></label>
                        <textarea id="message" name="interest" data-i18n-placeholder="${X}_form_ph" required></textarea>
                    </div>
                    <button class="btn btn-teal" type="submit" style="width:100%; border-radius:12px;" data-i18n="form_submit"></button>
                    <div class="toast" id="formToast"></div>
                </form>
                <div class="contact-card">
                    <h3 data-i18n="tp_contacts_h"></h3>
                    <p data-i18n="office_address"></p>
                    <p>Email: <a href="mailto:rk@pharmabrain.ru">rk@pharmabrain.ru</a><br>
                    <span data-i18n="phone_label"></span>: <a href="tel:+79261291266" dir="ltr">+7 926 129-12-66</a><br>
                    Telegram: <a href="https://t.me/Ruslan_V_Kalashnikov" target="_blank" rel="noopener">@Ruslan_V_Kalashnikov</a></p>
                </div>
            </div>
        </div>
    </section>

    <footer>
        <div class="container">
            <div style="display:flex; align-items:center; gap:12px;">
                <img src="images/logo.png" data-i18n-alt="brand" alt="" style="height:36px; width:auto;">
                <span>© <a href="https://lpt.digital/" target="_blank" rel="noopener" data-i18n="footer_company"></a></span>
            </div>
            <div data-i18n="footer_tag"></div>
        </div>
    </footer>`;

    function renderTour() {
        const n = shot + 1;
        const img = document.getElementById("tourImg");
        img.src = shotSrc(TOOL.shots[shot]);
        img.alt = t(X + "_shot" + n + "_h");
        document.getElementById("tourLink").href = img.src;
        document.getElementById("tourName").textContent = t(X + "_shot" + n + "_h");
        document.getElementById("tourTitle").textContent = t(X + "_shot" + n + "_t");
        document.getElementById("tourText").textContent = t(X + "_shot" + n + "_p");
        document.getElementById("tourTabs").innerHTML = TOOL.shots.map((_, i) =>
            `<button type="button" class="tour-tab${i === shot ? " active" : ""}" data-shot-i="${i}">${t(X + "_shot" + (i + 1) + "_h")}</button>`
        ).join("");
    }

    function renderAgents() {
        document.getElementById("agentGrid").innerHTML = TOOL.agents.map(id => {
            const item = AGENTS.find(a => a.id === id);
            const name = item ? loc(item.name, lang) : t("ag_" + id + "_name");
            const full = item ? loc(item.full, lang) : t("ag_" + id + "_full");
            return `
            <article class="agent">
                <span class="badge${item ? "" : " builtin"}">${t(item ? "tp_ag_catalog" : "tp_ag_builtin")}</span>
                <h3>${name}</h3>
                <p class="full">${full}</p>
                <p>${t(X + "_ag_" + id)}</p>
            </article>`;
        }).join("");
    }

    function applyStatic() {
        document.documentElement.lang = lang;
        document.documentElement.dir = RTL_LANGS.includes(lang) ? "rtl" : "ltr";
        document.title = t(X + "_title");
        const meta = document.querySelector('meta[name="description"]');
        if (meta) meta.setAttribute("content", t(X + "_description"));
        document.querySelectorAll("[data-i18n]").forEach(el => { el.textContent = t(el.dataset.i18n); });
        document.querySelectorAll("[data-i18n-placeholder]").forEach(el => { el.placeholder = t(el.dataset.i18nPlaceholder); });
        document.querySelectorAll("[data-i18n-alt]").forEach(el => { el.alt = t(el.dataset.i18nAlt); });
        document.querySelectorAll("[data-i18n-aria]").forEach(el => { el.setAttribute("aria-label", t(el.dataset.i18nAria)); });
        document.querySelectorAll("[data-home]").forEach(a => { a.href = withLang("./"); });
        document.querySelectorAll("[data-home-hash]").forEach(a => { a.href = withLang("./#" + a.dataset.homeHash); });
        document.querySelectorAll("[data-page]").forEach(a => { a.href = withLang(a.dataset.page); });
        document.getElementById("langSelect").value = lang;
        renderTour();
        renderAgents();
    }

    function setLang(next) {
        lang = LANGS.includes(next) ? next : "ru";
        try { localStorage.setItem("farmozg-lang", lang); } catch (e) {}
        const url = new URL(location.href);
        if (lang === "ru") url.searchParams.delete("lang");
        else url.searchParams.set("lang", lang);
        history.replaceState(null, "", url.pathname + url.search + url.hash);
        applyStatic();
    }

    document.getElementById("langSelect").addEventListener("change", e => setLang(e.target.value));
    document.getElementById("tourTabs").addEventListener("click", e => {
        const b = e.target.closest("[data-shot-i]");
        if (b) { shot = +b.dataset.shotI; renderTour(); }
    });
    document.getElementById("tourPrev").onclick = () => { shot = (shot + TOOL.shots.length - 1) % TOOL.shots.length; renderTour(); };
    document.getElementById("tourNext").onclick = () => { shot = (shot + 1) % TOOL.shots.length; renderTour(); };
    document.querySelectorAll("[data-plan]").forEach(a => {
        a.addEventListener("click", () => { document.getElementById("plan").value = a.dataset.plan; });
    });
    const navLinks = document.getElementById("navLinks");
    document.getElementById("menuBtn").onclick = () => navLinks.classList.toggle("open");
    navLinks.querySelectorAll("a").forEach(a => a.addEventListener("click", () => navLinks.classList.remove("open")));

    document.getElementById("contactForm").addEventListener("submit", async (e) => {
        e.preventDefault();
        const form = e.target;
        const toast = document.getElementById("formToast");
        // The request names the system and the plan in Russian, so the team reads it the same way in every language.
        const plan = form.plan.value === "individual" ? I18N.ru.plan1_name : form.plan.value === "enterprise" ? I18N.ru.plan2_name : "";
        const product = I18N.ru["pf_" + TOOL.id + "_name"] + (plan ? " · " + I18N.ru.plan_prefix + plan : "");
        const interest = [I18N.ru.product_prefix + product, form.interest.value].join("\n");
        try {
            const response = await fetch("https://pharmabrain.ru/PharmAI/api/contact", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    name: form.name.value,
                    email: form.email.value,
                    phone: form.phone.value,
                    company: form.company.value || null,
                    interest
                })
            });
            const result = await response.json();
            toast.className = "toast " + (result.success ? "ok" : "err");
            toast.textContent = result.success ? result.message : (result.error || t("form_fail"));
            if (result.success) form.reset();
        } catch (err) {
            toast.className = "toast err";
            toast.textContent = t("form_fail_mail");
        }
    });

    const params = new URLSearchParams(location.search);
    const browserLang = (navigator.language || "").toLowerCase().slice(0, 2);
    let savedLang = null;
    try { savedLang = localStorage.getItem("farmozg-lang"); } catch (e) {}
    setLang(params.get("lang") || savedLang || (LANGS.includes(browserLang) ? browserLang : "ru"));
    if (location.hash) {
        const target = document.querySelector(location.hash);
        if (target) target.scrollIntoView();
    }
})();
