import Vue from 'vue'
import Router from 'vue-router'
import { interopDefault } from './utils'
import scrollBehavior from './router.scrollBehavior.js'

const _f3482d40 = () => interopDefault(import('../pages/actual.vue' /* webpackChunkName: "pages/actual" */))
const _2f516314 = () => interopDefault(import('../pages/configuration.vue' /* webpackChunkName: "pages/configuration" */))
const _55fb65de = () => interopDefault(import('../pages/futura.vue' /* webpackChunkName: "pages/futura" */))
const _485a8c95 = () => interopDefault(import('../pages/server.vue' /* webpackChunkName: "pages/server" */))
const _96c4a220 = () => interopDefault(import('../pages/index.vue' /* webpackChunkName: "pages/index" */))

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
    component: _f3482d40,
    name: "actual"
  }, {
    path: "/configuration",
    component: _2f516314,
    name: "configuration"
  }, {
    path: "/futura",
    component: _55fb65de,
    name: "futura"
  }, {
    path: "/server",
    component: _485a8c95,
    name: "server"
  }, {
    path: "/",
    component: _96c4a220,
    name: "index"
  }],

  fallback: false
}

export function createRouter () {
  return new Router(routerOptions)
}
