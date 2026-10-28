<script setup>
import { ref, computed, onBeforeMount } from 'vue'
import axios from 'axios'

const products = ref([])
const categories = ref([])
const productToAdd = ref({})
const productToEdit = ref({})

const categoriesById = computed(() => {
  const result = {}
  for (const c of categories.value) {
    result[c.id] = c
  }
  return result
})

async function fetchProducts() {
  const r = await axios.get('/api/products/')
  products.value = r.data
}

async function fetchCategories() {
  const r = await axios.get('/api/categories/')
  categories.value = r.data
}

async function onProductAdd() {
  await axios.post('/api/products/', {
    ...productToAdd.value,
  })
  await fetchProducts()
}

async function onRemoveClick(product) {
  await axios.delete(`/api/products/${product.id}/`)
  await fetchProducts()
}

async function onProductEditClick(product) {
  productToEdit.value = { ...product }
}

async function onUpdateProduct() {
  await axios.put(`/api/products/${productToEdit.value.id}/`, {
    ...productToEdit.value,
  })
  await fetchProducts()
}

onBeforeMount(async () => {
  await fetchProducts()
  await fetchCategories()
})
</script>

<template>
  <h2>Товары</h2>

  <form @submit.prevent.stop="onProductAdd">
    <div class="row">
      <div class="col">
        <div class="form-floating">
          <input type="text" class="form-control" v-model="productToAdd.name" required />
          <label for="floatingInput">Название</label>
        </div>
      </div>
      <div class="col">
        <div class="form-floating">
          <input type="text" class="form-control" v-model="productToAdd.description" />
          <label for="floatingInput">Описание</label>
        </div>
      </div>
      <div class="col">
        <div class="form-floating">
          <input type="number" step="0.01" class="form-control" v-model="productToAdd.price" required />
          <label for="floatingInput">Цена</label>
        </div>
      </div>
      <div class="col">
        <div class="form-floating">
          <input type="number" class="form-control" v-model="productToAdd.stock" required />
          <label for="floatingInput">На складе</label>
        </div>
      </div>
      <div class="col">
        <div class="form-floating">
          <select class="form-select" v-model="productToAdd.category" required>
            <option :value="c.id" v-for="c in categories">{{ c.name }}</option>
          </select>
          <label for="floatingInput">Категория</label>
        </div>
      </div>
      <div class="col-auto">
        <button class="btn btn-primary">Добавить</button>
      </div>
    </div>
  </form>

  <div v-for="item in products" class="item">
    <div>{{ item.name }}</div>
    <div>{{ item.description }}</div>
    <div>{{ item.price }} руб.</div>
    <div>{{ item.stock }} шт.</div>
    <div>{{ categoriesById[item.category]?.name }}</div>
    <button
      class="btn btn-success"
      @click="onProductEditClick(item)"
      data-bs-toggle="modal"
      data-bs-target="#editProductModal"
    >
      Изменить
    </button>
    <button class="btn btn-danger" @click="onRemoveClick(item)">Удалить</button>
  </div>

  <div class="modal fade" id="editProductModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5">Редактировать</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div class="form-floating mb-2">
            <input type="text" class="form-control" v-model="productToEdit.name" />
            <label for="floatingInput">Название</label>
          </div>
          <div class="form-floating mb-2">
            <input type="text" class="form-control" v-model="productToEdit.description" />
            <label for="floatingInput">Описание</label>
          </div>
          <div class="form-floating mb-2">
            <input type="number" step="0.01" class="form-control" v-model="productToEdit.price" />
            <label for="floatingInput">Цена</label>
          </div>
          <div class="form-floating mb-2">
            <input type="number" class="form-control" v-model="productToEdit.stock" />
            <label for="floatingInput">На складе</label>
          </div>
          <div class="form-floating">
            <select class="form-select" v-model="productToEdit.category">
              <option :value="c.id" v-for="c in categories">{{ c.name }}</option>
            </select>
            <label for="floatingInput">Категория</label>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          <button data-bs-dismiss="modal" type="button" class="btn btn-primary" @click="onUpdateProduct">
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