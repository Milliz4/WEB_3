<script setup>
import { ref, computed, onBeforeMount } from 'vue'
import axios from 'axios'

const addresses = ref([])
const customers = ref([])
const addressToAdd = ref({})
const addressToEdit = ref({})

const customersById = computed(() => {
  const result = {}
  for (const x of customers.value) {
    result[x.id] = x
  }
  return result
})

async function fetchAddresses() {
  const r = await axios.get('/api/addresses/')
  addresses.value = r.data
}

async function fetchCustomers() {
  const r = await axios.get('/api/customers/')
  customers.value = r.data
}

async function onAddressAdd() {
  await axios.post('/api/addresses/', {
    ...addressToAdd.value,
  })
  await fetchAddresses()
}

async function onRemoveClick(address) {
  await axios.delete(`/api/addresses/${address.id}/`)
  await fetchAddresses()
}

async function onAddressEditClick(address) {
  addressToEdit.value = { ...address }
}

async function onUpdateAddress() {
  await axios.put(`/api/addresses/${addressToEdit.value.id}/`, {
    ...addressToEdit.value,
  })
  await fetchAddresses()
}

onBeforeMount(async () => {
  await fetchAddresses()
  await fetchCustomers()
})
</script>

<template>
  <h2>Адреса</h2>

  <form @submit.prevent.stop="onAddressAdd">
    <div class="row">
      <div class="col">
        <div class="form-floating">
          <select class="form-select" v-model="addressToAdd.customer" required>
            <option :value="o.id" v-for="o in customers">{{ o.full_name }}</option>
          </select>
          <label for="floatingInput">Покупатель</label>
        </div>
      </div>
      <div class="col">
        <div class="form-floating">
          <input type="text" class="form-control" v-model="addressToAdd.street" required />
          <label for="floatingInput">Улица</label>
        </div>
      </div>
      <div class="col">
        <div class="form-floating">
          <input type="text" class="form-control" v-model="addressToAdd.city" required />
          <label for="floatingInput">Город</label>
        </div>
      </div>
      <div class="col">
        <div class="form-floating">
          <input type="text" class="form-control" v-model="addressToAdd.postal_code" required />
          <label for="floatingInput">Почтовый индекс</label>
        </div>
      </div>
      <div class="col-auto">
        <button class="btn btn-primary">Добавить</button>
      </div>
    </div>
  </form>

  <div v-for="item in addresses" class="item">
    <div>{{ customersById[item.customer]?.full_name }}</div>
    <div>{{ item.street }}</div>
    <div>{{ item.city }}</div>
    <div>{{ item.postal_code }}</div>
    <button
      class="btn btn-success"
      @click="onAddressEditClick(item)"
      data-bs-toggle="modal"
      data-bs-target="#editAddressModal"
    >
      Изменить
    </button>
    <button class="btn btn-danger" @click="onRemoveClick(item)">Удалить</button>
  </div>

  <div class="modal fade" id="editAddressModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5">Редактировать</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div class="form-floating mb-2">
            <select class="form-select" v-model="addressToEdit.customer">
              <option :value="o.id" v-for="o in customers">{{ o.full_name }}</option>
            </select>
            <label for="floatingInput">Покупатель</label>
          </div>
          <div class="form-floating mb-2">
            <input type="text" class="form-control" v-model="addressToEdit.street" />
            <label for="floatingInput">Улица</label>
          </div>
          <div class="form-floating mb-2">
            <input type="text" class="form-control" v-model="addressToEdit.city" />
            <label for="floatingInput">Город</label>
          </div>
          <div class="form-floating">
            <input type="text" class="form-control" v-model="addressToEdit.postal_code" />
            <label for="floatingInput">Почтовый индекс</label>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          <button data-bs-dismiss="modal" type="button" class="btn btn-primary" @click="onUpdateAddress">
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