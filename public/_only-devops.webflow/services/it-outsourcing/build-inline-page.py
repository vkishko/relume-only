#!/usr/bin/env python3
"""Regenerate services/it-outsourcing/index.html — hybrid CSS + navbar11 + IT mega dropdown."""
import re
from pathlib import Path

base = Path(__file__).resolve().parents[2]
it_dir = Path(__file__).resolve().parent
index_path = base / "index.html"
untitled_path = it_dir / "untitled.html"
devops_path = base / "services" / "devops-2.html"
out_path = it_dir / "index.html"

MAIN_SITE_ID = "69fa2db34a07dabdc28b9a9c"
IT_SITE_ID = "6a11c687b27411cca96dfd66"
IT_PAGE_ID = "6a11c71cd2ea2cb28a3f295a"

index_lines = index_path.read_text(encoding="utf-8").splitlines()
untitled_lines = untitled_path.read_text(encoding="utf-8").splitlines()
devops_lines = devops_path.read_text(encoding="utf-8").splitlines()

global_styles_block = "\n".join(devops_lines[26:257])

ix_style = untitled_lines[12].strip()
if ix_style.startswith("<style>") and ix_style.endswith("</style>"):
    ix_style = ix_style[7:-8]

# navbar11 shell from index.html (logo, links, buttons)
navbar_html = "\n".join(index_lines[756:817]).replace(
    'src="images/relume-914021.png"', 'src="../../images/relume-914021.png"'
)

# Mega dropdown from IT export (navbar10) — cards with images, works with js/webflow.js
navbar10_dropdown = "\n".join(untitled_lines[34:150])
navbar10_dropdown = navbar10_dropdown.replace(
    "<div>Resources</div>", "<div>Услуги и решения</div>", 1
)
navbar10_dropdown = navbar10_dropdown.replace('data-hover="true"', 'data-hover="false"', 1)

# Swap navbar11 simple dropdown for IT mega menu
navbar_html = re.sub(
    r'<div data-delay="200" data-hover="true" class="navbar11_menu-dropdown w-dropdown">.*?</div>(?=\s*<a href="#" class="navbar11_link)',
    navbar10_dropdown.strip(),
    navbar_html,
    count=1,
    flags=re.DOTALL,
)

navbar_css = "\n".join(index_lines[329:648])
navbar_css = navbar_css.replace(
    "transition: transform 0.25s ease",
    "transition: transform 0.2s ease",
)
navbar_css = navbar_css.replace(
    "transform: rotate(180deg);",
    "transform: rotate(180deg) !important;",
)

it_main = "\n".join(untitled_lines[167:1243])

footer_html = "\n".join(index_lines[1241:1298]).replace(
    'src="images/relume-914021.png"', 'src="../../images/relume-914021.png"'
)

