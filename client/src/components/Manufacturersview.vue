<script setup>
import { ref, onBeforeMount } from 'vue'
import axios from 'axios'

const manufacturers = ref([])
const manufacturerToAdd = ref({})
const manufacturerToEdit = ref({})
const manufacturersPictureRef = ref()
const manufacturersEditPictureRef = ref()
const manufacturerAddImageUrl = ref()
const bigImageUrl = ref()

async function fetchManufacturers() {
  const r = await axios.get('/api/manufacturers/')
  manufacturers.value = r.data
}

// показываем выбранный файл сразу после выбора
async function manufacturersAddPictureChange() {
  const file = manufacturersPictureRef.value.files[0]
  manufacturerAddImageUrl.value = file ? URL.createObjectURL(file) : undefined
}

async function onManufacturerAdd() {
  const formData = new FormData()

  // файл добавляем только если он выбран
  const file = manufacturersPictureRef.value.files[0]
  if (file) {
    formData.append('picture', file)
  }

  formData.set('name', manufacturerToAdd.value.name)
  formData.set('country', manufacturerToAdd.value.country)

  await axios.post('/api/manufacturers/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  await fetchManufacturers()
}

async function onRemoveClick(manufacturer) {
  await axios.delete(`/api/manufacturers/${manufacturer.id}/`)
  await fetchManufacturers()
}

async function onManufacturerEditClick(manufacturer) {
  manufacturerToEdit.value = { ...manufacturer }
  manufacturersEditPictureRef.value.value = ''
}

async function onUpdateManufacturer() {
  const formData = new FormData()

  // если новый файл не выбран, старая картинка останется как есть
  const file = manufacturersEditPictureRef.value.files[0]
  if (file) {
    formData.append('picture', file)
  }

  formData.set('name', manufacturerToEdit.value.name)
  formData.set('country', manufacturerToEdit.value.country)

  await axios.put(`/api/manufacturers/${manufacturerToEdit.value.id}/`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  await fetchManufacturers()
}

onBeforeMount(async () => {
  await fetchManufacturers()
})
</script>

<template>
  <h2>Производители</h2>

  <form @submit.prevent.stop="onManufacturerAdd">
    <div class="row">
      <div class="col">
        <div class="form-floating">
          <input type="text" class="form-control" v-model="manufacturerToAdd.name" required />
          <label for="floatingInput">Название</label>
        </div>
      </div>
      <div class="col">
        <div class="form-floating">
          <input type="text" class="form-control" v-model="manufacturerToAdd.country" required />
          <label for="floatingInput">Страна</label>
        </div>
      </div>
      <div class="col-auto">
        <input
          class="form-control"
          type="file"
          ref="manufacturersPictureRef"
          @change="manufacturersAddPictureChange"
        />
      </div>
      <div class="col-auto">
        <img v-if="manufacturerAddImageUrl" :src="manufacturerAddImageUrl" style="max-height: 60px" alt="" />
      </div>
      <div class="col-auto">
        <button class="btn btn-primary">Добавить</button>
      </div>
    </div>
  </form>

  <div v-for="item in manufacturers" class="item">
    <div>{{ item.name }}</div>
    <div>{{ item.country }}</div>
    <div>
      <img
        v-if="item.picture"
        :src="item.picture"
        style="max-height: 60px; cursor: pointer"
        data-bs-toggle="modal"
        data-bs-target="#imageModal"
        @click="bigImageUrl = item.picture"
        alt=""
      />
    </div>
    <button
      class="btn btn-success"
      @click="onManufacturerEditClick(item)"
      data-bs-toggle="modal"
      data-bs-target="#editManufacturerModal"
    >
      Изменить
    </button>
    <button class="btn btn-danger" @click="onRemoveClick(item)">Удалить</button>
  </div>

  <div class="modal fade" id="editManufacturerModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5">Редактировать</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div class="form-floating mb-2">
            <input type="text" class="form-control" v-model="manufacturerToEdit.name" />
            <label for="floatingInput">Название</label>
          </div>
          <div class="form-floating mb-2">
            <input type="text" class="form-control" v-model="manufacturerToEdit.country" />
            <label for="floatingInput">Страна</label>
          </div>
          <div>
            <label class="form-label">Новый логотип (необязательно)</label>
            <input class="form-control" type="file" ref="manufacturersEditPictureRef" />
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          <button data-bs-dismiss="modal" type="button" class="btn btn-primary" @click="onUpdateManufacturer">
            Сохранить
          </button>
        </div>
      </div>
    </div>
  </div>

  <div class="modal fade" id="imageModal" tabindex="-1">
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-body">
          <img :src="bigImageUrl" class="img-fluid" alt="" />
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