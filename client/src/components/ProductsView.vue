<script setup>
import { ref, computed, onBeforeMount } from 'vue'
import axios from 'axios'

const products = ref([])
const categories = ref([])
const manufacturers = ref([])
const photos = ref([])
const productToAdd = ref({})
const productToEdit = ref({})
const productsPictureRef = ref()
const productsEditPictureRef = ref()
const productAddImageUrl = ref()
const bigImageUrl = ref()

// альбом фотографий товара
const albumProduct = ref({})
const albumPhotoUrl = ref()
const albumPhotosRef = ref()

const categoriesById = computed(() => {
  const result = {}
  for (const c of categories.value) {
    result[c.id] = c
  }
  return result
})

const manufacturersById = computed(() => {
  const result = {}
  for (const m of manufacturers.value) {
    result[m.id] = m
  }
  return result
})

// фотографии только того товара, чей альбом открыт
const albumPhotos = computed(() => {
  return photos.value.filter((p) => p.product === albumProduct.value.id)
})

async function fetchProducts() {
  const r = await axios.get('/api/products/')
  products.value = r.data
}

async function fetchCategories() {
  const r = await axios.get('/api/categories/')
  categories.value = r.data
}

async function fetchManufacturers() {
  const r = await axios.get('/api/manufacturers/')
  manufacturers.value = r.data
}

async function fetchPhotos() {
  const r = await axios.get('/api/product-photos/')
  photos.value = r.data
}

// показываем выбранный файл сразу после выбора
async function productsAddPictureChange() {
  const file = productsPictureRef.value.files[0]
  productAddImageUrl.value = file ? URL.createObjectURL(file) : undefined
}

async function onProductAdd() {
  const formData = new FormData()

  // файл добавляем только если он выбран
  const file = productsPictureRef.value.files[0]
  if (file) {
    formData.append('picture', file)
  }

  formData.set('name', productToAdd.value.name)
  formData.set('price', productToAdd.value.price)
  formData.set('stock', productToAdd.value.stock)
  formData.set('category', productToAdd.value.category)
  formData.set('manufacturer', productToAdd.value.manufacturer)

  await axios.post('/api/products/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  await fetchProducts()
}

async function onRemoveClick(product) {
  await axios.delete(`/api/products/${product.id}/`)
  await fetchProducts()
  await fetchPhotos()
}

async function onProductEditClick(product) {
  productToEdit.value = { ...product }
  productsEditPictureRef.value.value = ''
}

async function onUpdateProduct() {
  const formData = new FormData()

  // если новый файл не выбран, старая картинка останется как есть
  const file = productsEditPictureRef.value.files[0]
  if (file) {
    formData.append('picture', file)
  }

  formData.set('name', productToEdit.value.name)
  formData.set('price', productToEdit.value.price)
  formData.set('stock', productToEdit.value.stock)
  formData.set('category', productToEdit.value.category)
  formData.set('manufacturer', productToEdit.value.manufacturer)

  await axios.put(`/api/products/${productToEdit.value.id}/`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  await fetchProducts()
}

async function onAlbumClick(product) {
  albumProduct.value = product
  albumPhotoUrl.value = photos.value.find((p) => p.product === product.id)?.image
}

async function onPhotosAdd() {
  // можно выбрать сразу несколько файлов, каждый отправляем отдельным запросом
  for (const file of albumPhotosRef.value.files) {
    const formData = new FormData()
    formData.set('product', albumProduct.value.id)
    formData.append('image', file)

    await axios.post('/api/product-photos/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  }
  albumPhotosRef.value.value = ''
  await fetchPhotos()
  if (!albumPhotoUrl.value) {
    albumPhotoUrl.value = albumPhotos.value[0]?.image
  }
}

async function onPhotoRemoveClick(photo) {
  await axios.delete(`/api/product-photos/${photo.id}/`)
  await fetchPhotos()
  albumPhotoUrl.value = albumPhotos.value[0]?.image
}

onBeforeMount(async () => {
  await fetchProducts()
  await fetchCategories()
  await fetchManufacturers()
  await fetchPhotos()
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
      <div class="col">
        <div class="form-floating">
          <select class="form-select" v-model="productToAdd.manufacturer" required>
            <option :value="m.id" v-for="m in manufacturers">{{ m.name }}</option>
          </select>
          <label for="floatingInput">Производитель</label>
        </div>
      </div>
      <div class="col-auto">
        <input
          class="form-control"
          type="file"
          ref="productsPictureRef"
          @change="productsAddPictureChange"
        />
      </div>
      <div class="col-auto">
        <img v-if="productAddImageUrl" :src="productAddImageUrl" style="max-height: 60px" alt="" />
      </div>
      <div class="col-auto">
        <button class="btn btn-primary">Добавить</button>
      </div>
    </div>
  </form>

  <div v-for="item in products" class="item">
    <div>{{ item.name }}</div>
    <div>{{ item.price }} руб.</div>
    <div>{{ item.stock }} шт.</div>
    <div>{{ categoriesById[item.category]?.name }}</div>
    <div>{{ manufacturersById[item.manufacturer]?.name }}</div>
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
      class="btn btn-secondary"
      @click="onAlbumClick(item)"
      data-bs-toggle="modal"
      data-bs-target="#albumModal"
    >
      Фото
    </button>
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
            <input type="number" step="0.01" class="form-control" v-model="productToEdit.price" />
            <label for="floatingInput">Цена</label>
          </div>
          <div class="form-floating mb-2">
            <input type="number" class="form-control" v-model="productToEdit.stock" />
            <label for="floatingInput">На складе</label>
          </div>
          <div class="form-floating mb-2">
            <select class="form-select" v-model="productToEdit.category">
              <option :value="c.id" v-for="c in categories">{{ c.name }}</option>
            </select>
            <label for="floatingInput">Категория</label>
          </div>
          <div class="form-floating mb-2">
            <select class="form-select" v-model="productToEdit.manufacturer">
              <option :value="m.id" v-for="m in manufacturers">{{ m.name }}</option>
            </select>
            <label for="floatingInput">Производитель</label>
          </div>
          <div>
            <label class="form-label">Новая картинка (необязательно)</label>
            <input class="form-control" type="file" ref="productsEditPictureRef" />
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

  <div class="modal fade" id="imageModal" tabindex="-1">
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-body">
          <img :src="bigImageUrl" class="img-fluid" alt="" />
        </div>
      </div>
    </div>
  </div>

  <div class="modal fade" id="albumModal" tabindex="-1">
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5">Фотографии: {{ albumProduct.name }}</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div v-if="albumPhotos.length === 0">Фотографий пока нет</div>
          <img v-if="albumPhotoUrl" :src="albumPhotoUrl" class="img-fluid mb-3" alt="" />

          <div class="album-row">
            <div v-for="photo in albumPhotos" class="album-item">
              <img
                :src="photo.image"
                style="max-height: 80px; cursor: pointer"
                @click="albumPhotoUrl = photo.image"
                alt=""
              />
              <button class="btn btn-sm btn-danger" @click="onPhotoRemoveClick(photo)">Удалить</button>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <input class="form-control" type="file" multiple ref="albumPhotosRef" />
          <button type="button" class="btn btn-primary" @click="onPhotosAdd">Загрузить</button>
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
.album-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.album-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
  align-items: center;
}
</style>