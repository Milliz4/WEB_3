<script setup>
import { onBeforeMount } from 'vue'
import { RouterLink, RouterView } from 'vue-router'
import axios from 'axios'
import Cookies from 'js-cookie'

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken')
})
</script>

<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary mb-3">
    <div class="container-fluid">
      <a class="navbar-brand" href="/">Магазин</a>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNavDropdown"
        aria-controls="navbarNavDropdown"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse justify-content-between" id="navbarNavDropdown">
        <ul class="navbar-nav">
          <li class="nav-item"><RouterLink class="nav-link" to="/customers">Покупатели</RouterLink></li>
          <li class="nav-item"><RouterLink class="nav-link" to="/addresses">Адреса</RouterLink></li>
          <li class="nav-item"><RouterLink class="nav-link" to="/categories">Категории</RouterLink></li>
          <li class="nav-item"><RouterLink class="nav-link" to="/manufacturers">Производители</RouterLink></li>
          <li class="nav-item"><RouterLink class="nav-link" to="/products">Товары</RouterLink></li>
          <li class="nav-item"><RouterLink class="nav-link" to="/orders">Заказы</RouterLink></li>
          <li class="nav-item"><RouterLink class="nav-link" to="/order-items">Позиции заказа</RouterLink></li>
          <li class="nav-item"><RouterLink class="nav-link" to="/reviews">Отзывы</RouterLink></li>
        </ul>
        <ul class="navbar-nav">
          <li class="nav-item dropdown">
            <a
              class="nav-link dropdown-toggle"
              href="#"
              role="button"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              Пользователь
            </a>
            <ul class="dropdown-menu">
              <li><a class="dropdown-item" href="/admin">Админка</a></li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </nav>

  <div class="container-fluid">
    <RouterView />
  </div>
</template>

<style scoped></style>