<template>
  <div class="vintage-divider" aria-hidden="true">
    <span class="line"></span>
    <svg class="flourish" viewBox="0 0 32 16">
      <path d="M16 14c-3 0-5.5-2.5-5.5-5.5S13 3 16 3s5.5 2.5 5.5 5.5S19 14 16 14z" fill="none" stroke="currentColor" stroke-width="1" />
      <path d="M16 0v3M12 8H4M20 8h8" stroke="currentColor" stroke-width="1" />
    </svg>
    <span class="line"></span>
  </div>
</template>

<style scoped>
.vintage-divider {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  width: 100%;
  padding: 0.5rem 0;
}

.line {
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, transparent, #c4b49a 20%, #c4b49a 80%, transparent);
  opacity: 0.7;
}

.flourish {
  width: 32px;
  height: 16px;
  color: #8b6f47;
  opacity: 0.8;
}
</style>
