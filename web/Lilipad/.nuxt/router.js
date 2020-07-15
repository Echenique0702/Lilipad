import Vue from 'vue'
import Router from 'vue-router'
import { interopDefault } from './utils'
import scrollBehavior from './router.scrollBehavior.js'

const _542ea632 = () => interopDefault(import('../pages/actual.vue' /* webpackChunkName: "pages/actual" */))
const _519c2ca6 = () => interopDefault(import('../pages/configuration.vue' /* webpackChunkName: "pages/configuration" */))
const _248f1098 = () => interopDefault(import('../pages/futura.vue' /* webpackChunkName: "pages/futura" */))
const _d0315fc8 = () => interopDefault(import('../pages/server.vue' /* webpackChunkName: "pages/server" */))
const _4f9242ee = () => interopDefault(import('../pages/index.vue' /* webpackChunkName: "pages/index" */))

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
    component: _542ea632,
    name: "actual"
  }, {
    path: "/configuration",
    component: _519c2ca6,
    name: "configuration"
  }, {
    path: "/futura",
    component: _248f1098,
    name: "futura"
  }, {
    path: "/server",
    component: _d0315fc8,
    name: "server"
  }, {
    path: "/",
    component: _4f9242ee,
    name: "index"
  }],

  fallback: false
}

export function createRouter () {
  return new Router(routerOptions)
}