navbar_dropdown_css = """
  /* === IT-аутсорсинг: тёмный HERO с синим фоном === */
  .it-hero-dark {
    background-color: #051133 !important;
  }
  .it-hero-dark .heading-style-h1,
  .it-hero-dark h1 {
    color: #fff !important;
    -webkit-text-fill-color: #fff !important;
  }
  .it-hero-dark .text-size-medium,
  .it-hero-dark p {
    color: rgba(255,255,255,0.82) !important;
    -webkit-text-fill-color: rgba(255,255,255,0.82) !important;
  }
  .it-hero-dark .button.is-secondary.is-alternate {
    background-color: transparent !important;
    border-color: rgba(255,255,255,0.5) !important;
    color: #fff !important;
  }
  .it-hero-dark .button.is-secondary.is-alternate:hover {
    background-color: rgba(255,255,255,0.1) !important;
    border-color: #fff !important;
  }
  .it-hero-dark .home_header-1_image-wrapper {
    border-radius: 1rem;
    overflow: hidden;
  }
  .it-hero-dark .home_header-1_image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
    border-radius: 1rem;
  }
  @media screen and (min-width: 992px) {
    .it-hero-dark .home_header-1_content {
      grid-template-columns: 1fr 1fr;
      grid-template-rows: auto auto;
      grid-template-areas:
        "hero-text hero-image"
        "hero-actions hero-image";
      align-items: start;
    }
    .it-hero-dark .home_header-1_content-left {
      grid-area: hero-text;
    }
    .it-hero-dark .home_header-1_image-wrapper {
      grid-area: hero-image;
      grid-row: 1 / span 2;
      align-self: center;
    }
    .it-hero-dark .home_header-1_image {
      object-position: 25% 50%;
    }
    .it-hero-dark .home_header-1_actions {
      grid-area: hero-actions;
    }
  }
  @media screen and (max-width: 991px) {
    .it-hero-dark .home_header-1_content {
      grid-template-columns: 1fr;
      grid-row-gap: 1.5rem;
    }
    .it-hero-dark .home_header-1_image {
      aspect-ratio: 16 / 9;
    }
    .it-hero-dark .home_header-1_actions .button-group {
      flex-direction: column;
      align-items: stretch;
      width: 100%;
    }
    .it-hero-dark .home_header-1_actions .button {
      width: 100%;
      text-align: center;
    }
  }

  /* Закрытое мегаменю не должно перехватывать клики (IX/Webflow оставляют opacity:0) */
  .navbar11_component .navbar10_dropdown-list.w-dropdown-list:not(.w--open):not(.w--nav-dropdown-list-open),
  .navbar11_component [data-w-id="cf535bf3-c510-52ea-83b5-bf28a0809eb8"]:not(.w--open) {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
    height: 0 !important;
    max-height: 0 !important;
    overflow: hidden !important;
  }
  /* navbar10 mega-menu внутри navbar11 — общее */
  .navbar11_component .navbar10_menu-dropdown {
    position: static;
  }
  /* Webflow IX крутит .dropdown-chevron — сброс, чтобы не суммировалось с поворотом svg */
  .navbar11_component .navbar10_dropdown-toggle .dropdown-chevron,
  .navbar11_component .navbar10_menu-dropdown.w--open .navbar10_dropdown-toggle .dropdown-chevron,
  .navbar11_component .navbar10_dropdown-toggle.w--open .dropdown-chevron,
  .navbar11_component .navbar10_dropdown-toggle.w--nav-dropdown-toggle-open .dropdown-chevron,
  .navbar11_component .navbar10_dropdown-toggle[aria-expanded="true"] .dropdown-chevron {
    transform: none !important;
    transition: none !important;
  }
  .navbar11_component .navbar10_dropdown-toggle .dropdown-chevron svg,
  .navbar11_component .navbar11_dropdown-toggle .dropdown-chevron svg {
    transition: transform 0.2s ease;
    transform: rotate(0deg);
    transform-origin: center center;
    display: block;
  }
  .navbar11_component .navbar10_menu-dropdown:has(.navbar10_dropdown-list.w--open) .navbar10_dropdown-toggle .dropdown-chevron svg,
  .navbar11_component .navbar10_menu-dropdown.w--open .navbar10_dropdown-toggle .dropdown-chevron svg,
  .navbar11_component .navbar10_dropdown-toggle.w--open .dropdown-chevron svg,
  .navbar11_component .navbar10_dropdown-toggle.w--nav-dropdown-toggle-open .dropdown-chevron svg,
  .navbar11_component .navbar10_dropdown-toggle[aria-expanded="true"] .dropdown-chevron svg,
  .navbar11_component .navbar11_menu-dropdown:has(.navbar11_dropdown-list.w--open) .navbar11_dropdown-toggle .dropdown-chevron svg,
  .navbar11_component .navbar11_menu-dropdown.w--open .navbar11_dropdown-toggle .dropdown-chevron svg,
  .navbar11_component .navbar11_dropdown-toggle.w--open .dropdown-chevron svg,
  .navbar11_component .navbar11_dropdown-toggle[aria-expanded="true"] .dropdown-chevron svg {
    transform: rotate(180deg) !important;
  }
  .navbar11_component .navbar10_dropdown-list .navbar10_container {
    width: 100%;
    max-width: none;
    padding-left: 0;
    padding-right: 0;
  }
  .navbar11_component .navbar10_blog-item {
    align-items: stretch;
  }
  .navbar11_component .navbar10_blog-item-image-wrapper {
    flex: 0 0 22.5rem;
    width: 22.5rem;
    min-width: 22.5rem;
    max-width: 22.5rem;
    height: auto;
    align-self: flex-start;
  }
  .navbar11_component .navbar10_blog-item-image {
    aspect-ratio: 16 / 9;
    width: 100%;
    height: auto;
    object-fit: cover;
    display: block;
  }
  .navbar11_component .navbar10_blog-item-content {
    flex: 1 1 auto;
    min-width: 0;
  }
  /* Логотип: webflow .w-nav-brand { float:left } ломает вертикальное выравнивание в flex-шапке */
  .navbar11_component .navbar11_logo-link.w-nav-brand {
    display: flex;
    align-items: center;
    align-self: center;
    float: none;
    padding-left: 0 !important;
    line-height: 0;
  }
  .navbar11_component .navbar11_logo {
    display: block;
    height: 36px;
    width: auto;
    max-height: 36px;
  }
  .navbar11_component .navbar11_menu-button {
    align-self: center;
  }
  .navbar11_component.w-nav,
  .navbar11_component .navbar11_container,
  .page-wrapper {
    overflow: visible;
  }

  /* Desktop */
  @media screen and (min-width: 1200px) {
    .navbar11_component .navbar11_menu-links {
      display: flex;
      align-items: center;
      flex-wrap: nowrap;
    }
    .navbar11_component .navbar11_menu {
      flex: 1;
      justify-content: flex-end;
      align-items: center;
    }
    .navbar11_component .navbar11_container,
    .navbar11_component .w-nav-menu,
    .navbar11_component .navbar11_menu {
      align-items: center;
    }
    .navbar11_component .navbar11_container {
      min-height: 4.5rem;
    }
    .navbar11_component .navbar10_dropdown-toggle {
      padding: .5rem 1rem;
      align-items: center;
      display: flex;
    }
    .navbar11_component .navbar10_dropdown-list {
      position: absolute;
      display: none !important;
      pointer-events: none !important;
      visibility: hidden !important;
    }
    .navbar11_component .navbar10_dropdown-list.w--open,
    .navbar11_component .navbar10_menu-dropdown.w--open .navbar10_dropdown-list {
      position: fixed;
      left: 0;
      right: 0;
      top: 4.5rem;
      width: 100vw;
      max-width: 100vw;
      margin-left: 0;
      padding-left: 5%;
      padding-right: 5%;
      box-sizing: border-box;
      z-index: 998;
      display: block !important;
      visibility: visible !important;
      opacity: 1 !important;
      height: auto !important;
      max-height: none !important;
      pointer-events: auto !important;
      overflow: visible !important;
      border-bottom: 1px solid rgba(255,255,255,0.22);
      background-color: #051133 !important;
      color: #fff !important;
    }
    .navbar11_component .navbar10_menu-dropdown.w--open .navbar10_dropdown-toggle .dropdown-chevron svg,
    .navbar11_component .navbar10_dropdown-toggle.w--open .dropdown-chevron svg,
    .navbar11_component .navbar10_dropdown-toggle.w--nav-dropdown-toggle-open .dropdown-chevron svg,
    .navbar11_component .navbar10_dropdown-toggle[aria-expanded="true"] .dropdown-chevron svg {
      transform: rotate(180deg);
    }
  }

  /* Mobile / tablet — как navbar11 на index.html */
  @media screen and (max-width: 1199px) {
    /* iPad/tablet: Webflow иногда красит текст через -webkit-text-fill-color */
    .navbar11_component.color-scheme-4.w-nav .w-nav-menu[data-nav-menu-open],
    .navbar11_component.color-scheme-4.w-nav .w-nav-menu[data-nav-menu-open] * {
      color: #fff !important;
      -webkit-text-fill-color: #fff !important;
    }
    .navbar11_component.color-scheme-4.w-nav .w-nav-menu[data-nav-menu-open] .text-size-small {
      color: rgba(255,255,255,0.78) !important;
      -webkit-text-fill-color: rgba(255,255,255,0.78) !important;
    }
    .navbar11_component.color-scheme-4.w-nav .w-nav-menu[data-nav-menu-open] .dropdown-chevron svg,
    .navbar11_component.color-scheme-4.w-nav .w-nav-menu[data-nav-menu-open] .dropdown-chevron svg path {
      color: #fff !important;
      fill: currentColor !important;
    }

    .navbar11_component .navbar11_menu-links {
      display: flex;
      flex-direction: column !important;
      align-items: stretch;
      flex-wrap: nowrap;
      width: 100%;
    }
    .navbar11_component .navbar11_menu,
    .navbar11_component .w-nav-menu {
      align-items: stretch !important;
    }
    .navbar11_component .navbar11_container {
      align-items: center !important;
    }
    .navbar11_component .navbar10_menu-dropdown {
      width: 100%;
      font-size: 1.125rem;
    }
    .navbar11_component .navbar10_dropdown-toggle {
      width: 100%;
      justify-content: space-between;
      padding: .75rem 0;
      font-size: 1.125rem;
      display: flex !important;
    }
    .navbar11_component .navbar10_dropdown-toggle .dropdown-chevron {
      position: static !important;
      inset: auto !important;
      flex: none;
      flex-shrink: 0;
      margin-left: auto !important;
    }
    .navbar11_component .navbar10_menu-dropdown:has(.navbar10_dropdown-list.w--open) .navbar10_dropdown-toggle .dropdown-chevron svg,
    .navbar11_component .navbar10_dropdown-toggle[aria-expanded="true"] .dropdown-chevron svg,
    .navbar11_component .navbar10_menu-dropdown.w--open .navbar10_dropdown-toggle .dropdown-chevron svg,
    .navbar11_component .navbar10_dropdown-toggle.w--open .dropdown-chevron svg,
    .navbar11_component .navbar10_dropdown-toggle.w--nav-dropdown-toggle-open .dropdown-chevron svg {
      transform: rotate(180deg) !important;
    }
    .navbar11_component .navbar10_dropdown-list {
      position: static !important;
      top: auto !important;
      left: auto !important;
      right: auto !important;
      width: 100% !important;
      max-width: 100% !important;
      margin-left: 0 !important;
      padding-left: 0 !important;
      padding-right: 0 !important;
      z-index: auto;
      overflow: hidden;
    }
    .navbar11_component .navbar10_dropdown-list.w--open {
      display: block !important;
      visibility: visible !important;
      opacity: 1 !important;
      height: auto !important;
      border-style: none;
      background-color: transparent !important;
      padding: 0;
    }
    .navbar11_component .navbar10_dropdown-content {
      flex-direction: column;
      width: 100%;
    }
    .navbar11_component .navbar10_dropdown-content-left,
    .navbar11_component .navbar10_dropdown-content-right {
      max-width: none;
      width: 100%;
      padding-left: 0;
      padding-right: 0;
    }
    .navbar11_component .navbar10_blog-list {
      grid-template-columns: 1fr;
      grid-row-gap: 1.5rem;
      width: 100%;
    }
    .navbar11_component .navbar10_blog-item {
      grid-template-columns: 1fr;
      grid-row-gap: .75rem;
      flex-direction: column;
      align-items: stretch;
    }
    .navbar11_component .navbar10_blog-item-image-wrapper {
      flex: 0 0 auto;
      width: 100%;
      min-width: 0;
      max-width: none;
    }
    .navbar11_component .navbar10_blog-item-image,
    .navbar11_component .navbar10_blog-item-content {
      width: 100%;
    }
    .navbar11_component .navbar10_dropdown-link-list {
      padding-top: .5rem;
      padding-bottom: .5rem;
    }
    /* Webflow IX: не схлопывать панель в бургер-меню — только когда открыта */
    .navbar11_component .navbar10_dropdown-list.w--open,
    .navbar11_component .navbar10_menu-dropdown:has(.navbar10_dropdown-list.w--open) .navbar10_dropdown-list {
      height: auto !important;
      max-height: none !important;
      opacity: 1 !important;
      pointer-events: auto !important;
    }
    .navbar11_component .navbar10_dropdown-list:not(.w--open) {
      display: none !important;
      visibility: hidden !important;
      opacity: 0 !important;
      pointer-events: none !important;
      height: 0 !important;
      overflow: hidden !important;
    }
    /* webflow.css: .w-nav-link { margin-left/right: auto } — ломает выравнивание в бургере */
    .navbar11_component .navbar11_menu-links > .navbar11_link.w-nav-link,
    .navbar11_component .navbar11_link.w-nav-link {
      display: block;
      width: 100%;
      max-width: 100%;
      margin-left: 0 !important;
      margin-right: 0 !important;
      padding-left: 0 !important;
      padding-right: 0 !important;
      text-align: left;
      align-self: stretch;
    }
    /* global-styles: .w-nav-link { font-size: inherit } сбрасывает 1.125rem у navbar11_link */
    .navbar11_component .navbar11_link.w-nav-link,
    .navbar11_component .navbar10_dropdown-toggle,
    .navbar11_component .navbar10_dropdown-toggle > div:first-child,
    .navbar11_component .navbar11_dropdown-toggle,
    .navbar11_component .navbar11_dropdown-toggle > div:first-child {
      font-size: 1.125rem !important;
      line-height: 1.5;
    }
    .navbar11_component .navbar11_menu-buttons {
      width: 100%;
      align-self: stretch;
      padding-left: 0;
      padding-right: 0;
    }
    .navbar11_component .navbar11_menu-buttons .button {
      width: 100%;
      max-width: 100%;
      margin-left: 0;
      margin-right: 0;
      box-sizing: border-box;
    }
  }

  @media screen and (min-width: 992px) {
    .section_home_header-1 .home_header-1_content {
      align-items: center;
    }
  }
"""

