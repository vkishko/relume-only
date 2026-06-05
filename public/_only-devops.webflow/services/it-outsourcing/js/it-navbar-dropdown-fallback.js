/* navbar10 mega-dropdown inside navbar11 (IT page). */
(function () {
  var menu = null;
  var listObserver = null;
  var ignoreOutsideClick = false;
  var closeTimer = null;
  var CLOSE_DELAY_MS = 280;
  var desktopMq = window.matchMedia("(min-width: 1200px)");

  function listEl() {
    if (!menu) return null;
    return (
      menu.querySelector(".navbar10_dropdown-list") ||
      menu.querySelector(".navbar11_dropdown-list")
    );
  }

  function toggleEl() {
    if (!menu) return null;
    return (
      menu.querySelector(".navbar10_dropdown-toggle") ||
      menu.querySelector(".navbar11_dropdown-toggle")
    );
  }

  function chevronSvg() {
    var toggle = toggleEl();
    return toggle ? toggle.querySelector(".dropdown-chevron svg") : null;
  }

  function isInsideDropdown(target) {
    if (!target || !target.closest) return false;
    return !!(
      target.closest(".navbar10_menu-dropdown") ||
      target.closest(".navbar11_menu-dropdown") ||
      target.closest(".navbar10_dropdown-list") ||
      target.closest(".navbar11_dropdown-list")
    );
  }

  function isDropdownOpen() {
    var list = listEl();
    return !!(list && list.classList.contains("w--open"));
  }

  function clearCloseTimer() {
    if (closeTimer) {
      window.clearTimeout(closeTimer);
      closeTimer = null;
    }
  }

  function scheduleClose() {
    clearCloseTimer();
    closeTimer = window.setTimeout(closeDropdowns, CLOSE_DELAY_MS);
  }

  function setChevronSvg(isOpen) {
    var svg = chevronSvg();
    if (!svg) return;
    if (isOpen) {
      svg.style.setProperty("transform", "rotate(180deg)", "important");
      svg.style.setProperty("transition", "transform 0.2s ease", "important");
    } else {
      svg.style.removeProperty("transform");
      svg.style.removeProperty("transition");
    }
  }

  function setListOpen(list, isOpen) {
    if (!list) return;
    if (isOpen) {
      list.classList.add("w--open");
    } else {
      list.classList.remove("w--open");
    }
  }

  function setToggleOpen(toggle, isOpen) {
    if (!toggle) return;
    if (isOpen) {
      toggle.classList.add("w--open", "w--nav-dropdown-toggle-open");
      toggle.setAttribute("aria-expanded", "true");
    } else {
      toggle.classList.remove("w--open", "w--nav-dropdown-toggle-open");
      toggle.setAttribute("aria-expanded", "false");
    }
    setChevronSvg(isOpen);
  }

  function syncOpenStateFromDom() {
    var list = listEl();
    var toggle = toggleEl();
    if (!list || !toggle) return;
    var open = list.classList.contains("w--open");
    if (open) {
      menu.classList.add("w--open");
      setToggleOpen(toggle, true);
    } else {
      menu.classList.remove("w--open");
      setToggleOpen(toggle, false);
    }
  }

  function closeDropdowns() {
    clearCloseTimer();
    if (!menu) return;
    menu.classList.remove("w--open");
    setListOpen(listEl(), false);
    setToggleOpen(toggleEl(), false);
  }

  function openDropdown() {
    if (!menu) return;
    clearCloseTimer();
    menu.classList.add("w--open");
    setListOpen(listEl(), true);
    setToggleOpen(toggleEl(), true);
  }

  function toggleDropdown() {
    if (!menu) return;
    if (isDropdownOpen()) {
      closeDropdowns();
    } else {
      openDropdown();
    }
  }

  function onHoverEnter() {
    if (!desktopMq.matches) return;
    openDropdown();
  }

  function onHoverLeave(e) {
    if (!desktopMq.matches) return;
    var related = e.relatedTarget;
    if (related && isInsideDropdown(related)) return;
    scheduleClose();
  }

  function onToggleActivate(e) {
    var toggle = e.target.closest(
      ".navbar10_dropdown-toggle, .navbar11_dropdown-toggle"
    );
    if (!toggle || !menu.contains(toggle)) return;

    if (desktopMq.matches) {
      e.preventDefault();
      e.stopPropagation();
      ignoreOutsideClick = true;
      toggleDropdown();
      window.setTimeout(function () {
        ignoreOutsideClick = false;
      }, 0);
      return;
    }

    ignoreOutsideClick = true;
    window.setTimeout(function () {
      syncOpenStateFromDom();
      ignoreOutsideClick = false;
    }, 0);
    window.setTimeout(syncOpenStateFromDom, 50);
    window.setTimeout(syncOpenStateFromDom, 400);
  }

  function bindDesktopHover() {
    var list = listEl();
    if (!list) return;
    menu.addEventListener("mouseenter", onHoverEnter);
    menu.addEventListener("mouseleave", onHoverLeave);
    list.addEventListener("mouseenter", onHoverEnter);
    list.addEventListener("mouseleave", onHoverLeave);
  }

  function unbindDesktopHover() {
    var list = listEl();
    menu.removeEventListener("mouseenter", onHoverEnter);
    menu.removeEventListener("mouseleave", onHoverLeave);
    if (list) {
      list.removeEventListener("mouseenter", onHoverEnter);
      list.removeEventListener("mouseleave", onHoverLeave);
    }
  }

  function observeList() {
    var list = listEl();
    if (!list || listObserver) return;
    listObserver = new MutationObserver(syncOpenStateFromDom);
    listObserver.observe(list, {
      attributes: true,
      attributeFilter: ["class"],
    });
  }

  function init() {
    menu =
      document.querySelector(".navbar10_menu-dropdown.w-dropdown") ||
      document.querySelector(".navbar11_menu-dropdown.w-dropdown");
    if (!menu) return;

    closeDropdowns();

    menu.addEventListener("click", onToggleActivate, true);
    menu.addEventListener(
      "keydown",
      function (e) {
        if (e.key === "Enter" || e.key === " ") {
          onToggleActivate(e);
        }
      },
      true
    );

    observeList();

    if (desktopMq.matches) {
      bindDesktopHover();
    }

    desktopMq.addEventListener("change", function () {
      unbindDesktopHover();
      closeDropdowns();
      if (desktopMq.matches) {
        bindDesktopHover();
      }
    });

    document.addEventListener(
      "click",
      function (e) {
        if (ignoreOutsideClick) return;
        if (isInsideDropdown(e.target)) return;
        closeDropdowns();
      },
      true
    );

    window.setTimeout(closeDropdowns, 400);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      window.setTimeout(init, 100);
    });
  } else {
    window.setTimeout(init, 100);
  }
})();
