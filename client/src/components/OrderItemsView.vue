<script setup>
import { ref, computed, onBeforeMount } from 'vue'
import axios from 'axios'

const orderItems = ref([])
const orders = ref([])
const products = ref([])
const orderItemToAdd = ref({})
const orderItemToEdit = ref({})

const productsById = computed(() => {
  const result = {}
  for (const p of products.value) {
    result[p.id] = p
  }
  return result
})

async function fetchOrderItems() {
  const r = await axios.get('/api/order-items/')
  orderItems.value = r.data
}

async function fetchOrders() {
  const r = await axios.get('/api/orders/')
  orders.value = r.data
}

async function fetchProducts() {
  const r = await axios.get('/api/products/')
  products.value = r.data
}

async function onOrderItemAdd() {
  await axios.post('/api/order-items/', {
    ...orderItemToAdd.value,
  })
  await fetchOrderItems()
}

async function onRemoveClick(orderItem) {
  await axios.delete(`/api/order-items/${orderItem.id}/`)
  await fetchOrderItems()
}

async function onOrderItemEditClick(orderItem) {
  orderItemToEdit.value = { ...orderItem }
}

async function onUpdateOrderItem() {
  await axios.put(`/api/order-items/${orderItemToEdit.value.id}/`, {
    ...orderItemToEdit.value,
  })
  await fetchOrderItems()
}

onBeforeMount(async () => {
  await fetchOrderItems()
  await fetchOrders()
  await fetchProducts()
})
</script>

<template>
  <h2>Позиции заказов</h2>

  <form @submit.prevent.stop="onOrderItemAdd">
    <div class="row">
      <div class="col">
        <div class="form-floating">
          <select class="form-select" v-model="orderItemToAdd.order" required>
            <option :value="o.id" v-for="o in orders">Заказ #{{ o.id }}</option>
          </select>
          <label for="floatingInput">Заказ</label>
        </div>
      </div>
      <div class="col">
        <div class="form-floating">
          <select class="form-select" v-model="orderItemToAdd.product" required>
            <option :value="p.id" v-for="p in products">{{ p.name }}</option>
          </select>
          <label for="floatingInput">Товар</label>
        </div>
      </div>
      <div class="col">
        <div class="form-floating">
          <input type="number" class="form-control" v-model="orderItemToAdd.quantity" required />
          <label for="floatingInput">Количество</label>
        </div>
      </div>
      <div class="col">
        <div class="form-floating">
          <input type="number" step="0.01" class="form-control" v-model="orderItemToAdd.price" required />
          <label for="floatingInput">Цена</label>
        </div>
      </div>
      <div class="col-auto">
        <button class="btn btn-primary">Добавить</button>
      </div>
    </div>
  </form>

  <div v-for="item in orderItems" class="item">
    <div>Заказ #{{ item.order }}</div>
    <div>{{ productsById[item.product]?.name }}</div>
    <div>{{ item.quantity }} шт.</div>
    <div>{{ item.price }} руб.</div>
    <button
      class="btn btn-success"
      @click="onOrderItemEditClick(item)"
      data-bs-toggle="modal"
      data-bs-target="#editOrderItemModal"
    >
      Изменить
    </button>
    <button class="btn btn-danger" @click="onRemoveClick(item)">Удалить</button>
  </div>

  <div class="modal fade" id="editOrderItemModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5">Редактировать</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div class="form-floating mb-2">
            <select class="form-select" v-model="orderItemToEdit.order">
              <option :value="o.id" v-for="o in orders">Заказ #{{ o.id }}</option>
            </select>
            <label for="floatingInput">Заказ</label>
          </div>
          <div class="form-floating mb-2">
            <select class="form-select" v-model="orderItemToEdit.product">
              <option :value="p.id" v-for="p in products">{{ p.name }}</option>
            </select>
            <label for="floatingInput">Товар</label>
          </div>
          <div class="form-floating mb-2">
            <input type="number" class="form-control" v-model="orderItemToEdit.quantity" />
            <label for="floatingInput">Количество</label>
          </div>
          <div class="form-floating">
            <input type="number" step="0.01" class="form-control" v-model="orderItemToEdit.price" />
            <label for="floatingInput">Цена</label>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          <button data-bs-dismiss="modal" type="button" class="btn btn-primary" @click="onUpdateOrderItem">
            Сохранить
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.item {
  display: flex;
  gap: 8px;
  align-items: center;
  padding: 8px;
  margin-top: 8px;
  border: 1px solid #ddd;
  border-radius: 8px;
}
.item > div {
  flex: 1;
}
</style>