# Mobile burger: navbar10 dropdown в том же блоке, что navbar11
navbar_css = navbar_css.replace(
    ".navbar11_menu-links,\n    .navbar11_menu-dropdown {",
    ".navbar11_menu-links,\n    .navbar11_menu-dropdown,\n    .navbar11_menu-links .navbar10_menu-dropdown {",
)
navbar_css = navbar_css.replace(
    ".navbar11_component .navbar11_dropdown-toggle {",
    ".navbar11_component .navbar11_dropdown-toggle,\n    .navbar11_component .navbar10_dropdown-toggle {",
    1,
)
navbar_css = navbar_css.replace(
    ".navbar11_dropdown-list {",
    ".navbar11_dropdown-list,\n    .navbar11_component .navbar10_dropdown-list {",
    1,
)
navbar_css = navbar_css.replace(
    ".navbar11_dropdown-list.w--open {",
    ".navbar11_dropdown-list.w--open,\n    .navbar11_component .navbar10_dropdown-list.w--open {",
    1,
)
navbar_css = navbar_css.replace(
    ".navbar11_menu-dropdown {",
    ".navbar11_menu-dropdown,\n    .navbar11_component .navbar10_menu-dropdown {",
    1,
)
# Webflow открывает бургер через [data-nav-menu-open] — иначе меню остаётся display:none
navbar_css = navbar_css.replace(
    """    .navbar11_component.w-nav[data-collapse='medium'] .w-nav-menu {
      display: none;
    }
    .navbar11_component.w-nav[data-collapse='medium'] .w-nav-button {
      display: block;
    }""",
    """    .navbar11_component.w-nav[data-collapse='medium'] .w-nav-menu {
      display: none;
    }
    .navbar11_component.w-nav[data-collapse='medium'] .w-nav-menu[data-nav-menu-open] {
      display: flex !important;
      flex-direction: column;
      align-items: stretch;
      float: none;
    }
    .navbar11_component.w-nav[data-collapse='medium'] .w-nav-button {
      display: block;
    }""",
    1,
)

