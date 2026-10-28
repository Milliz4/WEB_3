<script setup>
import { ref, computed, onBeforeMount } from 'vue'
import axios from 'axios'

const reviews = ref([])
const products = ref([])
const users = ref([])
const reviewToAdd = ref({})
const reviewToEdit = ref({})

const productsById = computed(() => {
  const result = {}
  for (const p of products.value) {
    result[p.id] = p
  }
  return result
})

const usersById = computed(() => {
  const result = {}
  for (const u of users.value) {
    result[u.id] = u
  }
  return result
})

async function fetchReviews() {
  const r = await axios.get('/api/reviews/')
  reviews.value = r.data
}

async function fetchProducts() {
  const r = await axios.get('/api/products/')
  products.value = r.data
}

async function fetchUsers() {
  const r = await axios.get('/api/users/')
  users.value = r.data
}

async function onReviewAdd() {
  await axios.post('/api/reviews/', {
    ...reviewToAdd.value,
  })
  await fetchReviews()
}

async function onRemoveClick(review) {
  await axios.delete(`/api/reviews/${review.id}/`)
  await fetchReviews()
}

async function onReviewEditClick(review) {
  reviewToEdit.value = { ...review }
}

async function onUpdateReview() {
  await axios.put(`/api/reviews/${reviewToEdit.value.id}/`, {
    ...reviewToEdit.value,
  })
  await fetchReviews()
}

onBeforeMount(async () => {
  await fetchReviews()
  await fetchProducts()
  await fetchUsers()
})
</script>

<template>
  <h2>Отзывы</h2>

  <form @submit.prevent.stop="onReviewAdd">
    <div class="row">
      <div class="col">
        <div class="form-floating">
          <select class="form-select" v-model="reviewToAdd.product" required>
            <option :value="p.id" v-for="p in products">{{ p.name }}</option>
          </select>
          <label for="floatingInput">Товар</label>
        </div>
      </div>
      <div class="col">
        <div class="form-floating">
          <select class="form-select" v-model="reviewToAdd.author">
            <option :value="u.id" v-for="u in users">{{ u.username }}</option>
          </select>
          <label for="floatingInput">Автор</label>
        </div>
      </div>
      <div class="col-auto">
        <div class="form-floating">
          <input type="number" min="1" max="5" class="form-control" v-model="reviewToAdd.rating" required />
          <label for="floatingInput">Оценка</label>
        </div>
      </div>
      <div class="col">
        <div class="form-floating">
          <input type="text" class="form-control" v-model="reviewToAdd.text" required />
          <label for="floatingInput">Текст</label>
        </div>
      </div>
      <div class="col-auto">
        <button class="btn btn-primary">Добавить</button>
      </div>
    </div>
  </form>

  <div v-for="item in reviews" class="item">
    <div>{{ productsById[item.product]?.name }}</div>
    <div>{{ usersById[item.author]?.username }}</div>
    <div>{{ item.rating }} / 5</div>
    <div>{{ item.text }}</div>
    <button
      class="btn btn-success"
      @click="onReviewEditClick(item)"
      data-bs-toggle="modal"
      data-bs-target="#editReviewModal"
    >
      Изменить
    </button>
    <button class="btn btn-danger" @click="onRemoveClick(item)">Удалить</button>
  </div>

  <div class="modal fade" id="editReviewModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5">Редактировать</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div class="form-floating mb-2">
            <select class="form-select" v-model="reviewToEdit.product">
              <option :value="p.id" v-for="p in products">{{ p.name }}</option>
            </select>
            <label for="floatingInput">Товар</label>
          </div>
          <div class="form-floating mb-2">
            <select class="form-select" v-model="reviewToEdit.author">
              <option :value="u.id" v-for="u in users">{{ u.username }}</option>
            </select>
            <label for="floatingInput">Автор</label>
          </div>
          <div class="form-floating mb-2">
            <input type="number" min="1" max="5" class="form-control" v-model="reviewToEdit.rating" />
            <label for="floatingInput">Оценка</label>
          </div>
          <div class="form-floating">
            <input type="text" class="form-control" v-model="reviewToEdit.text" />
            <label for="floatingInput">Текст</label>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          <button data-bs-dismiss="modal" type="button" class="btn btn-primary" @click="onUpdateReview">
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