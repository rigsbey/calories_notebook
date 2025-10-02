import { _ as __nuxt_component_0 } from "./nuxt-link-BeVqdmom.js";
import { withCtx, createTextVNode, useSSRContext } from "vue";
import { ssrRenderAttrs, ssrRenderSlot, ssrRenderAttr, ssrRenderComponent } from "vue/server-renderer";
import { _ as _imports_0 } from "./virtual_public-CEu87jeG.js";
import { u as useHead } from "./v3-D915_2dV.js";
import { _ as _export_sfc } from "../server.mjs";
import "/Users/kamil/PycharmProjects/calories_notebook/landing/node_modules/ufo/dist/index.mjs";
import "#internal/nuxt/paths";
import "/Users/kamil/PycharmProjects/calories_notebook/landing/node_modules/@unhead/vue/dist/index.mjs";
import "ofetch";
import "/Users/kamil/PycharmProjects/calories_notebook/landing/node_modules/hookable/dist/index.mjs";
import "/Users/kamil/PycharmProjects/calories_notebook/landing/node_modules/unctx/dist/index.mjs";
import "/Users/kamil/PycharmProjects/calories_notebook/landing/node_modules/h3/dist/index.mjs";
import "vue-router";
import "/Users/kamil/PycharmProjects/calories_notebook/landing/node_modules/radix3/dist/index.mjs";
import "/Users/kamil/PycharmProjects/calories_notebook/landing/node_modules/defu/dist/defu.mjs";
const _sfc_main = {
  __name: "default",
  __ssrInlineRender: true,
  setup(__props) {
    useHead({
      htmlAttrs: {
        lang: "ru"
      },
      meta: [
        { name: "viewport", content: "width=device-width, initial-scale=1" },
        { name: "format-detection", content: "telephone=no" }
      ],
      link: [
        { rel: "preconnect", href: "https://fonts.googleapis.com" },
        { rel: "preconnect", href: "https://fonts.gstatic.com", crossorigin: "" },
        { rel: "preconnect", href: "https://t.me" },
        { rel: "stylesheet", href: "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap" },
        // Favicons
        { rel: "icon", type: "image/x-icon", href: "/favicon.ico" },
        { rel: "icon", type: "image/png", sizes: "16x16", href: "/favicon-16x16.png" },
        { rel: "icon", type: "image/png", sizes: "32x32", href: "/favicon-32x32.png" },
        { rel: "icon", type: "image/png", sizes: "96x96", href: "/favicon-96x96.png" },
        // Apple Touch Icons
        { rel: "apple-touch-icon", sizes: "57x57", href: "/apple-icon-57x57.png" },
        { rel: "apple-touch-icon", sizes: "60x60", href: "/apple-icon-60x60.png" },
        { rel: "apple-touch-icon", sizes: "72x72", href: "/apple-icon-72x72.png" },
        { rel: "apple-touch-icon", sizes: "76x76", href: "/apple-icon-76x76.png" },
        { rel: "apple-touch-icon", sizes: "114x114", href: "/apple-icon-114x114.png" },
        { rel: "apple-touch-icon", sizes: "120x120", href: "/apple-icon-120x120.png" },
        { rel: "apple-touch-icon", sizes: "144x144", href: "/apple-icon-144x144.png" },
        { rel: "apple-touch-icon", sizes: "152x152", href: "/apple-icon-152x152.png" },
        { rel: "apple-touch-icon", sizes: "180x180", href: "/apple-icon-180x180.png" },
        { rel: "apple-touch-icon", href: "/apple-icon.png" },
        { rel: "apple-touch-icon-precomposed", href: "/apple-icon-precomposed.png" },
        // Android Icons
        { rel: "icon", type: "image/png", sizes: "36x36", href: "/android-icon-36x36.png" },
        { rel: "icon", type: "image/png", sizes: "48x48", href: "/android-icon-48x48.png" },
        { rel: "icon", type: "image/png", sizes: "72x72", href: "/android-icon-72x72.png" },
        { rel: "icon", type: "image/png", sizes: "96x96", href: "/android-icon-96x96.png" },
        { rel: "icon", type: "image/png", sizes: "144x144", href: "/android-icon-144x144.png" },
        { rel: "icon", type: "image/png", sizes: "192x192", href: "/android-icon-192x192.png" },
        // Microsoft Tiles
        { rel: "msapplication-TileColor", content: "#ffffff" },
        { rel: "msapplication-TileImage", content: "/ms-icon-144x144.png" },
        { rel: "msapplication-config", content: "/browserconfig.xml" },
        // Web App Manifest
        { rel: "manifest", href: "/manifest.json" }
      ]
    });
    return (_ctx, _push, _parent, _attrs) => {
      const _component_NuxtLink = __nuxt_component_0;
      _push(`<div${ssrRenderAttrs(_attrs)} data-v-fdf84ce5><main data-v-fdf84ce5>`);
      ssrRenderSlot(_ctx.$slots, "default", {}, null, _push, _parent);
      _push(`</main><footer class="footer" data-v-fdf84ce5><div class="container" data-v-fdf84ce5><div class="footer-content" data-v-fdf84ce5><div class="footer-brand" data-v-fdf84ce5><img${ssrRenderAttr("src", _imports_0)} alt="Calories Bot" class="brand-icon" loading="eager" data-v-fdf84ce5><span class="brand-text" data-v-fdf84ce5>Calories Notebook Bot</span></div><div class="footer-links" data-v-fdf84ce5><a href="https://t.me/caloriesnote_bot" class="footer-link" data-v-fdf84ce5>Telegram Bot</a>`);
      _push(ssrRenderComponent(_component_NuxtLink, {
        to: "/privacy",
        class: "footer-link privacy-link"
      }, {
        default: withCtx((_, _push2, _parent2, _scopeId) => {
          if (_push2) {
            _push2(`Политика конфиденциальности`);
          } else {
            return [
              createTextVNode("Политика конфиденциальности")
            ];
          }
        }),
        _: 1
      }, _parent));
      _push(ssrRenderComponent(_component_NuxtLink, {
        to: "/terms",
        class: "footer-link"
      }, {
        default: withCtx((_, _push2, _parent2, _scopeId) => {
          if (_push2) {
            _push2(`Условия использования`);
          } else {
            return [
              createTextVNode("Условия использования")
            ];
          }
        }),
        _: 1
      }, _parent));
      _push(`</div></div><div class="footer-bottom" data-v-fdf84ce5><p class="footer-text" data-v-fdf84ce5> Сделано с ❤️ для тех, кто следит за питанием </p></div></div></footer></div>`);
    };
  }
};
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("layouts/default.vue");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const _default = /* @__PURE__ */ _export_sfc(_sfc_main, [["__scopeId", "data-v-fdf84ce5"]]);
export {
  _default as default
};
//# sourceMappingURL=default-CRgS3pQf.js.map
