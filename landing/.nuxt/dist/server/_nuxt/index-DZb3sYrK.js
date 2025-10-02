import { _ as __nuxt_component_0 } from "./HeaderSection-Bskbvj7i.js";
import { _ as __nuxt_component_0$1 } from "./nuxt-link-BeVqdmom.js";
import { ref, unref, withCtx, createTextVNode, toDisplayString, useSSRContext } from "vue";
import { ssrRenderAttrs, ssrRenderComponent, ssrRenderList, ssrRenderAttr, ssrInterpolate } from "vue/server-renderer";
import { a as useSeoMeta, u as useHead } from "./v3-D915_2dV.js";
import { _ as _export_sfc } from "../server.mjs";
import "./virtual_public-CEu87jeG.js";
import "#internal/nuxt/paths";
import "/Users/kamil/PycharmProjects/calories_notebook/landing/node_modules/ufo/dist/index.mjs";
import "/Users/kamil/PycharmProjects/calories_notebook/landing/node_modules/@unhead/vue/dist/index.mjs";
import "ofetch";
import "/Users/kamil/PycharmProjects/calories_notebook/landing/node_modules/hookable/dist/index.mjs";
import "/Users/kamil/PycharmProjects/calories_notebook/landing/node_modules/unctx/dist/index.mjs";
import "/Users/kamil/PycharmProjects/calories_notebook/landing/node_modules/h3/dist/index.mjs";
import "vue-router";
import "/Users/kamil/PycharmProjects/calories_notebook/landing/node_modules/radix3/dist/index.mjs";
import "/Users/kamil/PycharmProjects/calories_notebook/landing/node_modules/defu/dist/defu.mjs";
const _sfc_main = {
  __name: "index",
  __ssrInlineRender: true,
  setup(__props) {
    useSeoMeta({
      title: "Блог о питании и здоровье | Calories Bot",
      description: "Полезные статьи о правильном питании, подсчете калорий и здоровом образе жизни. ИИ-анализ еды и автоматический дневник питания.",
      ogTitle: "Блог о питании и здоровье | Calories Bot",
      ogDescription: "Полезные статьи о правильном питании, подсчете калорий и здоровом образе жизни",
      ogImage: "https://calories.toxiguard.site/blog-og.jpg",
      ogUrl: "https://calories.toxiguard.site/blog",
      robots: "index, follow",
      author: "Calories Bot"
    });
    useHead({
      link: [
        { rel: "canonical", href: "https://calories.toxiguard.site/blog" }
      ],
      script: [
        {
          type: "application/ld+json",
          innerHTML: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "Blog",
            "name": "Блог о питании и здоровье",
            "description": "Полезные статьи о правильном питании, подсчете калорий и здоровом образе жизни",
            "url": "https://calories.toxiguard.site/blog",
            "publisher": {
              "@type": "Organization",
              "name": "Calories Bot",
              "url": "https://calories.toxiguard.site"
            }
          })
        }
      ]
    });
    const posts = ref([
      {
        slug: "podschet-kaloriy-po-foto-telegram-bot",
        title: "Подсчет калорий по фото: как Telegram-бот меняет правила игры",
        excerpt: "Узнайте, как ИИ-анализ фотографий еды помогает точно считать калории и контролировать питание",
        category: "Питание",
        date: "26 сентября 2025",
        image: "/blog/podschet-kaloriy-po-foto.jpg"
      },
      {
        slug: "avtomaticheskiy-dnevnik-pitaniya",
        title: "Автоматический дневник питания: будущее уже здесь",
        excerpt: "Как технологии упрощают ведение дневника питания и помогают достичь целей в здоровье",
        category: "Технологии",
        date: "28 сентября 2025",
        image: "/blog/avtomaticheskiy-dnevnik-pitaniya.jpg"
      },
      {
        slug: "ii-v-pitanii-kak-iskusstvennyy-intellekt-menyaet-zdorove",
        title: "ИИ в питании: как искусственный интеллект меняет здоровье",
        excerpt: "Революция в области питания: как машинное обучение помогает принимать правильные решения",
        category: "ИИ и здоровье",
        date: "28 сентября 2025",
        image: "/blog/ii-v-pitanii.jpg"
      },
      {
        slug: "pochemu-vazhno-sledit-za-kaloriyami-nauka-zdorove-prakticheskie-vyvody",
        title: "Почему важно следить за калориями: наука, здоровье, практические выводы",
        excerpt: "Научные исследования о важности подсчета калорий и практические советы для здорового питания",
        category: "Наука",
        date: "28 сентября 2025",
        image: "/blog/pochemu-vazhno-sledit-za-kaloriyami.jpg"
      }
    ]);
    return (_ctx, _push, _parent, _attrs) => {
      const _component_HeaderSection = __nuxt_component_0;
      const _component_NuxtLink = __nuxt_component_0$1;
      _push(`<div${ssrRenderAttrs(_attrs)} data-v-433ebdc8>`);
      _push(ssrRenderComponent(_component_HeaderSection, null, null, _parent));
      _push(`<section class="blog-hero" data-v-433ebdc8><div class="container" data-v-433ebdc8><h1 class="blog-title" data-v-433ebdc8>Блог о питании и здоровье</h1><p class="blog-subtitle" data-v-433ebdc8>Полезные статьи о правильном питании, подсчете калорий и здоровом образе жизни</p></div></section><section class="blog-posts" data-v-433ebdc8><div class="container" data-v-433ebdc8><div class="posts-grid" data-v-433ebdc8><!--[-->`);
      ssrRenderList(unref(posts), (post) => {
        _push(`<article class="post-card" data-v-433ebdc8><div class="post-image" data-v-433ebdc8><img${ssrRenderAttr("src", post.image)}${ssrRenderAttr("alt", post.title)} loading="lazy" class="w-full h-48 object-cover rounded-lg" data-v-433ebdc8></div><div class="post-content" data-v-433ebdc8><div class="post-meta" data-v-433ebdc8><span class="post-date" data-v-433ebdc8>Опубликовано ${ssrInterpolate(post.date)}</span><span class="post-category" data-v-433ebdc8>${ssrInterpolate(post.category)}</span></div><h2 class="post-title" data-v-433ebdc8>`);
        _push(ssrRenderComponent(_component_NuxtLink, {
          to: `/blog/${post.slug}`
        }, {
          default: withCtx((_, _push2, _parent2, _scopeId) => {
            if (_push2) {
              _push2(`${ssrInterpolate(post.title)}`);
            } else {
              return [
                createTextVNode(toDisplayString(post.title), 1)
              ];
            }
          }),
          _: 2
        }, _parent));
        _push(`</h2><p class="post-excerpt" data-v-433ebdc8>${ssrInterpolate(post.excerpt)}</p><div class="post-footer" data-v-433ebdc8>`);
        _push(ssrRenderComponent(_component_NuxtLink, {
          to: `/blog/${post.slug}`,
          class: "read-more"
        }, {
          default: withCtx((_, _push2, _parent2, _scopeId) => {
            if (_push2) {
              _push2(` Читать далее → `);
            } else {
              return [
                createTextVNode(" Читать далее → ")
              ];
            }
          }),
          _: 2
        }, _parent));
        _push(`</div></div></article>`);
      });
      _push(`<!--]--></div></div></section></div>`);
    };
  }
};
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("pages/blog/index.vue");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const index = /* @__PURE__ */ _export_sfc(_sfc_main, [["__scopeId", "data-v-433ebdc8"]]);
export {
  index as default
};
//# sourceMappingURL=index-DZb3sYrK.js.map
