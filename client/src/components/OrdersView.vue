<script setup>
import { ref, computed, onBeforeMount } from 'vue'
import axios from 'axios'

const orders = ref([])
const users = ref([])
const orderToAdd = ref({})
const orderToEdit = ref({})

const statuses = [
  { id: 'CREATED', name: 'Создан' },
  { id: 'PAID', name: 'Оплачен' },
  { id: 'DELIVERED', name: 'Доставлен' },
  { id: 'CANCELLED', name: 'Отменён' },
]

const paymentMethods = [
  { id: 'CASH', name: 'Наличные' },
  { id: 'CONLINE', name: 'Картой онлайн' },
  { id: 'CCOURIER', name: 'Картой курьеру' },
]

const usersById = computed(() => {
  const result = {}
  for (const u of users.value) {
    result[u.id] = u
  }
  return result
})

const statusesById = computed(() => {
  const result = {}
  for (const s of statuses) {
    result[s.id] = s
  }
  return result
})

const paymentMethodsById = computed(() => {
  const result = {}
  for (const p of paymentMethods) {
    result[p.id] = p
  }
  return result
})

async function fetchOrders() {
  const r = await axios.get('/api/orders/')
  orders.value = r.data
}

async function fetchUsers() {
  const r = await axios.get('/api/users/')
  users.value = r.data
}

async function onOrderAdd() {
  await axios.post('/api/orders/', {
    ...orderToAdd.value,
  })
  await fetchOrders()
}

async function onRemoveClick(order) {
  await axios.delete(`/api/orders/${order.id}/`)
  await fetchOrders()
}

async function onOrderEditClick(order) {
  orderToEdit.value = { ...order }
}

async function onUpdateOrder() {
  await axios.put(`/api/orders/${orderToEdit.value.id}/`, {
    ...orderToEdit.value,
  })
  await fetchOrders()
}

onBeforeMount(async () => {
  await fetchOrders()
  await fetchUsers()
})
</script>

<template>
  <h2>Заказы</h2>

  <form @submit.prevent.stop="onOrderAdd">
    <div class="row">
      <div class="col">
        <div class="form-floating">
          <select class="form-select" v-model="orderToAdd.customer">
            <option :value="u.id" v-for="u in users">{{ u.username }}</option>
          </select>
          <label for="floatingInput">Покупатель</label>
        </div>
      </div>
      <div class="col">
        <div class="form-floating">
          <select class="form-select" v-model="orderToAdd.status" required>
            <option :value="s.id" v-for="s in statuses">{{ s.name }}</option>
          </select>
          <label for="floatingInput">Статус</label>
        </div>
      </div>
      <div class="col">
        <div class="form-floating">
          <input type="number" step="0.01" class="form-control" v-model="orderToAdd.total" required />
          <label for="floatingInput">Сумма</label>
        </div>
      </div>
      <div class="col">
        <div class="form-floating">
          <select class="form-select" v-model="orderToAdd.payment_method" required>
            <option :value="p.id" v-for="p in paymentMethods">{{ p.name }}</option>
          </select>
          <label for="floatingInput">Оплата</label>
        </div>
      </div>
      <div class="col-auto">
        <button class="btn btn-primary">Добавить</button>
      </div>
    </div>
  </form>

  <div v-for="item in orders" class="item">
    <div>Заказ #{{ item.id }}</div>
    <div>{{ usersById[item.customer]?.username }}</div>
    <div>{{ statusesById[item.status]?.name }}</div>
    <div>{{ item.total }} руб.</div>
    <div>{{ paymentMethodsById[item.payment_method]?.name }}</div>
    <button
      class="btn btn-success"
      @click="onOrderEditClick(item)"
      data-bs-toggle="modal"
      data-bs-target="#editOrderModal"
    >
      Изменить
    </button>
    <button class="btn btn-danger" @click="onRemoveClick(item)">Удалить</button>
  </div>

  <div class="modal fade" id="editOrderModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5">Редактировать</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div class="form-floating mb-2">
            <select class="form-select" v-model="orderToEdit.customer">
              <option :value="u.id" v-for="u in users">{{ u.username }}</option>
            </select>
            <label for="floatingInput">Покупатель</label>
          </div>
          <div class="form-floating mb-2">
            <select class="form-select" v-model="orderToEdit.status">
              <option :value="s.id" v-for="s in statuses">{{ s.name }}</option>
            </select>
            <label for="floatingInput">Статус</label>
          </div>
          <div class="form-floating mb-2">
            <input type="number" step="0.01" class="form-control" v-model="orderToEdit.total" />
            <label for="floatingInput">Сумма</label>
          </div>
          <div class="form-floating">
            <select class="form-select" v-model="orderToEdit.payment_method">
              <option :value="p.id" v-for="p in paymentMethods">{{ p.name }}</option>
            </select>
            <label for="floatingInput">Оплата</label>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          <button data-bs-dismiss="modal" type="button" class="btn btn-primary" @click="onUpdateOrder">
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