footer_css = """
  /* === Footer dark (from index.html) === */
  .footer3_top-wrapper {
    display: grid;
    grid-template-columns: minmax(0, 1fr) minmax(0, 1.5fr);
    grid-column-gap: 5rem;
    grid-row-gap: 3rem;
    align-items: start;
  }
  .footer3_left-wrapper {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 0;
    min-width: 0;
  }
  .footer3_logo-link { float: none; display: inline-block; padding-left: 0; }
  .footer3_logo { height: 2.25rem; width: auto; display: block; }
  .footer3_details-wrapper { display: flex; flex-direction: column; gap: 0.25rem; width: 100%; }
  .footer3_details-wrapper a { display: block; }
  .footer3_social-list { display: flex; flex-wrap: wrap; gap: 0.75rem; width: 100%; }
  .footer3_social-link { display: flex; align-items: center; justify-content: center; width: 2.25rem; height: 2.25rem; }
  .footer3_menu-wrapper {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    grid-column-gap: 2rem;
    grid-row-gap: 1rem;
    align-items: start;
    min-width: 0;
  }
  .footer3_link-list { display: flex; flex-direction: column; gap: 0.75rem; }
  .footer3_link { color: inherit !important; text-decoration: none; font-size: 0.875rem; opacity: 0.78; }
  .footer3_link:hover { opacity: 1; }
  .footer3_bottom-wrapper { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; }
  .footer3_credit-text { font-size: 0.875rem; opacity: 0.6; }
  .footer3_legal-list { display: flex; flex-wrap: wrap; gap: 1.5rem; align-items: center; }
  .footer3_legal-link { font-size: 0.875rem; color: inherit !important; opacity: 0.6; text-decoration: none; }
  .footer3_legal-link:hover { opacity: 1; }
  .divider-horizontal { height: 1px; background-color: rgba(255,255,255,0.15); width: 100%; }
  .home-v29_footer-dark { background-color: #000 !important; color: #fff !important; }
  .home-v29_footer-dark, .home-v29_footer-dark * { color: #fff !important; }
  .home-v29_footer-dark a, .home-v29_footer-dark .footer3_link, .home-v29_footer-dark .footer3_legal-link, .home-v29_footer-dark .footer3_credit-text, .home-v29_footer-dark .text-size-small { color: #fff !important; opacity: 1; }
  .home-v29_footer-dark .footer3_social-link { border-color: rgba(255,255,255,0.22) !important; }
  .home-v29_footer-dark .divider-horizontal { background-color: rgba(255,255,255,0.22) !important; }
  .home-v29_footer-dark .footer3_logo { filter: brightness(0) invert(1); }
  @media (max-width: 991px) {
    .footer3_top-wrapper { grid-template-columns: minmax(0, 1fr); grid-column-gap: 0; grid-row-gap: 3rem; }
  }
  @media (max-width: 767px) {
    .footer3_menu-wrapper { grid-template-columns: minmax(0, 1fr); }
    .footer3_bottom-wrapper { flex-direction: column; align-items: flex-start; }
    .footer3_legal-list { flex-direction: column; align-items: flex-start; gap: 0.75rem; }
  }
"""

