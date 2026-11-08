<script setup>
import { ref, onBeforeMount } from 'vue'
import axios from 'axios'

const customers = ref([])
const customerToAdd = ref({})
const customerToEdit = ref({})

async function fetchCustomers() {
  const r = await axios.get('/api/customers/')
  customers.value = r.data
}

async function onCustomerAdd() {
  await axios.post('/api/customers/', {
    ...customerToAdd.value,
  })
  await fetchCustomers()
}

async function onRemoveClick(customer) {
  await axios.delete(`/api/customers/${customer.id}/`)
  await fetchCustomers()
}

async function onCustomerEditClick(customer) {
  customerToEdit.value = { ...customer }
}

async function onUpdateCustomer() {
  await axios.put(`/api/customers/${customerToEdit.value.id}/`, {
    ...customerToEdit.value,
  })
  await fetchCustomers()
}

onBeforeMount(async () => {
  await fetchCustomers()
})
</script>

<template>
  <h2>Покупатели</h2>

  <form @submit.prevent.stop="onCustomerAdd">
    <div class="row">
      <div class="col">
        <div class="form-floating">
          <input type="text" class="form-control" v-model="customerToAdd.full_name" required />
          <label for="floatingInput">ФИ</label>
        </div>
      </div>
      <div class="col">
        <div class="form-floating">
          <input type="email" class="form-control" v-model="customerToAdd.email" required />
          <label for="floatingInput">Email</label>
        </div>
      </div>
      <div class="col">
        <div class="form-floating">
          <input type="text" class="form-control" v-model="customerToAdd.phone" required />
          <label for="floatingInput">Телефон</label>
        </div>
      </div>
      <div class="col-auto">
        <button class="btn btn-primary">Добавить</button>
      </div>
    </div>
  </form>

  <div v-for="item in customers" class="item">
    <div>{{ item.full_name }}</div>
    <div>{{ item.email }}</div>
    <div>{{ item.phone }}</div>
    <button
      class="btn btn-success"
      @click="onCustomerEditClick(item)"
      data-bs-toggle="modal"
      data-bs-target="#editCustomerModal"
    >
      Изменить
    </button>
    <button class="btn btn-danger" @click="onRemoveClick(item)">Удалить</button>
  </div>

  <div class="modal fade" id="editCustomerModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5">Редактировать</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div class="form-floating mb-2">
            <input type="text" class="form-control" v-model="customerToEdit.full_name" />
            <label for="floatingInput">ФИ</label>
          </div>
          <div class="form-floating mb-2">
            <input type="email" class="form-control" v-model="customerToEdit.email" />
            <label for="floatingInput">Email</label>
          </div>
          <div class="form-floating">
            <input type="text" class="form-control" v-model="customerToEdit.phone" />
            <label for="floatingInput">Телефон</label>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          <button data-bs-dismiss="modal" type="button" class="btn btn-primary" @click="onUpdateCustomer">
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