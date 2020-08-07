import Vue from 'vue'
import Router from 'vue-router'
import { interopDefault } from './utils'
import scrollBehavior from './router.scrollBehavior.js'

const _d7777550 = () => interopDefault(import('../pages/actual.vue' /* webpackChunkName: "pages/actual" */))
const _4cffbfc8 = () => interopDefault(import('../pages/configuration.vue' /* webpackChunkName: "pages/configuration" */))
const _3a2aadee = () => interopDefault(import('../pages/futura.vue' /* webpackChunkName: "pages/futura" */))
const _6abdf3f8 = () => interopDefault(import('../pages/index.vue' /* webpackChunkName: "pages/index" */))

// TODO: remove in Nuxt 3
const emptyFn = () => {}
const originalPush = Router.prototype.push
Router.prototype.push = function push (location, onComplete = emptyFn, onAbort) {
  return originalPush.call(this, location, onComplete, onAbort)
}

Vue.use(Router)

export const routerOptions = {
  mode: 'history',
  base: decodeURI('/'),
  linkActiveClass: 'nuxt-link-active',
  linkExactActiveClass: 'nuxt-link-exact-active',
  scrollBehavior,

  routes: [{
    path: "/actual",
    component: _d7777550,
    name: "actual"
  }, {
    path: "/configuration",
    component: _4cffbfc8,
    name: "configuration"
  }, {
    path: "/futura",
    component: _3a2aadee,
    name: "futura"
  }, {
    path: "/",
    component: _6abdf3f8,
    name: "index"
  }],

  fallback: false
}

export function createRouter () {
  return new Router(routerOptions)
}
