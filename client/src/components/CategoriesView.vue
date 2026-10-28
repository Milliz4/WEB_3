<script setup>
import { ref, onBeforeMount } from 'vue'
import axios from 'axios'

const categories = ref([])
const categoryToAdd = ref({})
const categoryToEdit = ref({})

async function fetchCategories() {
  const r = await axios.get('/api/categories/')
  categories.value = r.data
}

async function onCategoryAdd() {
  await axios.post('/api/categories/', {
    ...categoryToAdd.value,
  })
  await fetchCategories()
}

async function onRemoveClick(category) {
  await axios.delete(`/api/categories/${category.id}/`)
  await fetchCategories()
}

async function onCategoryEditClick(category) {
  categoryToEdit.value = { ...category }
}

async function onUpdateCategory() {
  await axios.put(`/api/categories/${categoryToEdit.value.id}/`, {
    ...categoryToEdit.value,
  })
  await fetchCategories()
}

onBeforeMount(async () => {
  await fetchCategories()
})
</script>

<template>
  <h2>Категории</h2>

  <form @submit.prevent.stop="onCategoryAdd">
    <div class="row">
      <div class="col">
        <div class="form-floating">
          <input type="text" class="form-control" v-model="categoryToAdd.name" required />
          <label for="floatingInput">Название</label>
        </div>
      </div>
      <div class="col-auto">
        <button class="btn btn-primary">Добавить</button>
      </div>
    </div>
  </form>

  <div v-for="item in categories" class="item">
    <div>{{ item.name }}</div>
    <button
      class="btn btn-success"
      @click="onCategoryEditClick(item)"
      data-bs-toggle="modal"
      data-bs-target="#editCategoryModal"
    >
      Изменить
    </button>
    <button class="btn btn-danger" @click="onRemoveClick(item)">Удалить</button>
  </div>

  <div class="modal fade" id="editCategoryModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5">Редактировать</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div class="form-floating">
            <input type="text" class="form-control" v-model="categoryToEdit.name" />
            <label for="floatingInput">Название</label>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          <button data-bs-dismiss="modal" type="button" class="btn btn-primary" @click="onUpdateCategory">
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