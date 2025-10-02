import { ref, mergeProps, unref, useSSRContext } from "vue";
import { ssrRenderAttrs, ssrRenderAttr, ssrRenderClass } from "vue/server-renderer";
import { _ as _imports_0 } from "./virtual_public-CEu87jeG.js";
import { _ as _export_sfc } from "../server.mjs";
const _sfc_main = {
  __name: "HeaderSection",
  __ssrInlineRender: true,
  setup(__props) {
    const mobileMenuOpen = ref(false);
    return (_ctx, _push, _parent, _attrs) => {
      _push(`<header${ssrRenderAttrs(mergeProps({ class: "header" }, _attrs))} data-v-927877b9><div class="header-container" data-v-927877b9><div class="header-left" data-v-927877b9><div class="logo" data-v-927877b9><img${ssrRenderAttr("src", _imports_0)} alt="Calories Bot" class="logo-icon" loading="eager" data-v-927877b9><span class="logo-text" data-v-927877b9>Calories Bot</span></div></div><nav class="header-nav" data-v-927877b9><a href="/#features" class="nav-link" data-v-927877b9>Возможности</a><a href="/#how-it-works" class="nav-link" data-v-927877b9>Как работает</a><a href="/#pricing" class="nav-link" data-v-927877b9>Цены</a><a href="/blog" class="nav-link" data-v-927877b9>Блог</a><a href="/#faq" class="nav-link" data-v-927877b9>FAQ</a><a href="/privacy" class="nav-link" data-v-927877b9>Конфиденциальность</a></nav><div class="header-right" data-v-927877b9><a href="https://t.me/caloriesnote_bot" class="btn-start-growing" data-v-927877b9> Запустить бота </a></div><button class="mobile-menu-btn" data-v-927877b9><span class="hamburger-line" data-v-927877b9></span><span class="hamburger-line" data-v-927877b9></span><span class="hamburger-line" data-v-927877b9></span></button></div><div class="${ssrRenderClass([{ "mobile-menu--open": unref(mobileMenuOpen) }, "mobile-menu"])}" data-v-927877b9><nav class="mobile-nav" data-v-927877b9><a href="/#features" class="mobile-nav-link" data-v-927877b9>Возможности</a><a href="/#how-it-works" class="mobile-nav-link" data-v-927877b9>Как работает</a><a href="/#pricing" class="mobile-nav-link" data-v-927877b9>Цены</a><a href="/blog" class="mobile-nav-link" data-v-927877b9>Блог</a><a href="/#faq" class="mobile-nav-link" data-v-927877b9>FAQ</a><a href="/privacy" class="mobile-nav-link" data-v-927877b9>Конфиденциальность</a></nav><div class="mobile-buttons" data-v-927877b9><a href="https://t.me/caloriesnote_bot" class="btn-start-growing w-full" data-v-927877b9> Запустить бота </a></div></div></header>`);
    };
  }
};
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("components/HeaderSection.vue");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const __nuxt_component_0 = /* @__PURE__ */ _export_sfc(_sfc_main, [["__scopeId", "data-v-927877b9"]]);
export {
  __nuxt_component_0 as _
};
//# sourceMappingURL=HeaderSection-Bskbvj7i.js.map
