(function () {
  var toggle = document.querySelector(".menu-toggle");
  var nav = document.querySelector(".nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  document.addEventListener("click", function (e) {
    var node = e.target;
    if (!node) return;
    if (node.nodeType !== 1) node = node.parentElement;
    if (!node || !node.closest) return;
    var el = node.closest("[data-track]");
    if (!el) return;
    track(el.getAttribute("data-track"), {
      label: el.getAttribute("data-track-label") || "",
      href: el.getAttribute("href") || "",
    });
  });

  var params = new URLSearchParams(window.location.search);
  var interest = params.get("interest") || "";
  if (
    interest === "virtual-bookkeeping" ||
    interest === "bookkeeping" ||
    interest === "catch-up-bookkeeping"
  ) {
    var dest = sitePrefix() + "virtual-bookkeeping/fit-check/";
    if (interest === "catch-up-bookkeeping") dest += "?intent=catch-up";
    window.location.replace(dest);
    return;
  }

  initRequestForm(interest);
  initBookkeepingForm(params);

  function sitePrefix() {
    var parts = window.location.pathname.split("/").filter(Boolean);
    if (parts.length && parts[parts.length - 1].indexOf(".") !== -1) parts.pop();
    var prefix = "";
    for (var i = 0; i < parts.length; i++) prefix += "../";
    return prefix || "./";
  }

  function track(eventName, payload) {
    if (!eventName) return;
    var paramsObj = payload || {};
    try {
      if (window.dataLayer && typeof window.dataLayer.push === "function") {
        var entry = { event: eventName };
        Object.keys(paramsObj).forEach(function (key) {
          entry[key] = paramsObj[key];
        });
        window.dataLayer.push(entry);
      }
      if (typeof window.gtag === "function") window.gtag("event", eventName, paramsObj);
      if (typeof window.plausible === "function") {
        window.plausible(eventName, { props: paramsObj });
      }
    } catch (err) {
      /* Analytics is optional. A missing or broken provider must not block the form. */
    }
  }

  function initRequestForm(interestValue) {
    var form = document.getElementById("request-form");
    if (!form) return;

    var interestInput = document.getElementById("interest");
    if (interestInput && interestValue) interestInput.value = interestValue;
    if (interestValue) {
      var tools = document.getElementById("tools");
      if (tools) tools.required = false;
      var subject = form.querySelector('[name="_subject"]');
      if (subject) subject.value = "Meridian inquiry: " + interestValue;
    }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var success = document.getElementById("form-success");
      var submitBtn = form.querySelector('[type="submit"]');
      var data = new FormData(form);
      var endpoint = form.getAttribute("data-formspree") || "";

      var ack = form.querySelector("#secrets-ack");
      if (ack && !ack.checked) {
        alert("Please confirm you have not pasted secrets, API keys, or credentials.");
        return;
      }

      function showSuccess() {
        if (success) {
          success.classList.add("show");
          success.scrollIntoView({ behavior: "smooth", block: "nearest" });
        }
        form.reset();
        if (submitBtn) submitBtn.disabled = false;
      }

      if (endpoint && endpoint.indexOf("YOUR_FORM_ID") === -1) {
        if (submitBtn) submitBtn.disabled = true;
        fetch(endpoint, {
          method: "POST",
          body: data,
          headers: { Accept: "application/json" },
        })
          .then(function (res) {
            if (res.ok) showSuccess();
            else throw new Error("Form error");
          })
          .catch(function () {
            mailtoFallback(data);
            showSuccess();
          });
      } else {
        mailtoFallback(data);
        showSuccess();
      }
    });

    function mailtoFallback(data) {
      var name = data.get("name") || "";
      var email = data.get("email") || "";
      var company = data.get("company") || "";
      var tools = data.get("tools") || "";
      var problem = data.get("problem") || "";
      var repo = data.get("repo") || "";
      var interestField = data.get("interest") || "";
      var body =
        "Name: " +
        name +
        "\nEmail: " +
        email +
        "\nCompany: " +
        company +
        "\nInterest: " +
        interestField +
        "\nTools: " +
        tools +
        "\nRepo (optional): " +
        repo +
        "\n\nProblem:\n" +
        problem;
      var subject = interestField
        ? "Meridian inquiry: " + interestField
        : "Vibe Code Rescue diagnostic request";
      window.location.href =
        "mailto:hello@meridian.dev?subject=" +
        encodeURIComponent(subject) +
        "&body=" +
        encodeURIComponent(body);
    }
  }

  function initBookkeepingForm(query) {
    var form = document.getElementById("bookkeeping-fit-form");
    if (!form) return;

    var behindMap = {
      current: "Current",
      "1-3": "1-3 months",
      "3-plus": "3+ months",
    };
    var softwareMap = {
      qbo: "QuickBooks Online",
      xero: "Xero",
      spreadsheets: "Spreadsheets",
      other: "Other",
    };

    var inquiry = document.getElementById("bk-inquiry");
    var source = document.getElementById("bk-source");
    var behind = document.getElementById("bk-behind");
    var software = document.getElementById("bk-software");
    var deadline = document.getElementById("bk-deadline");
    var otherWrap = document.getElementById("bk-deadline-other-wrap");
    var otherInput = document.getElementById("bk-deadline-detail");
    var catchupNote = document.getElementById("catchup-note");

    if (query.get("intent") === "catch-up") {
      if (inquiry) inquiry.value = "Catch-up quote";
      if (source && !query.get("source")) source.value = "catch-up";
      if (catchupNote) catchupNote.hidden = false;
    }

    var sourceParam = query.get("source") || "";
    if (source && /^[a-z0-9-]{1,40}$/i.test(sourceParam)) source.value = sourceParam;

    if (behind && behindMap[query.get("behind")]) behind.value = behindMap[query.get("behind")];
    if (software && softwareMap[query.get("software")]) software.value = softwareMap[query.get("software")];

    function syncDeadline() {
      var isOther = deadline && deadline.value === "Other";
      if (otherWrap) otherWrap.hidden = !isOther;
      if (otherInput) {
        if (isOther) otherInput.setAttribute("required", "required");
        else {
          otherInput.removeAttribute("required");
          otherInput.value = "";
          clearField(otherInput);
        }
      }
    }

    if (deadline) deadline.addEventListener("change", syncDeadline);
    syncDeadline();

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var errors = validateBookkeepingForm(form, otherInput);
      var errorBox = document.getElementById("books-form-errors");
      if (errors.length) {
        if (errorBox) {
          errorBox.textContent = "";
          var list = document.createElement("ul");
          errors.forEach(function (message) {
            var item = document.createElement("li");
            item.textContent = message;
            list.appendChild(item);
          });
          errorBox.appendChild(list);
          errorBox.classList.add("show");
          errorBox.scrollIntoView({ behavior: "smooth", block: "nearest" });
        }
        return;
      }
      if (errorBox) {
        errorBox.textContent = "";
        errorBox.classList.remove("show");
      }

      var email = (form.querySelector("#bk-email") || {}).value || "";
      var reply = document.getElementById("bk-replyto");
      if (reply) reply.value = email.trim();
      var data = new FormData(form);
      var endpoint = form.getAttribute("data-formspree") || "";
      var submitBtn = form.querySelector('[type="submit"]');
      var configured =
        endpoint &&
        endpoint.indexOf("YOUR_BOOKKEEPING_FORM_ID") === -1 &&
        endpoint.indexOf("YOUR_FORM_ID") === -1;

      var eventPayload = {
        inquiry: data.get("inquiry") || "",
        source: data.get("source") || "",
        software: data.get("software") || "",
        behind: data.get("behind") || "",
        need: data.get("need") || "",
        transactions: data.get("transactions") || "",
        deadline: data.get("deadline") || "",
        delivery: configured ? "formspree" : "mailto",
      };

      function showSuccess(viaMailto) {
        var success = document.getElementById("books-form-success");
        var delivery = document.getElementById("books-form-delivery");
        var card = document.getElementById("books-form-card");
        if (delivery) {
          if (viaMailto) {
            delivery.hidden = false;
            delivery.textContent =
              "A Formspree form id is not configured yet (YOUR_BOOKKEEPING_FORM_ID), so this page cannot deliver email on its own. Your email app should open a draft to hello@meridian.dev. Send that draft to complete the request.";
          } else {
            delivery.hidden = true;
            delivery.textContent = "";
          }
        }
        if (card) card.hidden = true;
        if (success) {
          success.classList.add("show");
          success.focus();
          success.scrollIntoView({ behavior: "smooth", block: "nearest" });
        }
        if (submitBtn) submitBtn.disabled = false;
      }

      if (configured) {
        if (submitBtn) submitBtn.disabled = true;
        fetch(endpoint, {
          method: "POST",
          body: data,
          headers: { Accept: "application/json" },
        })
          .then(function (res) {
            if (!res.ok) throw new Error("Form error");
            track("bookkeeping_fit_check_submit", eventPayload);
            showSuccess(false);
          })
          .catch(function () {
            eventPayload.delivery = "mailto_fallback";
            track("bookkeeping_fit_check_submit", eventPayload);
            booksMailto(data);
            showSuccess(true);
          });
      } else {
        track("bookkeeping_fit_check_submit", eventPayload);
        booksMailto(data);
        showSuccess(true);
      }
    });

    function booksMailto(data) {
      var lines = [
        ["Name", "name"],
        ["Email", "email"],
        ["Business / industry", "business"],
        ["Approx monthly transactions", "transactions"],
        ["Current software", "software"],
        ["How far behind", "behind"],
        ["Need", "need"],
        ["Deadline", "deadline"],
        ["Deadline detail", "deadline_detail"],
        ["Inquiry", "inquiry"],
        ["Source", "source"],
        ["Anything else", "notes"],
      ].map(function (pair) {
        return pair[0] + ": " + (data.get(pair[1]) || "");
      });
      window.location.href =
        "mailto:hello@meridian.dev?subject=" +
        encodeURIComponent("Meridian bookkeeping fit check") +
        "&body=" +
        encodeURIComponent(lines.join("\n"));
    }
  }

  function clearField(input) {
    if (!input) return;
    input.classList.remove("invalid");
    input.removeAttribute("aria-invalid");
    var slot = document.getElementById(input.id + "-error");
    if (slot) slot.textContent = "";
  }

  function setFieldError(input, message) {
    if (!input) return message;
    input.classList.add("invalid");
    input.setAttribute("aria-invalid", "true");
    var slot = document.getElementById(input.id + "-error");
    if (slot) slot.textContent = message;
    return message;
  }

  function validateBookkeepingForm(form, otherInput) {
    var messages = [];
    var firstInvalid = null;

    function check(id, message, ok) {
      var input = form.querySelector("#" + id);
      if (!input) return;
      if (ok) {
        clearField(input);
        return;
      }
      setFieldError(input, message);
      messages.push(message);
      if (!firstInvalid) firstInvalid = input;
    }

    var name = valueOf(form, "bk-name");
    var email = valueOf(form, "bk-email");
    var business = valueOf(form, "bk-business");
    var transactions = valueOf(form, "bk-transactions");
    var software = valueOf(form, "bk-software");
    var behind = valueOf(form, "bk-behind");
    var need = valueOf(form, "bk-need");
    var deadline = valueOf(form, "bk-deadline");
    var detail = otherInput ? otherInput.value.trim() : "";

    check("bk-name", "Enter your name.", name.length > 0);
    check("bk-email", "Enter a valid email address.", /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email));
    check("bk-business", "Enter the business or industry.", business.length > 0);
    check("bk-transactions", "Choose a transaction band.", transactions.length > 0);
    check("bk-software", "Choose the current software.", software.length > 0);
    check("bk-behind", "Say how far behind the books are.", behind.length > 0);
    check("bk-need", "Choose books only, or books and admin.", need.length > 0);
    check("bk-deadline", "Choose a deadline, or None.", deadline.length > 0);
    if (deadline === "Other") {
      check("bk-deadline-detail", "Tell us the deadline in a few words.", detail.length > 1);
    } else if (otherInput) {
      clearField(otherInput);
    }

    if (firstInvalid && typeof firstInvalid.focus === "function") firstInvalid.focus();
    return messages;
  }

  function valueOf(form, id) {
    var input = form.querySelector("#" + id);
    return input ? String(input.value || "").trim() : "";
  }
})();
