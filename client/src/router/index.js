import { createRouter, createWebHistory } from 'vue-router'
import CustomersView from '../components/Customersview.vue'
import AddressesView from '../components/Addressesview.vue'
import CategoriesView from '../components/CategoriesView.vue'
import ManufacturersView from '../components/Manufacturersview.vue'
import ProductsView from '../components/ProductsView.vue'
import OrdersView from '../components/OrdersView.vue'
import OrderItemsView from '../components/OrderItemsView.vue'
import ReviewsView from '../components/ReviewsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', redirect: '/customers' },
    { path: '/customers', name: 'customers', component: CustomersView },
    { path: '/addresses', name: 'addresses', component: AddressesView },
    { path: '/categories', name: 'categories', component: CategoriesView },
    { path: '/manufacturers', name: 'manufacturers', component: ManufacturersView },
    { path: '/products', name: 'products', component: ProductsView },
    { path: '/orders', name: 'orders', component: OrdersView },
    { path: '/order-items', name: 'order-items', component: OrderItemsView },
    { path: '/reviews', name: 'reviews', component: ReviewsView },
  ],
})

export default router