html = f"""<!DOCTYPE html><!--
  EXPERIMENTAL HYBRID PAGE — services/it-outsourcing
  Navbar11 (шапка) — index.html; выпадающее меню — navbar10 mega-menu из untitled.html.
  Контент IT — untitled.html; CSS секций — valerys-fresh-site…css.
  Общие стили/кнопки — ../../css/only-devops.webflow.css.
  JS: js/webflow.js (IT) для dropdown; js/it-tabs-fallback.js для табов.
  Пересборка: python3 build-inline-page.py
-->
<html data-wf-page="{IT_PAGE_ID}" data-wf-site="{IT_SITE_ID}">
<head>
  <meta charset="utf-8">
  <title>IT-аутсорсинг</title>
  <meta content="IT-аутсорсинг" property="og:title">
  <meta content="IT-аутсорсинг" name="twitter:title">
  <meta content="width=device-width, initial-scale=1" name="viewport">
  <meta content="Webflow" name="generator">
  <link href="../../css/normalize.css" rel="stylesheet" type="text/css">
  <link href="../../css/webflow.css" rel="stylesheet" type="text/css">
  <link href="css/valerys-fresh-site-20beb6.webflow.css" rel="stylesheet" type="text/css">
  <link href="../../css/only-devops.webflow.css" rel="stylesheet" type="text/css">
  <style>{ix_style}</style>
  <style>
  * {{
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    -o-font-smoothing: antialiased;
  }}
{navbar_css}
{navbar_dropdown_css}
{footer_css}
  </style>
  <script type="text/javascript">!function(o,c){{var n=c.documentElement,t=" w-mod-";n.className+=t+"js",("ontouchstart"in o||o.DocumentTouch&&c instanceof DocumentTouch)&&(n.className+=t+"touch")}}(window,document);</script>
  <link href="../../images/favicon.png" rel="shortcut icon" type="image/x-icon">
  <link href="../../images/webclip.png" rel="apple-touch-icon">
</head>
<body>
  <div class="page-wrapper">
{global_styles_block}
{navbar_html}
{it_main}
{footer_html}
  </div>
  <script src="https://d3e54v103j8qbb.cloudfront.net/js/jquery-3.5.1.min.dc5e7f18c8.js?site={IT_SITE_ID}" type="text/javascript" integrity="sha256-9/aliU8dGd2tb6OSsuzixeV4y/faTqgFtohetphbbj0=" crossorigin="anonymous"></script>
  <script src="js/webflow.js" type="text/javascript"></script>
  <script src="js/it-navbar-dropdown-fallback.js?v=13" type="text/javascript"></script>
  <script src="js/it-tabs-fallback.js?v=3" type="text/javascript"></script>
</body>
</html>
"""

out_path.write_text(html, encoding="utf-8")
print(f"Written {out_path} ({len(html):,} bytes, {html.count(chr(10)) + 1} lines)")
