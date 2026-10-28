import { createRouter, createWebHistory } from 'vue-router'
import CategoriesView from '../components/CategoriesView.vue'
import ProductsView from '../components/ProductsView.vue'
import OrdersView from '../components/OrdersView.vue'
import OrderItemsView from '../components/OrderItemsView.vue'
import ReviewsView from '../components/ReviewsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', redirect: '/categories' },
    { path: '/categories', name: 'categories', component: CategoriesView },
    { path: '/products', name: 'products', component: ProductsView },
    { path: '/orders', name: 'orders', component: OrdersView },
    { path: '/order-items', name: 'order-items', component: OrderItemsView },
    { path: '/reviews', name: 'reviews', component: ReviewsView },
  ],
})

export default router